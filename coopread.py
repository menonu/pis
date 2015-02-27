#!/usr/bin/python
# coding: utf-8

import sys,math,struct,os,csv,numpy

class readheader:
    def Run(self):
        sec = 5
        datalength = 112000000
        powerlist = numpy.empty([5,datalength],dtype=numpy.float16)
        fp = range(5)
        for i in xrange(sec):
            fp[i] = numpy.memmap('tmp'+str(i)+'.dat',dtype=numpy.float16,mode='r',shape=datalength)
            print fp[i]
            powerlist[i][:] = fp[i][:]
        powerlist = powerlist.reshape(datalength*sec)
        histlist = numpy.histogram(powerlist[powerlist > -1000],bins=50)
        summation = 0
        for i in range(len(histlist[0])):
            prob=histlist[0][i]/float(len(powerlist))
            summation = prob + summation
            print str(histlist[1][i])+','+str(prob)+','+str(summation)


if __name__ == "__main__":
    m = readheader()
    m.Run()

