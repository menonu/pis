#!/usr/bin/python
# coding: utf-8

import ctypes,ConfigParser
from ctypes import *
from pynmea import nmea
import sys,math,struct,os,subprocess,csv,numpy,time,string
import datetime
import garminusb

#sys.path.append('C:\\Program Files\\Tektronix\\RSA306\\RSA306 API')
class rsa:
    def __init__(self):
        self.libc = ctypes.windll.msvcrt
        self.fileio()
        self.rsa300 = ctypes.WinDLL("RSA300API.dll")
        self.Parse()
        self.intArray = c_int * 10
        self.searchIDs = self.intArray() 
        self.deviceserial = c_wchar_p()
        self.numFound = c_int()
        self.gpsstrbuff = create_string_buffer(1024) 
        self.time = datetime.datetime.today()
        self.strtime = self.time.strftime("%Y%m%d%H%M%S")
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


    #Config File Parser
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

    def Warn(self):
        tmpl = '{0:20} : {1:>10g}'
        tmpld = '{0:20} : {1:>3.2e}'
        print '#'*36
        print tmpl.format('ReferenceLevel',self.referenceLevel)
        print tmpl.format('CenterFrequency',self.centerFrequency)
        print tmpl.format('IQRecordLength',self.iqRecordLength)
        print '#'*36
        print 'Is that OK? (y) ',
        tmps = raw_input()
        if tmps is 'y' or tmps is 'Y':
            pass
        else:
            exit(1)

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
        rl = c_double(self.referenceLevel)
        cf = c_double(self.centerFrequency)
        iqbw = c_double(self.iqBandwidth)
        self.rsa300.SetCenterFreq(cf)
        self.rsa300.SetReferenceLevel(rl)
        self.rsa300.SetIQBandwidth(iqbw)

        triggerMode = c_int(0) # 0 is freerun mode, 1 is triggered mode
        self.rsa300.SetTriggerMode(triggerMode)

    def SetIQData(self):
        self.timeout = c_int(self.iqTimeout)
        self.startindex = c_int(0)
        self.samplerate = c_double()
        print 'Getting device parameter'

        ret = self.rsa300.Run()
        if ret is not 0:
            sys.stderr.write('Run Error! ' + str(ret))
            sys.exit(1)

        self.rsa300.GetIQSampleRate(byref(self.samplerate))
        self.iqRecordLength = int(self.samplerate.value)
        self.length = c_int(self.iqRecordLength)
        self.iqLen = self.iqRecordLength*2
        self.floatArray = c_float * self.iqLen

        ret = m.rsa300.Stop()
        if ret is not 0:
            "Device Stop Error! " + str(ret)
            sys.exit(1)
        self.rsa300.SetIQRecordLength(self.length)

        ret = self.rsa300.Run()
        if ret is not 0:
            sys.stderr.write('Run Error! ' + str(ret))
            sys.exit(1)

    def ShowInfo(self):
        self.giqlength = c_long()
        self.gbandwidth = c_double()
        self.gcenterfrequency = c_double()
        self.greflevel = c_double()

        #Get device setting
        self.rsa300.GetIQRecordLength(byref(self.giqlength))
        self.rsa300.GetIQBandwidth(byref(self.gbandwidth))
        self.rsa300.GetCenterFreq(byref(self.gcenterfrequency))
        self.rsa300.GetReferenceLevel(byref(self.greflevel))

        tmpl = '{0:20} : {1:>10g}'
        tmpld = '{0:20} : {1:>3.2e}'
        print '#'*36
        print tmpl.format('ReferenceLevel',self.greflevel.value)
        print tmpl.format('CenterFrequency',self.gcenterfrequency.value)
        print tmpl.format('IQRecordLength',self.giqlength.value)
        print tmpl.format('IQSampleRate',self.samplerate.value)
        print tmpl.format('IQBandwidth',self.gbandwidth.value)
        print tmpl.format('IQTimeout',self.iqTimeout)
        print '#'*36

    def WriteCSV(self):
        self.iqData = self.floatArray()
        self.f = self.fopen(self.iqPath+'/'+self.iqFilenameBase+self.strtime +'.dat','ab')
        try:
            while True:
                self.GetIQData()
        finally:
            self.fclose(self.f)


    def GetIQData(self):
        ready = c_bool(False)
        #iqData = self.floatArray()
        for i in xrange(5):
            ret = self.rsa300.WaitForIQDataReady(self.timeout,byref(ready))
            if ready.value is True:
                break
            if ret is 35:
                print '\nIQDATA wait timeout. Retry...'
            if ret is 36:
                self.ReProcess()
                sys.exit(1)
            #35 means Timeout
            else:
                '\nError Code' + str(ret)
                sys.exit(1)

        if ready:
            print '\r    working...',
            #self.GetGPSstring()
            self.MakeHeader()
            ret = self.rsa300.GetIQData(self.iqData,self.startindex,self.length)
            if ret is not 0:
                sys.stderr.write('GetIQData Error! ' + str(ret))
                sys.exit(1)
        else:
            print 'Device not ready.' + str(ret)
            sys.exit(1)
        self.count = self.count+1
        print '%d captured' % self.count,
        self.fwrite(self.gpsstrbuff,1,1024,self.f)
        self.fwrite(self.iqData,4,self.iqLen,self.f)

    def MakeHeader(self):
        self.GetGPSstring()
        struct.pack_into('l' ,self.gpsstrbuff,512,self.giqlength.value)
        struct.pack_into('f' ,self.gpsstrbuff,516,self.gcenterfrequency.value)
        struct.pack_into('f' ,self.gpsstrbuff,524,self.gbandwidth.value)
        struct.pack_into('f' ,self.gpsstrbuff,532,self.greflevel.value)
        struct.pack_into('f' ,self.gpsstrbuff,540,self.samplerate.value)

    def GetGPSstring(self):
        #self.gps = nmea.GPRMC()
        #self.gps.parse(gpsdevice.GetGPSData)
        st = str(gpsdevice.GetGPSData).rstrip()
        struct.pack_into('%ds' % len(st),self.gpsstrbuff,0,gpsdevice.GetGPSData)

    def ReProcess(self):
        print '#####Reconnect#####'
        time.sleep(1)
        m.Connect()
        m.Setdevice()
        m.SetIQData()
        m.ShowInfo()
        m.WriteCSV()

    def Testfunc(self):
        print self.iqBandwidth
        
if __name__ == "__main__":
    gpsdevice = garminusb.garmin()
    gpsdevice.start()
    m = rsa()
    m.Warn()
    try:
        m.Connect()
        m.Setdevice()
        m.SetIQData()
        m.ShowInfo()
        m.WriteCSV()
    except KeyboardInterrupt:
        print '\nAborted'
    finally:
        print 'stopping rsa306...'
        m.rsa300.Stop()
        m.rsa300.Disconnect()
        print 'Done. everything is fine :)'

