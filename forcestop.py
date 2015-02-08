#!/usr/bin/python
# coding: utf-8

import sys,math,struct,os,csv,ctypes
from ctypes import *

class stoprsa306:
    def Run(self):
        self.rsa300 = ctypes.WinDLL("RSA300API.dll")
        self.intArray = c_int * 10
        self.searchIDs = self.intArray() 
        self.deviceserial = c_wchar_p()
        self.numFound = c_int()
        self.rsa300.Search(self.searchIDs,byref(self.deviceserial),byref(self.numFound))
        self.rsa300.Connect(self.searchIDs[0])
        self.rsa300.Stop()
        self.rsa300.Disconnect()

if __name__ == "__main__":
    m = stoprsa306()
    m.Run()

