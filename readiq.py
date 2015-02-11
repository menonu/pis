#!/usr/bin/python
# coding: utf-8

import sys,math,struct,os,csv

class readheader:
    def Readheader(self):
        pass
    def Run(self):
        f = open(sys.argv[1],'rb')
        while True:
            b =  f.read(4)
            if b == "":
                break
            i = struct.unpack('f',b)[0]
            b =  f.read(4)
            if b == "":
                break
            q = struct.unpack('f',b)[0]
            print i,q

if __name__ == "__main__":
    m = readheader()
    m.Run()

