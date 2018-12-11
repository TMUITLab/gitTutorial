import scrapy
import os
import json;
import numpy as np
import json
from tutorial.rrk import captcha

class rrkscrapper(scrapy.Spider):
    name = 'tutorial'
    start_urls = ['http://www.rrk.ir/News/ShowNews.aspx?Code=%d' % (n) for n in range(12500000, 12000000,-1)]

    download_delay = 1.5

    def start_requests(self):
        
        z = 12500000;

        print(z);
        urls = ['http://www.rrk.ir/News/ShowNews.aspx?Code=%d' % (n) for n in range(z, 12000000, -1)]
        for i, url in enumerate(urls):
            yield scrapy.Request(url, meta={'cookiejar': i},
                                 callback=self.parse)

    def parse(self, response):
        #for author in response.css('select#author > option ::attr(value)').extract():
        p = response.url.find('?Code=');
        docid = int(response.url[p + 6:])


        yield scrapy.FormRequest(
            response.url,
            meta={'cookiejar': response.meta['cookiejar']},
            #response = response,
            headers={
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language':'en-US,en;q=0.5',
                'Accept-Encoding':'gzip, deflate',
                'Upgrade-Insecure-Requests':'1'
            },
            formdata={
                '__EVENTTARGET':'',
                '__EVENTARGUMENT':'',
                '__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                '__VIEWSTATEGENERATOR':response.css('input#__VIEWSTATEGENERATOR::attr(value)').extract_first(),
                '__VIEWSTATEENCRYPTED':'',
                '__EVENTVALIDATION':response.css('input#__EVENTVALIDATION::attr(value)').extract_first(),
                'ctl00$cphMain$btnCaptcha':'ارسال',
                'ctl00$cphMain$captcha$txtCaptcha': captcha.getDigit(response.css('img#imgCaptcha::attr(src)').extract_first())
            },
            callback=self.parse_rrk_shownews
        )

    def parse_rrk_shownews(self, response):
        #for quote in response.css(".quote"):
        p = response.url.find('?Code=');
        docid = response.url[p+6:]
        #with open(docid + '.html', 'wb') as f:
        #   f.write(response.body)
        if(response.xpath("//span[@id='cphMain_lblNewsTitle']/text()").extract_first() == None):
            yield{
                'DocID': docid,
            };
        else:
            yield {
                'DocID': docid,
                'NewsType': response.xpath("//span[@id='cphMain_lblNewsTitle']/text()").extract_first(),
                'NewsDate': response.xpath("//span[@id='cphMain_lblNewsDate']/text()").extract_first(),
                'IndicatorNumber': response.xpath("//span[@id='cphMain_lblIndikatorNumber']/text()").extract_first(),
                'PageNumber': response.xpath("//span[@id='cphMain_lblPageNumber']/text()").extract_first(),
                'NewsPaperNo': response.xpath("//span[@id='cphMain_lblNewspaperNo']/text()").extract_first(),
                'NewsPaperName': response.xpath("//span[@id='cphMain_lblNewsPaperCityType']/text()").extract_first(),
                'Text': response.css("#cphMain_pnlNewsInfo > div.Jus").extract_first()
            };