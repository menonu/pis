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
        self.reader = csv.reader(filter(lambda row: row[0]!='#', f))
        inputtime = a.Tconv(args.start_time)
        if args.m:
            endtime = inputtime + a.Tsec(60*args.duration) 
        else :
            endtime = inputtime + a.Tsec(args.duration) 
        #print inputtime,endtime
        lists = [line for line in self.reader if len(line)==10 and inputtime < a.Tconv(line[0]) < endtime]
        #print len(lists)
        powerlist=[]
        for line in lists:
            powerlist.append(10*math.log10(float(line[8])))
            #print a.Get_jst(line[0])
        #print powerlist
        sumention = 0
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
    parser.add_argument('start_time',\
            action='store',\
            nargs=None,\
            default=None,\
            type=str,\
            )
    parser.add_argument('duration',\
            action='store',\
            nargs=None,\
            default=None,\
            type=int,\
            )
    parser.add_argument('-m',\
            action='store_true',\
            default=False,\
            )

    args = parser.parse_args()
    if os.path.exists(args.target) == False:
        print 'file not found'
        exit(1)
    m.run(args)
   
