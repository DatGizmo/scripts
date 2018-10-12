#!/usr/bin/python

import sys
import os
import binascii
from subprocess import call

def hashimage(baseName):
    call(["openssl", "dgst", "-sha256", "-binary", "-out", baseName + ".hash", baseName + ".img"])

def verify(baseName, privKey):
    call(["openssl", "dgst", "-sha256", "-verify", privKey+".pub", "-signature", baseName+".sig", baseName+".hash"])

def extractPub(privKey):
    call(["openssl", "rsa", "-in", privKey, "-pubout", "-out", privKey+".pub"])

def extractSig(fn, pos, size):
    f = open(fn, 'rb')
    fp = open(fn+".sig", 'wb')
    pos += 24 #Offset for the string + sig info + key_id
    chunk = size - pos
    f.seek(pos)
    fp.write(f.read(chunk))
    fp.close()

def extractImg(fn, pos):
    f = open(fn, 'rb')
    fp = open(fn+".img", 'wb')
    fp.write(f.read(pos))
    fp.close()
    f.close()


if __name__ == "__main__":
    fn = sys.argv[1]
    privKey = sys.argv[2]
    extractPub(privKey)
    size = os.path.getsize(fn)
    imgEnd = 0
    with open(fn, 'rb') as f:
        for pos in range(size-1, 0, -1):
            f.seek(pos)
            by = f.read(1)
            if by == b'C':
                f.seek(pos)
                by = f.read(10)
                if by == b"CERT_OTHER":
                    imgEnd = pos
                    break
    if imgEnd > 0:
        extractSig(fn, imgEnd, size)
        extractImg(fn, imgEnd)
        hashimage(fn)
        verify(fn, privKey)

