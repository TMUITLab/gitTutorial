import numpy as np
import io
import json
import sys
import rrkscrap

args = {
    'ctl00$cphMain$txtNewsText': '',
    'ctl00$cphMain$txtCompanySabtNumber':'',
    'ctl00$cphMain$cboHCNewsTypeCode': '',
    'ctl00$cphMain$txtIndikatorNumber': '',
    'ctl00$cphMain$txtNewspaperNo':'',
    'ctl00$cphMain$txtSabtNationalID': '',
    'ctl00$cphMain$txtReferenceNo': '',
    'ctl00$cphMain$txtDeclarationNo': '',
    'ctl00$cphMain$cboCityCode': '',
    'ctl00$cphMain$dteSabtDate$dteSabtDate_txtDate': '',
    'ctl00$cphMain$dteFromNewspaperDate$dteFromNewspaperDate_txtDate': ''
}

for i in range(len(sys.argv)):
    if( i>0):
        key = args.keys[i-1];
        args[key] = sys.argv[i];

v = rrkscrap.ListNews();
output = v.fetchNewsList(args);

with io.open('NewsList-output.txt', 'w') as fp:
    for item in output:
        fp.write(item['NewsUrl'] + '\n');

with io.open('NewsList-output.json', 'w') as fp:
    json.dump(output, fp)
