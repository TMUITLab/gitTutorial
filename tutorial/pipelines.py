# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import csv
import json;

class TutorialPipeline(object):
    def process_item(self, item, spider):
        # get category and use it as filename
        docid = int(item['DocID']);
        dname = str(int(docid / 1000000));
        filename = str(int(docid / 1000) % 1000);

        if (os.path.exists('rrk-data\\'+dname) == False):
            os.mkdir('rrk-data\\'+dname);

        filename =  'rrk-data\\'+dname+ '\\'+filename+'.json'

        line = json.dumps(dict(item)) + ",\n";
        # open file for appending
        with open(filename, 'a',encoding='utf-8') as f:
            f.write(line)

            # write all data in row
            # warning: item is dictionary so item.values() don't have to return always values in the same order
            # writer.writerow(item.values())

        return item
