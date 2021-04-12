#!/usr/bin/env python3

import xml.etree.ElementTree as xTree
import re
from collections import namedtuple

TestCase = namedtuple('TestCase', ['Class', 'Name', 'BoardName', 'Erromsg'])

def parseXml(filename):
    testList = []
    misIncReg = re.compile("No such file or directory\n.*(#include\s+[\w\.<>_&]*)", re.MULTILINE)
    oveflowReg = re.compile("FLASH' overflowed by \d* bytes\ncollect2: error: ld returned 1 exit status")
    hashReg = re.compile("RuntimeError: Hash of key in [\w/_\.']* contains 0x[a-fA-F0-9]*\. Please regenerate the key.")
    undefRefReg = re.compile("undefined reference to .*'")
    notFitReg = re.compile("section .*' will not fit in region .*[\w]*'")
    undecReg = re.compile("error: '[\w_]*' undeclared \(first use in this function\)")
    kconfReg = re.compile("error: Aborting due to Kconfig warnings")
    fileNotFound = re.compile("^\s*File not found:\n\s*[\w/._]*", re.MULTILINE)
    arrBoundReg = re.compile(".*\[-Werror=array-bounds\]")
    linkerReg = re.compile("(FAILED: [\w\/\.]*)(\n.*)*?")
    cmakeReg = re.compile("^(CMake Error at)[\s\.\/\w:'`]*\(message\):\n\s*[\w\s'`\n.*]*$", re.MULTILINE)
    root = xTree.parse(filename).getroot()
    for ts in root.findall('testsuite'):
        for tc in ts.findall('testcase'):
            if 0 < len(tc.findall('error')):
                bname = ts.get('name')
                cname = tc.get('classname')
                tname = tc.get('name')
                testList.append(TestCase(cname, tname, bname, "Error"))
            elif 0 < len(tc.findall('failure')):
                bname = ts.get('name')
                cname = tc.get('classname')
                ind = (cname.find(':') + 1)
                tname = tc.get('name')
                etext = tc.find('failure').text
                if(etext):
                    resString = ""
                    resInc = re.search(misIncReg, etext)
                    resOver = re.search(oveflowReg, etext)
                    resHash = re.search(hashReg, etext)
                    resUndef = re.search(undefRefReg, etext)
                    resNoFit = re.search(notFitReg, etext)
                    resUndec = re.search(undecReg, etext)
                    resKconf = re.search(kconfReg, etext)
                    resFiNo = re.search(fileNotFound, etext)
                    resArBound = re.search(arrBoundReg, etext)
                    resLink = re.search(linkerReg, etext)
                    resCmake = re.search(cmakeReg, etext)
                    if(resInc):
                        resString = resInc.group(0)
                    elif(resOver):
                        resString = resOver.group(0)
                    elif(resHash):
                        resString = resHash.group(0)
                    elif(resUndef):
                        resString = resUndef.group(0)
                    elif(resNoFit):
                        resString =resNoFit.group(0)
                    elif(resUndec):
                        resString = resUndec.group(0)
                    elif(resKconf):
                        resString = resKconf.group(0)
                    elif(resFiNo):
                        resString = resFiNo.group(0)
                    elif(resArBound):
                        resString = resArBound.group(0)
                    elif(resLink):
                        resString = "Linker error: %s" % resLink.group(0)
                    elif(resCmake):
                        resString = resCmake.group(0)

                    if(not resString):
                        print("----------START---------")
                        print(etext)
                        print("-----------END----------\n")
                resString = resString.replace('|', '')
                resString = resString.replace('\'', '')
                resString = resString.replace('\n', '')
                resString = resString.replace('`', '')
                resString = resString.replace('{', '\{')
                resString = resString.replace('}', '\}')
                resString = re.sub('\s+', ' ', resString)
                testList.append(TestCase(cname[ind:], tname, bname, resString))

    xmlind = filename.find(".xml")
    fp = open(filename[:xmlind] + ".yml", "w")
    tabfp = open(filename[:xmlind] + ".md", "w")
    tabfp.write("| Class Name | Test Name | Affected Boards | Error Message | Responsible |\n")
    tabfp.write("| ----- | ----- | ----- | ----- | ----- |\n")

    testList.sort(key=lambda tup: (tup[0], tup[1], tup[2]))

    curCName = ""
    curTName = ""
    first = True
    for el in testList:
        if(curCName != el.Class):
            curCName = el.Class
            curTName = el.Name

            fp.write("%s:\n" % el.Class)
            fp.write("\t%s:\n" % el.Name)
            fp.write("\t\t%s:\n" % el.BoardName)
            fp.write("\t\t\t\"%s\"\n" % el.Erromsg)

            tabfp.write("| %s | %s | %s | \"%s\" | |\n" % (el.Class, el.Name, el.BoardName, el.Erromsg))
            first = True
        elif(curTName != el.Name):
            curTName = el.Name
            fp.write("\t%s:\n" % el.Name)
            fp.write("\t\t%s:\n" % el.BoardName)
            fp.write("\t\t\t\"%s\"\n" % el.Erromsg)
            if(first):
                tabfp.write("| | %s | %s | \"%s\" | |\n" % (el.Name, el.BoardName, el.Erromsg))
                first = False
            else:
                tabfp.write("| | | %s | \"%s\" | |\n" % (el.BoardName, el.Erromsg))
        else:
            fp.write("\t\t%s:\n" % el.BoardName)
            fp.write("\t\t\t\"%s\"\n" % el.Erromsg)
            tabfp.write("| | | %s | \"%s\" | |\n" % (el.BoardName, el.Erromsg))

    fp.close()
    tabfp.close()

if __name__ == "__main__":
    parseXml("twister-report.xml")
    parseXml("twister.xml")
