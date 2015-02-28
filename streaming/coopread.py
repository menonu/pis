#!/usr/bin/python
# coding: utf-8

import sys,math,struct,os,csv,numpy

class coopreader:
    def __init__(self,duration):
        self.duration = int(duration)

    def Run(self):
        datalength = 112000000
        powerlist = numpy.empty([self.duration,datalength],dtype=numpy.float16)
        fp = range(self.duration)
        for i in xrange(self.duration):
            fp[i] = numpy.memmap('tmp'+str(i)+'.dat',dtype=numpy.float16,mode='r',shape=datalength)
            powerlist[i][:] = fp[i][:]
        powerlist = powerlist.reshape(datalength*self.duration)
        histlist = numpy.histogram(powerlist[powerlist > -1000],bins=50)
        summation = 0
        for i in range(len(histlist[0])):
            prob=histlist[0][i]/float(len(powerlist))
            summation = prob + summation
            print str(histlist[1][i])+','+str(prob)+','+str(summation)

def selectread(dic,valuestr):
    valuelists = map(int,valuestr)
    num = len(valuestr)
    datalength = 112000000
    powerlist = numpy.empty([num,datalength],dtype=numpy.float16)
    fp = range(num)
    for i in xrange(num):
        fp[i] = numpy.memmap('tmp'+str(i)+'.dat',dtype=numpy.float16,mode='r',shape=datalength)
        powerlist[i][:] = fp[i][:]
    powerlist = powerlist.reshape(datalength*num)
    histlist = numpy.histogram(powerlist[powerlist > -1000],bins=50)
    summation = 0
    for i in range(len(histlist[0])):
        prob=histlist[0][i]/float(len(powerlist))
        summation = prob + summation
        print str(histlist[1][i])+','+str(prob)+','+str(summation)

if __name__ == "__main__":
    m = coopreader(sys.argv[1])
    m.Run()

