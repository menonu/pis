#!/usr/bin/python
# coding: utf-8

import sys,math,struct,os,csv

class readheader:
    def Run(self):
        f = open(sys.argv[1],'rb')
        while True:
            b =  f.read(4)
            if b is "":
                break
            t = struct.unpack('f',b)[0]
            print t

if __name__ == "__main__":
    m = readheader()
    m.Run()

