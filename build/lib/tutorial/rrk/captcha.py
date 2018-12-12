import numpy as np
import os

import json
import io

this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, 'keys.json')
json1_file = open(DATA_PATH)
json1_str = json1_file.read()
dic=json.loads(json1_str)


def getDigit(url):
    # Do what you want
    p = url.find('&c=')+3;
    key = url[p:p + url[p:].find('&')];

    if(key in dic.keys() ):
        return str(int(dic[key]));
    return ""
