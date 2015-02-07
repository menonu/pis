#!/usr/bin/python
# coding: utf-8

import sys,os,struct,pynmea,subprocess
from multiprocessing import Process
from serial import Serial

class garmin:
    def __init__(self):
        self.out = 'initial'
        self.com = Serial(
          port=0,
          baudrate=9600,
          bytesize=8,
          parity='N',
          stopbits=1,
          timeout=None,
          xonxoff=0,
          rtscts=0,
          writeTimeout=None,
          dsrdtr=None)
        if self.com.isOpen() is False:
            print "GPS Connection Error!"
            sys.exit(1)

    def Run(self):
        while True:
            self.out = self.readBuffer()
        print 'end'

    def GetGPSData(self):
        return self.out

    def readBuffer(self):
        try:
            data = self.com.read(1)
            n = self.com.inWaiting()
            if n:
                data = data + self.com.read(n)
            return data

        except Exception, e:
            print "GPS Error!",e
            sys.exit(1)




if __name__ == "__main__":
    m = garmin()
    p = Process(target=m.Run)
    p.start()
    for i in xrange(100):
        print m.GetGPSData()
        raw_input()

