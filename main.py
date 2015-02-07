#!/usr/bin/python
# coding: utf-8

import ctypes,ConfigParser
from ctypes import *
import sys,math,struct,os,subprocess,csv,numpy
import garmingusb

#sys.path.append('C:\\Program Files\\Tektronix\\RSA306\\RSA306 API')

class rsa:
    def __init__(self):
        self.Parse()
        self.rsa300 = ctypes.WinDLL("RSA300API.dll")
        self.iqLen = self.iqRecordLength*2
        self.floatArray = c_float * self.iqLen
        self.intArray = c_int * 10
        self.searchIDs = self.intArray() 
        self.deviceserial = c_wchar_p()
        self.numFound = c_int()

    def Parse(self):
        config = ConfigParser.SafeConfigParser()
        config.read("./parameter.conf")
        #DEVICE section
        self.referenceLevel = int(config.get("DEVICE","ReferenceLevel"))
        self.centerFrequency = float(config.get("DEVICE","CenterFrequency"))
        #IQDATA section
        self.iqRecordLength = int(config.get("IQDATA","IQRecordLength"))
        self.iqBandwidth = float(config.get("IQDATA","IQBandwidth"))
        self.iqTimeout = int(config.get("IQDATA","IQTimeout"))

    def Connect(self):
        print 'connecting...'
        ret = self.rsa300.Search(self.searchIDs,byref(self.deviceserial),byref(self.numFound))
        if ret is 0:
            self.rsa300.Connect(self.searchIDs[0])
            print 'done'
        else:
            sys.stderr.write('Connect Error! ' + str(ret))
            sys.exit(1)

    def Setdevice(self):
        length = c_int(self.iqRecordLength)
        rl = c_double(self.referenceLevel)
        cf = c_double(self.centerFrequency)
        iqbw = c_double(self.iqBandwidth)
        self.rsa300.SetIQRecordLength(length)
        self.rsa300.SetCenterFreq(cf)
        self.rsa300.SetReferenceLevel(rl)
        self.rsa300.SetIQBandwidth(iqbw)

        triggerMode = c_int(0) # 0 is freerun mode, 1 is triggered mode
        self.rsa300.SetTriggerMode(triggerMode)

    def GetIQData(self):
        ready = c_bool(False)
        timeout = c_int(self.iqTimeout)
        startindex = c_int(0)
        length = c_int(self.iqRecordLength)

        ret = self.rsa300.Run()
        if ret is not 0:
            sys.stderr.write('Run Error! ' + str(ret))
            exit(1)
        print 'runnning...' 
        ret = self.rsa300.WaitForIQDataReady(timeout,byref(ready))
        if ret is not 0:
            sys.stderr.write('WaitForIQDataReady Error! ' + str(ret))
        iqData = self.floatArray()
        if ready:
            print 'IQData Ready'
            ret = self.rsa300.GetIQData(iqData,startindex,length)
            if ret is not 0:
                sys.stderr.write('GetIQData Error! ' + str(ret))
                exit(1)
        else:
            print 'Device not ready... (GetIQdata)'
        z = [[iqData[x],iqData[x+1],gpsdevice.GetGPSData] for x in xrange(self.iqRecordLength)]
        for line in z:
            print line
    
    def Testfunc(self):
        print self.iqBandwidth
        
if __name__ == "__main__":
    gpsdevice = garmingusb.garmin()
    gpsdevice.start()
    m = rsa()
    m.Parse()
    m.Connect()
    try:
        m.Setdevice()
        m.GetIQData()
        #m.Testfunc()
    except KeyboardInterrupt:
        print 'Aborted'
    finally:
        print 'stop rsa306'
        m.rsa300.Stop()
        m.rsa300.Disconnect()

