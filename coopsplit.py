#!/usr/bin/python
# coding: utf-8

import sys,math,struct,os,csv,numpy

class readheader:
    def Run(self):
        sec = 5
        datalength = 112000000
        offset = int(sys.argv[2])
        with open(sys.argv[1],'rb') as f:
            f.seek(offset*datalength*2)
            for i in xrange(sec):
                b = f.read(datalength*2)
                nary = numpy.fromstring(b,numpy.int16)*2.0258938232e-07
                mw = numpy.power(nary,2)/50
                powerlist = 10*numpy.log10(mw)
                powerlistf16 = powerlist.astype(numpy.float16)
                print powerlistf16
                fp = numpy.memmap('tmp'+str(i)+'.dat',dtype=numpy.float16,mode='w+',shape=datalength)
                fp[:] = powerlistf16[:]
                del fp

if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print 'Too few args'
        sys.exit(1)
    m = readheader()
    m.Run()

