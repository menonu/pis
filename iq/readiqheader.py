#!/usr/bin/python
# coding: utf-8
import sys,math,struct,os,subprocess,csv,numpy,time,string,itertools
import datetime
from signal import signal,SIGPIPE,SIG_DFL

signal(SIGPIPE,SIG_DFL)

class splitter:
    def __init__(self,readfile):
        self.half = 512
        self.headerlen = 1024
        self.valuelen = 112000000
        self.r = readfile
        pass

    def run(self):
        with open(sys.argv[1],'rb') as f:
            size = 0
            gpsblock = f.read(self.half)
            f.seek(-512,1)
            headerblock = f.read(self.headerlen)
            gpsbuf = struct.unpack('512s',gpsblock)[0]
            gpsstr = gpsbuf.rstrip(' \t\r\n\0').split(',')
            date = '20'+gpsstr[9][4:]+gpsstr[9][2:4]+gpsstr[9][0:2]+str(int(gpsstr[1][0:2])+9)+gpsstr[1][2:]
            fformat = struct.Struct('f').unpack
            print date+','+\
                    str(float(gpsstr[3][:-7])+float(gpsstr[3][-7:])/60)+','+\
                    str(float(gpsstr[5][:-7])+float(gpsstr[5][-7:])/60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Too few args"
        sys.exit(1)
    try:
        m = splitter(sys.argv[1])
        m.run()
    except KeyboardInterrupt:
        pass
