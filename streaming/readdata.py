#!/usr/bin/python
# coding: utf-8

import sys,math,struct,os,csv,numpy

class readheader:
    def Run(self):
        f = open(sys.argv[1],'rb')
        b = f.read(224000000)
        nary = numpy.fromstring(b,numpy.int16)*2.0258938232e-07
        mw = numpy.power(nary,2)/50
        powerlist = 10*numpy.log10(mw)
        #powerlist2 = numpy.array([0.1,0.2,0.3,0.4])
        #print powerlist.dtype
        #print powerlist2
        #print numpy.sort(powerlist)
        #print 10*math.log10(numpy.average(mw))
        #print (numpy.where(tf == True))
        histlist = numpy.histogram(powerlist[powerlist > -1000],bins=50)
        #print numpy.histogram(powerlist2,bins=100)
        #print numpy.histogram(powerlist,bins=100)
        sumention = 0
        #print histlist
        for i in range(len(histlist[0])):
            prob=histlist[0][i]/float(len(powerlist))
            sumention=prob+sumention
            print str(histlist[1][i])+','+str(prob)+','+str(sumention)

        

if __name__ == "__main__":
    m = readheader()
    m.Run()

