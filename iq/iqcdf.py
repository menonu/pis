#!/usr/bin/python
# coding: utf-8
import sys,math,struct,os,subprocess,csv,numpy,time,string,itertools,argparse
import datetime
from signal import signal,SIGPIPE,SIG_DFL

signal(SIGPIPE,SIG_DFL)

class splitter:
    def __init__(self,args):
        self.half = 512
        self.headerlen = 1024
        self.valuelen = 112000000
        self.inputfile = args.target
        self.outputdir = args.dir

    def run(self):
        with open(self.inputfile,'rb') as f:
            size = 0
            gpsblock = f.read(self.half)
            f.seek(-512,1)
            headerblock = f.read(self.headerlen)
            gpsbuf = struct.unpack('512s',gpsblock)[0]
            gpsstr = gpsbuf.rstrip(' \t\r\n\0').split(',')
            date = '20'+gpsstr[9][4:]+gpsstr[9][2:4]+gpsstr[9][0:2]+str(int(gpsstr[1][0:2])+9)+gpsstr[1][2:]
            fformat = struct.Struct('f').unpack
            f.seek(1024)
            body = f.read(self.valuelen)
        nary = numpy.fromstring(body,numpy.float32)
        bnary = nary.reshape(self.valuelen/4/2,2)
        tnary = nary.reshape(self.valuelen/4/2,2).transpose()
        #numpy.savetxt('iq.txt',bnary,fmt='%2.2e')
        powerary = (numpy.power(tnary[0],2)+numpy.power(tnary[1],2))
        powerlist = 10*numpy.log10(powerary*1000/50)
        histlist = numpy.histogram(powerlist[powerlist > -1000],bins=50)
        summation = 0
        for i in range(len(histlist[0])):
            prob=histlist[0][i]/float(len(powerlist))
            summation = prob + summation
            string = str(histlist[1][i])+','+str(prob)+','+str(summation)
            print string.rstrip()
        #dbary = 10*numpy.log10(powerary/50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'test')
    parser.add_argument('target',\
            action='store',\
            nargs=None,\
            default=None,\
            type=str,\
            )
    parser.add_argument('dir',\
            action='store',\
            nargs='?',\
            default='./',\
            type=str,\
            )
    args = parser.parse_args()
    try:
        m = splitter(args)
        m.run()
    except KeyboardInterrupt:
        pass
