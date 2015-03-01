#!/usr/bin/python
# coding: utf-8

import sys,math,struct,os,csv,numpy

class coopreader:
    def __init__(self,duration):
        self.duration = int(duration)
        self.datalength = 112000000

    def Run(self):
        powerlist = numpy.empty([self.duration,self.datalength],dtype=numpy.float16)
        #fp = range(self.duration)
        #for i in xrange(self.duration):
        powerlist = numpy.memmap('tmp.dat',dtype=numpy.float16,mode='r',shape=self.datalength*self.duration)
        #powerlist[i][:] = fp[i][:]
        #powerlist = powerlist.reshape(datalength*self.duration)
        histlist = numpy.histogram(powerlist[powerlist > -1000],bins=50)
        summation = 0
        for i in range(len(histlist[0])):
            prob=histlist[0][i]/float(len(powerlist))
            summation = prob + summation
            string = str(histlist[1][i])+','+str(prob)+','+str(summation)
            print string.rstrip()
            #print str(histlist[1][i])+','+str(prob)+','+str(summation)

def selectread(dic,valuestr):
    valuelists = map(int,valuestr)
    num = len(valuestr)
    datalength = 112000000
    powerlist = numpy.memmap('tmp.dat',dtype=numpy.float16,mode='r',shape=datalength*num)
    histlist = numpy.histogram(powerlist[powerlist > -1000],bins=50)
    summation = 0
    for i in range(len(histlist[0])):
        prob=histlist[0][i]/float(len(powerlist))
        summation = prob + summation
        string = str(histlist[1][i])+','+str(prob)+','+str(summation)
        print string.rstrip()
        #print str(histlist[1][i])+','+str(prob)+','+str(summation)

if __name__ == "__main__":
    m = coopreader(sys.argv[1])
    m.Run()

