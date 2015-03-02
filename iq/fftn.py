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
        self.samplerate = 14e6
        self.fftpoint = 4096
        self.r = readfile
        self.start = int(sys.argv[2])
        pass

    def run(self):
        with open(sys.argv[1],'rb') as f:
#            size = 0
#            gpsblock = f.read(self.half)
#            f.seek(-512,1)
#            headerblock = f.read(self.headerlen)
#            gpsbuf = struct.unpack('512s',gpsblock)[0]
#            gpsstr = gpsbuf.rstrip(' \t\r\n\0').split(',')
#            date = '20'+gpsstr[9][4:]+gpsstr[9][2:4]+gpsstr[9][0:2]+str(int(gpsstr[1][0:2])+9)+gpsstr[1][2:]
#            fformat = struct.Struct('f').unpack
            f.seek(1024,1)
            body = f.read(self.valuelen)
        nary = numpy.fromstring(body,numpy.float32)
        bnary = nary.reshape(self.valuelen/4/2,2)
        tnary = nary.reshape(self.valuelen/4/2,2).transpose()
        zary = tnary[0]+1j*tnary[1]
        fftary = zary[self.start:self.start+self.fftpoint]
        #len(fftary)
        specary = numpy.fft.fft(fftary,self.fftpoint)
        
        powerspecary = numpy.power(numpy.abs(specary)/numpy.sqrt(2),2)
        freqary = numpy.fft.fftfreq(self.fftpoint,d=1/self.samplerate)
        shiftary = numpy.fft.fftshift(freqary)
        powershift = numpy.fft.fftshift(powerspecary)
        #print shiftary
        #print powershift
        powershiftdbm = 10*numpy.log10(powershift*1000/50)
        outp = numpy.vstack([shiftary,powershiftdbm]).transpose()
        numpy.savetxt('spectrum.txt',outp)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Too few args"
        sys.exit(1)
    try:
        m = splitter(sys.argv[1])
        m.run()
    except KeyboardInterrupt:
        pass
