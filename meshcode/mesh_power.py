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
        meshcode=args.meshcode
        
        self.reader = csv.reader(filter(lambda row: row[0]!='#', f))
        lists = [line for line in self.reader]
        powerlist=[]

        for line in lists:
            if(line[-1]==meshcode):
                powerlist.append(10*math.log10(float(line[-2])))
                print line[0],10*math.log10(float(line[-2]))
        #print powerlist
        #PDF&CDF
        sumention = 0
        histlist = numpy.histogram(powerlist,bins=100)
        for i in range(len(histlist[0])):
            prob=histlist[0][i]/float(len(powerlist))
            sumention=prob+sumention
            print histlist[1][i],prob,sumention
        #print args.start_time,args.duration
        

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
    parser = argparse.ArgumentParser(description = 'test')
    parser.add_argument('target',\
            action='store',\
            nargs=None,\
            default=None,\
            type=str,\
            )
    parser.add_argument('meshcode',\
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
   
