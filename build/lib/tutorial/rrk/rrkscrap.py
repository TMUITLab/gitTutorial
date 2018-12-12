from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
import numpy as np
import requests
import captcha
import msvcrt as m


class ShowNews:
    #def __init__(self)
        #tempurl = 'http://www.rrk.ir/News/ShowNews.aspx?Code=14301089'
        #self.news_session, self.news_data = ShowNews.news_newSession(tempurl)

    @staticmethod
    def news_newSession(url):
        print(' ==> creating session for ShowNews-page started...');
        s = requests.session();
        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0';
        s.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8';
        s.headers['Accept-Language'] = 'en-US,en;q=0.5';
        s.headers['Accept-Encoding'] = 'gzip, deflate';
        s.headers['Upgrade-Insecure-Requests'] = '1';

        r = s.get(url)
        soup = BeautifulSoup(r.content,"html.parser")

        data = {
            'ctl00$cphMain$btnCaptcha':'ارسال',
            'ctl00$cphMain$captcha$txtCaptcha': captcha.getDigit(soup.find('img',{'id':'imgCaptcha'})['src'])
        }

        state = {tag['name']: tag['value']
                 for tag in soup.select('input[name^=__]')
                 }

        data.update(state)
        print(' ==> session for ShowNews-page was created.');
        return s,data;

    def readNews(self,url):
        p = url.find('?Code=');
        docid = url[p + 6:]
        print("NewsID:"+docid + "...");

        news_session, news_data = ShowNews.news_newSession(url);
        f = news_session.post(url, data=news_data);
        soup = BeautifulSoup(f.content,"html.parser");

        if (soup.select_one("#cphMain_lblNewspaperNo") == None):
            print('Captcha was not Correct.');
            news_session, news_data = ShowNews.news_newSession(url);
            f = news_session.post(url, data=news_data);
            soup = BeautifulSoup(f.content,"html.parser")
        if(soup.select_one("#cphMain_lblNewspaperNo").text.strip() == ''):
            print('news Not Found');
            item = None;
        else:

            item = {
                'NewsType' : ' '.join(soup.select_one("#cphMain_lblNewsTitle").text.split()),
                'NewsDate' : ' '.join(soup.select_one("#cphMain_lblNewsDate").text.split()),
                'IndicatorNumber' : ' '.join(soup.select_one("#cphMain_lblIndikatorNumber").text.split()),
                'PageNumber' : ' '.join(soup.select_one("#cphMain_lblPageNumber").text.split()),
                'NewsPaperNo' : ' '.join(soup.select_one("#cphMain_lblNewspaperNo").text.split()),
                'City' : ' '.join(soup.select_one("#cphMain_lblNewsPaperCityType").text.split()),
                'Text' : ' '.join(soup.select_one("div.Jus").decode_contents().split())
            };
            print(" ==> NewsDate:"+ item['NewsDate'] + ",PageNumber:"+item['PageNumber']);


        return item;

    def readNewsList(self,urls):
        print ('number of urls is : ' + str(len(urls)));
        items = [];
        for url in urls:
            try:
                item = self.readNews(url);
            except:
                print(' ==> Connection Failed.')
                print('press enter to exit');
                return [];
                break;
            
            if(item != None):
                items = np.append(items,item);

        return items;

class ListNews:

   def __init__(self):
        self.list_session, self.list_data = ListNews.list_newSession()


   @staticmethod
   def list_newSession(args={}):
        print(' ==> creating session for NewsList-page started...');
        url = 'http://www.rrk.ir/News/NewsList.aspx';
        s = requests.session();
        s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0';
        s.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8';
        s.headers['Accept-Language'] = 'en-US,en;q=0.5';
        s.headers['Accept-Encoding'] = 'gzip, deflate';
        s.headers['Upgrade-Insecure-Requests'] = '1';

        r = s.get(url)
        soup = BeautifulSoup(r.content,"html.parser")

        # unsupported CSS Selector 'input[name^=ctl00][value]'
        data = {
            'ctl00$cphMain$ddlNewArchive':'1',
            'ctl00$cphMain$txtNewsText':'',
            'ctl00$cphMain$txtCompanySabtNumber':'',
            'ctl00$cphMain$cboHCNewsTypeCode':'',
            'ctl00$cphMain$txtIndikatorNumber':'',
            'ctl00$cphMain$txtNewspaperNo':'',
            'ctl00$cphMain$txtSabtNationalID':'',
            'ctl00$cphMain$txtReferenceNo':'',
            'ctl00$cphMain$txtDeclarationNo':'',
            'ctl00$cphMain$cboCityCode':'',
            'ctl00$cphMain$dteSabtDate$dteSabtDate_txtDate':'',
            'ctl00$cphMain$dteFromNewspaperDate$dteFromNewspaperDate_txtDate':'',
            'ctl00$cphMain$btnSearch': 'جستجو',
        }

        for item in data.keys():
            strargs = item[item.rfind('$')+1:]
            if(strargs in args.keys()):
                data[item] = args[strargs];

        state = {tag['name']: tag['value']
                 for tag in soup.select('input[name^=__]')
                 }

        data.update(state)

        r=s.post(url,data=data)
        soup = BeautifulSoup(r.content)

        state = {tag['name']: tag['value']
                 for tag in soup.select('input[name^=__]')
                 }
        data.pop('ctl00$cphMain$btnSearch', None)
        data.update(state)
        print(' ==> session for NewsList-page was created.');
        return s,data;


   def fetchNewsList(self,args={}):
        url = 'http://www.rrk.ir/News/NewsList.aspx'

        for item in self.list_data.keys():
            strargs = item[item.rfind('$')+1:]
            if(strargs in args.keys()):
                self.list_data[item] = args[strargs];

        urllist = [];
        for i in range(9):
            self.list_data['__EVENTTARGET'] = 'ctl00$cphMain$rptPagingRec$ctl0'+str(i+1)+'$btnNum';
            f = self.list_session.post(url, data=self.list_data);
            soup = BeautifulSoup(f.content);
            print(url+'-page:'+str(i+1))
            curbtn = soup.select_one('#cphMain_rptPagingRec_btnNum_'+str(i));
            if(curbtn != None and   curbtn['class']==['current'] ):
                newslist = soup.select(".NItem");
                for news in newslist:
                    print(' ==>'+news.select_one(".ShowNTitle a")['href'] +' added to list')
                    urllist = np.append(urllist, {
                        'NewsUrl': 'http://www.rrk.ir'+news.select_one(".ShowNTitle a")['href'],
                        'NewsTitle': ' '.join(news.select_one(".ShowNTitle a").text.replace('\n','').replace('\r','').strip().split()),
                        'ReferenceNo': ' '.join(news.select_one(".cNewsItem > span:nth-of-type(2)").text.replace('\n','').replace('\r','').strip().split()),
                        'NewsPaperNo': ' '.join(news.select_one(".cNewsItem > span:nth-of-type(4)").text.replace('\n','').replace('\r','').strip().split()),
                        'PageNumber': ' '.join(news.select_one(".cNewsItem > span:nth-of-type(6)").text.replace('\n','').replace('\r','').strip().split()),
                        'NewsPaperName': ' '.join(news.select_one(".cNewsItem > span:nth-of-type(7)").text.replace('\n','').replace('\r','').strip().split()),
                        'NewsDate': ' '.join(news.select_one(".cNewsItem > span:nth-of-type(9)").text.replace('\n','').replace('\r','').strip().split()),
                    });
        return urllist;
        """"
        print('Reading News Started ....');
        items = {};
        for url in urllist:
            print('' + news.select_one(".ShowNTitle a")['href'] + ' added to list')
            items = np.append(items,readNews(url['NewsUrl']));
        return  items;
        """

