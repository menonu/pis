#!/usr/bin/python
# coding: utf-8

import ctypes,ConfigParser
from ctypes import *
import sys,math,struct,os,subprocess,csv,numpy,time,string
import datetime
import garmingusb

#sys.path.append('C:\\Program Files\\Tektronix\\RSA306\\RSA306 API')

class rsa:
    def __init__(self):
        self.libc = ctypes.windll.msvcrt
        self.fileio()
        self.rsa300 = ctypes.WinDLL("RSA300API.dll")
        self.Parse()
        self.iqLen = self.iqRecordLength*2
        self.floatArray = c_float * self.iqLen
        self.intArray = c_int * 10
        self.searchIDs = self.intArray() 
        self.deviceserial = c_wchar_p()
        self.numFound = c_int()
        self.time = datetime.datetime.today()
        self.strtime = self.time.strftime("%Y-%m-%d-%H-%M-%S")
        self.count = 0

    def fileio(self):
        self.fopen = self.libc.fopen
        self.fopen.argtypes = c_char_p,c_char_p
        self.fopen.restype = c_void_p
        self.fwrite = self.libc.fwrite
        self.fwrite.argtypes = c_void_p,c_size_t,c_size_t,c_void_p
        self.fwrite.restype = c_size_t

        self.fclose = self.libc.fclose
        self.fclose.argtypes = c_void_p,
        self.fclose.restype = c_int

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
        self.iqPath = config.get("IQDATA","IQpath")
        self.iqFilenameBase = config.get("IQDATA","IQFilenameBase")


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

    def SetIQData(self):
        self.timeout = c_int(self.iqTimeout)
        self.startindex = c_int(0)
        self.length = c_int(self.iqRecordLength)

        ret = self.rsa300.Run()
        self.ShowInfo()
        if ret is not 0:
            sys.stderr.write('Run Error! ' + str(ret))
            exit(1)
        print 'runnning...' 

    def ShowInfo(self):
        samplerate = c_double(10)
        self.rsa300.GetIQSampleRate(byref(samplerate))
        tmpl = '{0:20} : {1:>10g}'
        tmpld = '{0:20} : {1:>3.2e}'
        print '#'*36
        print tmpl.format('ReferenceLevel',self.referenceLevel)
        print tmpl.format('CenterFrequency',self.centerFrequency)
        print tmpl.format('IQRecordLength',self.iqRecordLength)
        print tmpl.format('IQSampleRate',samplerate.value)
        print tmpl.format('IQBandwidth',self.iqBandwidth)
        print tmpl.format('IQTimeout',self.iqTimeout)
        print '#'*36

    def WriteCSV(self):
        try:
            while True:
                self.f = self.fopen(self.iqPath+'/'+self.iqFilenameBase+self.strtime,'ab')
                self.GetIQData()
                self.fclose(self.f)
        finally:
            self.fclose(self.f)


    def GetIQData(self):
        ready = c_bool(False)
        iqData = self.floatArray()
        ret = self.rsa300.WaitForIQDataReady(self.timeout,byref(ready))
        if ret is not 0:
            sys.stderr.write('WaitForIQDataReady Error! ' + str(ret))
        if ready:
            #print 'IQData Ready'
            ret = self.rsa300.GetIQData(iqData,self.startindex,self.length)
            if ret is not 0:
                sys.stderr.write('GetIQData Error! ' + str(ret))
                exit(1)
        else:
            print 'Device not ready. Timeout (Check IQRecordLength)' + str(ret)
            sys.exit(1)
        self.count = self.count+1
        print '\b\b%d' % self.count
        self.fwrite(iqData,4,self.iqLen,self.f)
        #print 'write done'

    def Testfunc(self):
        print self.iqBandwidth
        
if __name__ == "__main__":
    gpsdevice = garmingusb.garmin()
    gpsdevice.start()
    m = rsa()
    try:
        m.Connect()
        m.Setdevice()
        m.SetIQData()
        m.WriteCSV()
        #m.Testfunc()
    except KeyboardInterrupt:
        print 'Aborted'
    finally:
        print 'stopping rsa306...'
        m.rsa300.Stop()
        m.rsa300.Disconnect()
        print 'Done. everything is fine :)'

