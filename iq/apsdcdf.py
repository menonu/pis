#!/usr/bin/python
# coding: utf-8
import sys,math,struct,os,subprocess,csv,numpy,time,string,itertools
import datetime
from signal import signal,SIGPIPE,SIG_DFL
import iqcdf

signal(SIGPIPE,SIG_DFL)

class psdavgpower:
    def __init__(self,readfile,fftpoint):
        self.half = 512
        self.headerlen = 1024
        self.valuelen = 112000000
        self.samplerate = 14e6
        self.fftpoint = fftpoint
        self.targetfrequency = 760e6
        self.blackman = numpy.blackman(self.fftpoint)
        self.normalize = 1/numpy.average(numpy.power(self.blackman,2))
        self.file = readfile
        pass

    def getpower(self):
        with open(self.file,'rb') as f:
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
        alength = len(zary)
        newlen = self.fftpoint*(alength/self.fftpoint)
        psdarrays = zary[0:newlen].reshape((alength/self.fftpoint,self.fftpoint))
        #print psdarrays
        specary = numpy.fft.fft(psdarrays*self.blackman,self.fftpoint)/self.fftpoint
        absary = numpy.abs(specary)
        powerspecary = numpy.power(absary,2)
        freqary = numpy.fft.fftfreq(self.fftpoint,d=1/self.samplerate)
        shiftary = numpy.fft.fftshift(freqary)+self.targetfrequency
        powershift = numpy.fft.fftshift(powerspecary)
        #print shiftary
        #print powershift
        powershiftdbm = 10*numpy.log10(powershift*self.normalize/50/0.001)
        avgarrays = numpy.average(powershiftdbm,axis=1)
        return avgarrays
        #outp = numpy.vstack([shiftary,powershiftdbm]).transpose()
            #numpy.savetxt('spectrum.txt',outp)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Too few args"
        sys.exit(1)
    try:
        m = psdavgpower(sys.argv[1],fftpoint=256)
        powerarray = m.getpower()
        cdf = iqcdf.cdf(powerarray)
        lists = cdf.getcdf(histbin=2000)
        writer = csv.writer(sys.stdout)
        for line in lists:
            writer.writerow(line)

    except KeyboardInterrupt:
        pass
