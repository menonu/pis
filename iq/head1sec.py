#!/usr/bin/python
# coding: utf-8
import sys,math,struct,os,subprocess,csv,numpy,time,string,argparse
import datetime

class splitter:
    def __init__(self,args):
        self.half = 512
        self.headerlen = 1024
        self.valuelen = 112000000
        self.inputfile = args.target
        self.outputdir = args.dir
        pass

    def run(self):
        print self.inputfile
        with open(self.inputfile,'rb') as f:
            size = 0
            gpsblock = f.read(self.half)
            if gpsblock == "":
                print 'zero file'
                sys.exit(1)
            f.seek(-512,1)
            headerblock = f.read(self.headerlen)
            gpsbuf = struct.unpack('512s',gpsblock)[0]
            gpsstr = gpsbuf.rstrip(' \t\r\n\0').split(',')
            date = '20'+gpsstr[9][4:]+gpsstr[9][2:4]+gpsstr[9][0:2]+str(int(gpsstr[1][0:2])+9)+gpsstr[1][2:]
            bodyblock = f.read(self.valuelen)
            with open(self.outputdir + '/' + date + '.dat','wb') as fw:
                fw.write(headerblock)
                fw.write(bodyblock)
            size += 112
            print str(size)+'MB Write'
            print 'fine'
                



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'test')
    parser.add_argument('target',\
            action='store',\
            nargs=None,\
            default=None,\
            type=str,\
            )
    parser.add_argument('dir',\
            action='store',\
            nargs='?',\
            default='./',\
            type=str,\
            )
    args = parser.parse_args()
    if os.path.exists(args.target) == False:
        print 'file not found'
        exit(1)
    m = splitter(args)
    m.run()
