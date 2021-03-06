#!/usr/bin/python
# coding: utf-8

import sys,os,struct,pynmea,subprocess,threading,time
from serial import Serial


class garmin(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        print "GPS connecting..."
        self.com = Serial(
          port=0,
          baudrate=9600,
          bytesize=8,
          parity='N',
          stopbits=1,
          timeout=3,
          xonxoff=0,
          rtscts=0,
          writeTimeout=3,
          dsrdtr=None)
        #Initial Value
        if self.com.isOpen() is False:
            print "GPS Connection Error!"
            sys.exit(1)
        print "GPS Ready"
        self.out = self.readBuffer()
        if self.out == "":
            print "GPS Connection Error!"
            sys.exit(1)
        self.GetGPSData = self.out

    def run(self):
        while True:
            self.out = self.readBuffer()
            self.GetGPSData = self.out

    def readBuffer(self):
        try:
            data = self.com.read(1)
            n = self.com.inWaiting()
            if n:
                data = data + self.com.read(n)
            return data

        except Exception, e:
            print "GPS DataGet Error!",e
            sys.exit(1)

class streamingwrite(threading.Thread):
    def __init__(self,gpsp,fo):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.gm = gpsp
        self.fo = fo

    def run(self):
        while True:
            with open(self.fo,'a') as f:
                time.sleep(1)
                f.writelines(self.gm.GetGPSData)




if __name__ == "__main__":
    m = garmin()
    #p = Process(target=m.Testfunc,args=(10,))
    m.start()
    while True:
        time.sleep(1)
        print m.GetGPSData

