#!/usr/bin/python
# coding: utf-8

import sys,math,struct,os,csv,numpy

class coopsplit:
    def __init__(self,target,offset,duration):
        self.target = target
        self.offset = offset
        self.duration = duration
        self.datalength = 112000000

    def Run(self):
        with open(self.target,'rb') as f:
            f.seek(self.offset*datalength*2)
            for i in xrange(self.duration):
                b = f.read(datalength*2)
                nary = numpy.fromstring(b,numpy.int16)*2.0258938232e-07
                mw = numpy.power(nary,2)/50
                powerlist = 10*numpy.log10(mw)
                powerlistf16 = powerlist.astype(numpy.float16)
                print powerlistf16
                fp = numpy.memmap('tmp'+str(i)+'.dat',dtype=numpy.float16,mode='w+',shape=datalength)
                fp[:] = powerlistf16[:]
                del fp

def selectsplit(target,meshcode,strlist):
    valuelists = map(int,strlist)
    num = len(valuelists)
    datalength = 112000000
    with open(target,'rb') as f:
        for i,offset in enumerate(valuelists):
            print i,offset
            f.seek(offset*datalength*2)
            b = f.read(datalength*2)
            nary = numpy.fromstring(b,numpy.int16)*2.0258938232e-07
            mw = numpy.power(nary,2)/50
            powerlist = 10*numpy.log10(mw)
            powerlistf16 = powerlist.astype(numpy.float16)
            print 'value'+str(i),powerlistf16
            fp = numpy.memmap('tmp'+str(i)+'.dat',dtype=numpy.float16,mode='w+',shape=datalength)
            fp[:] = powerlistf16[:]
            del fp

if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print 'Too few args'
        sys.exit(1)
    m = coopsplit(sys.argv[1],sys.argv[2],sys.argv[3])
    m.Run()

