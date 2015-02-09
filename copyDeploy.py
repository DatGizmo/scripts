#!/usr/bin/python

import datetime
import sys
import os
import shutil

def can_symlink(testFolder):
    symlink_path = testFolder + "can_symlink"
    try:
        os.symlink(testFolder, symlink_path)
    except (OSError, NotImplementedError, AttributeError):
        can = False
    else:
        os.remove(symlink_path)
        can = True
    return can


def myCopy(source, destination, canLink):
    if canLink:
        shutil.copy2(source, destination)
    else:
        shutil.copyfile(source, destination)


def copyrecursively(source_folder, destination_folder):
    canLink = can_symlink(destination_folder)
    for root, dirs, files in os.walk(source_folder):
        for item in files:
            src_path = os.path.join(root, item)
            dst_path = os.path.join(destination_folder, src_path.replace(source_folder, ""))
            if os.path.exists(dst_path):
                if os.stat(src_path).st_mtime > os.stat(dst_path).st_mtime:
                    print ("Overwrite file: %s to %s" % (src_path, dst_path))
                    myCopy(src_path, dst_path, canLink)
                else:
                    print ("Target file already exists and is not older than source file %s - %s" % (src_path, dst_path))
            else:
                print ("Copy file: %s to %s" % (src_path, dst_path))
                if canLink and os.path.islink(src_path):
                    linkto = os.readlink(src_path)
                    os.symlink(linkto, dst_path)
                else:
                    myCopy(src_path, dst_path, canLink)
        for item in dirs:
            src_path = os.path.join(root, item)
            dst_path = os.path.join(destination_folder, src_path.replace(source_folder, ""))
            if not os.path.exists(dst_path):
                os.mkdir(dst_path)



targetPath = '/imageStorage'
sourcePath = os.environ['SOURCE_PATH']
jobName = os.environ['PARENT_JOB']

now = datetime.datetime.now()

if len(targetPath) <= 0:
    targetPath = "./"
elif not (targetPath.endswith("/")):
    targetPath += "/"

targetPath += jobName + now.strftime("/%Y%m%d") + "/"

if not os.path.exists(sourcePath):
    print "Source path doesn't exitst"
    exit(-1)

if not os.path.exists(targetPath):
    print "Create target folder: " + targetPath
    os.makedirs(targetPath)

print targetPath
print jobName
copyrecursively(sourcePath, targetPath)
