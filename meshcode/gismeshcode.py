#!/usr/bin/python
# coding: utf-8

import sys,math,struct,os,csv

class meshcode_convert:
    def Generatemeshcode(self,list):
        dLat = float(list[0])
        dLon = float(list[1])
        
        I1_code = int(dLat * 1.5)
        K1_code = int(dLon % 100)
        
        I1_lat = I1_code /1.5
        K1_lon = math.floor(dLon)

        I2_code = int((dLat - I1_lat) / 0.0833333333)
        K2_code = int((dLon - K1_lon) / 0.125)
        
        I2_lat = I1_lat + I2_code * 0.0833333333
        K2_lon = K1_lon + K2_code * 0.125
        
        I3_code = int((dLat - I2_lat) / 0.00833333333)
        K3_code = int((dLon - K2_lon) / 0.0125)
        
        I3_lat = I2_lat + I3_code * 0.00833333333 
        K3_lon = K2_lon + K3_code * 0.0125 
        
        Ia_code = int((dLat-I3_lat) / 0.000833333333)
        Ka_code = int((dLon-K3_lon) / 0.00125)

        Ia_lat = I3_lat + Ia_code * 0.000833333333
        Ka_lon = K3_lon + Ka_code * 0.00125

        Ib_code = int((dLat - Ia_lat) / 0.0000833333333)
        Kb_code = int((dLon-Ka_lon) / 0.000125)
        #print I1_code,K1_code,I2_code,K2_code,I3_code,K3_code,Ia_code,Ka_code,Ib_code,Kb_code 
        return "{0:2d}{1:2d}-{2:d}{3:d}-{4:d}{5:d}-{6:d}{7:d}-{8:d}{9:d}".format(I1_code,K1_code,I2_code,K2_code,I3_code,K3_code,Ia_code,Ka_code,Ib_code,Kb_code)

if __name__ == "__main__":
    m = meshcode_convert()
    print m.Generatemeshcode([35.197222, 136.902797])
    print m.Generatemeshcode([35.192799, 136.899916])
    
