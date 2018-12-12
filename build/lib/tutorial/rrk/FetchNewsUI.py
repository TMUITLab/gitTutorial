import numpy as np
import io
import json
import sys
import math
import argparse
import os
import rrkscrap
urls = []

parser = argparse.ArgumentParser(description='these file created for scraping rrk. you can define list of urls to be scraped or define interval [from,to] ids.')
parser.add_argument('fid', type = int ,help='first id to scrap', nargs='?');
parser.add_argument('lid', type = int ,help='last id to scrap', nargs='?');
parser.add_argument('fname', nargs='?');
parser.add_argument('o');
args = parser.parse_args();

"""
class aruments:
    def __init__(self):
        self.fid = 14301000;
        self.lid = 14301999;
        self.fname = '';
args = aruments();
"""

oname = 'output.txt'
if(args != None and args.fname != None and args.fname != ''):
    fname = args.fname;
    urls = [];
    with io.open(fname, 'r') as fp:
        urls = np.append(urls,fp.readline());

    v = rrkscrap.ShowNews();
    items = v.readNewsList(urls);
    with io.open(oname, 'w') as fp:
        for x in items:
            fp.write(x);

else:

    if(os.path.exists('rrk-raw')==False):
        os.mkdir('rrk-raw');

    batchsize1 = 10000;
    batchsize2 = 100;
    if(args.fid != None):
        fid = args.fid;
    if(args.lid != None):
        lid = args.lid;
    rfid = int(math.floor(fid / batchsize2)*batchsize1);
    rlid = int(math.ceil(lid / batchsize2)*batchsize1);

    cfid = math.floor(fid / batchsize2);
    clid = math.ceil(lid / batchsize2)

    v = rrkscrap.ShowNews();
    for i in range(clid, cfid,-1):
        urls=[];
        [b,a] = [min(lid,i*batchsize2-1),max(fid,(i-1)*batchsize2)];

        dname = str(int(fid/(batchsize1*batchsize2)));
        filename = str(int(a/batchsize2) % batchsize1);
        if(os.path.exists('rrk-raw\\'+dname +'\\'+filename + '.txt')):
            continue;

        if (os.path.exists('rrk-raw\\'+dname) == False):
            os.mkdir('rrk-raw/'+dname);
        for j in range(b,a-1,-1):
            urls = np.append(urls, 'http://rrk.ir/News/ShowNews.aspx?Code=' + str(j));

        print("////////////////////////////////")
        items = v.readNewsList(urls);
        if(len(items) > 0):
            with io.open('rrk-raw\\'+dname +'\\'+filename + '.txt', 'w',encoding='utf-8') as fp:
                for x in items:
                    fp.write(str(x));
            print(' ==>file saved.')
        else:
            print(' ==> Connection Lost');
        print("////////////////////////////////")








