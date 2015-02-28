#!/usr/bin/python
# coding: utf-8
import sys,math,struct,os,subprocess,csv,numpy,time,string,argparse
from collections import defaultdict
import datetime
import coopsplit

class splitter:
    def __init__(self,args):
        self.inputfile = args.target
        self.meshfile = args.mesh
        self.outputdir = args.dir

    def run(self):
        print self.inputfile
        meshdict = defaultdict(list)
        with open(self.meshfile,'r') as meshf:
            self.csvlines = csv.reader(meshf)
            for line in self.csvlines:
                meshdict[line[3]].append(line[4])
        
        for dic in meshdict:
            coopsplit.selectsplit(self.inputfile,dic,meshdict[dic])
            print dic,meshdict[dic]
            raw_input()
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'test')
    parser.add_argument('target',\
            action='store',\
            nargs=None,\
            default=None,\
            type=str,\
            )
    parser.add_argument('mesh',\
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
