#!/usr/bin/python
# coding: utf-8

import sys,math,struct,os,csv

class readheader:
    def Run(self):
        f = open(sys.argv[1],'rb')
        b = f.read(27)
        print '%s' % b
        f.seek(1024)
        t = f.read(8)
        b = struct.unpack('d',t)[0]
        print b
        t = f.read(8)
        b = struct.unpack('d',t)[0]
        print b
        t = f.read(8)
        b = struct.unpack('d',t)[0]
        print b
        f.seek(2048+4+6*4)
        t = f.read(8)
        b = struct.unpack('d',t)[0]
        print b
        t = f.read(8)
        b = struct.unpack('d',t)[0]
        print b
        t = f.read(8)
        b = struct.unpack('d',t)[0]
        print b


if __name__ == "__main__":
    m = readheader()
    m.Run()

