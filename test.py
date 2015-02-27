#!/usr/bin/python
# coding: utf-8

import numpy,time,datetime,sys,math,struct,os,subprocess,csv,re,argparse
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE,SIG_DFL)

class usrpparser:
    def __init__(self):
        pass
    def run(self,args):
        f = open(args.target,'r')
        self.reader = csv.reader(f)
        #print len(lists)
        #print powerlist
        sumention = 0
        powerlist=[]
        lists = [line for line in self.reader]
        for line in lists:
            powerlist.append(float(line[2]))
        #print a.Get_jst(line[0])
        #print powerlist
        histlist = numpy.histogram(powerlist,bins=200)
        for i in range(len(histlist[0])):
            prob=histlist[0][i]/float(len(lists))
            sumention=prob+sumention
            print str(histlist[1][i])+','+str(prob)+','+str(sumention)
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
    args = parser.parse_args()
    if os.path.exists(args.target) == False:
        print 'file not found'
        exit(1)
    m.run(args)
   
