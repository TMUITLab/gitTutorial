import scrapy
import  numpy
from scrapy.crawler import CrawlerProcess
class rkk1(scrapy.Spider):
    name = 'rrk1'
    start_urls = [
        "http://www.rrk.ir/News/ShowNews.aspx?Code=14301089",
        "http://www.rrk.ir/News/ShowNews.aspx?Code=14301089",

    ]
    download_delay = 1.5

    def parse(self, response):
        #for author in response.css('select#author > option ::attr(value)').extract():
        src = response.css("img[id='imgCaptcha']").xpath('@src').extract_first();
        val = src[41:41 + src[41:].find('&')];
        yield{
            'Token': val,
        }
