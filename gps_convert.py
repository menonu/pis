#!/usr/bin/python
# coding: utf-8

import numpy,time,datetime,sys,math,struct,os,subprocess,csv,re,argparse
from signal import signal, SIGPIPE, SIG_DFL
import gismeshcode

signal(SIGPIPE,SIG_DFL)

class usrpparser:
    def __init__(self):
        pass
    def run(self,args):
        f = open(args.target,'r')
        self.reader = csv.reader(filter(lambda row: row[0]!='#', f))
        lists = [line for line in self.reader]
        hour = []
        minute = []
        second = []
        lat = []
        lon = []
        mesh=[]
        num = 0
        for line in lists:
            lat = float(line[3][0:2]) + float(line[3][2:])/60
            lon = float(line[5][0:3]) + float(line[5][3:])/60
            hour = int(line[1][0:2])+9
            minute = int(line[1][2:4]) 
            second = int(line[1][4:6])
            mesh = meshcode.Generatemeshcode([lat,lon])
            print "{0:s}:{1:s}:{2:s},{3:s},{4:s},{5:s},{6:s}".format(str(hour),str(minute),str(second),str(lat),str(lon),mesh,str(num))
            num +=1
class modtime:
    def __init__(self):
        self.delta = datetime.timedelta(hours = 9)

    def Tsec(self,atime):
        return datetime.timedelta(seconds = int(atime))
    def Tconv(self,atime):
        return datetime.datetime.strptime(atime,'%Y/%m/%d %H:%M:%S')
    def Get_utc(self,atime):
        t = datetime.datetime.strptime(atime,'%Y/%m/%d %H:%M:%S')
        return (time.mktime(t.timetuple()))
    def Get_jst(self,atime):
        t = datetime.datetime.strptime(atime,'%Y/%m/%d %H:%M:%S')
        return int(time.mktime((t+self.delta).timetuple()))
        

if __name__ == "__main__":
    a = modtime()
    m = usrpparser()
    meshcode = gismeshcode.meshcode_convert()
    parser = argparse.ArgumentParser(description = 'test')
    parser.add_argument('target',\
            action='store',\
            nargs=None,\
            default=None,\
            type=str,\
            )
    args = parser.parse_args()
    if os.path.exists(args.target) == False:
        print 'file not found'
        exit(1)
    m.run(args)
   
