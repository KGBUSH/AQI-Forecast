# coding: utf-8


from Entity.AirIndicators import *
from Entity.settings import *

from xml.etree import ElementTree
from lxml import etree
import urllib
import urllib2
import time
import random



printCount = 0  # 后面输出计数


class SpiderPm25in(object):
    """
    爬虫
    """

    def __init__(self):
        """
        两个数组初始化，从文件中读入地区中文名及其拼音
        :return:
        """
        self.airindicatorsLists = []  # List<AirIndicators>
        self.cityLists = []  # [['/zhoukou', '周口'],[]]
        #Some User Agents
        self.hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
                  {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
                  {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]


        f_cityinfo = open(Settings.CITY_DATA_LOCATION, 'r')
        line = f_cityinfo.readline()

        while line:
            cityItem = line.split()
            self.cityLists.append([cityItem[1].strip()[1: -2], cityItem[2].strip()])
            line = f_cityinfo.readline()
        f_cityinfo.close()
        # for item in self.cityLists:
        #     print item[0], item[1]



    def dealing(self):
        """
        爬取数据
        :return:
        """

        for cityItem in self.cityLists:
            cityUrl = 'http://www.pm25.in' + cityItem[0]
            cityChinese = cityItem[1]
            self.getPointData(cityUrl, cityChinese)
            time.sleep(1)



    def getPointData(self, cityUrl, cityChinese):
        """
        根据指定城市访问页面，爬取各项所需数据
        :param cityUrl:url
        :param cityChinese: 城市中文
        :return:
        """
        global printCount

        req = urllib2.Request(cityUrl, headers=self.hds[random.randint(0,2)])
        page = urllib2.urlopen(req, timeout=10)
        # page = urllib.urlopen(cityUrl)
        html = page.read()
        if '热门城市' in html:
            # 找不到访问页面，重定向回主页
            print 'wrong url!'
            return
        # return html
        page = etree.HTML(html.decode('utf-8'))

        time = page.xpath(u"/html/body[@class='aqis_live_data']/div[@class='container']/div[@class='span12 avg']/"
                          u"div[@class='span11'][2]/div[@class='live_data_time']/p")
        for t in time:
            updatetime = t.text[7:]

        advice = page.xpath(u"/html/body[@class='aqis_live_data']/div[@class='container']/div[@class='span12 avg']/"
                            u"div[@class='span12 caution']/div[@class='action']/p")
        for ad in advice:
            advice = ad.text.split()[1]
        airdatas = page.xpath(u"/html/body[@class='aqis_live_data']/div[@class='container']/div[@class='table']/"
                           u"table[@id='detail-data']/tbody/tr")

        citychinese = cityChinese

        for item in airdatas:
            for x in xrange(len(item)):
                if item[x].text == '_':
                    item[x].text = Settings.NOT_DETECTED
                if item[x].text is None:
                    item[x].text = 'None'

            monitor, = item[0].text,

            aqi, = item[1].text,
            qualitylevel, = item[2].text,

            pm2_5, = item[4].text,
            pm10, = item[5].text,
            co, = item[6].text,
            no2, = item[7].text,
            o3, = item[8].text,
            o3_8h, = item[9].text,
            so2, = item[10].text,

            nowMonitor = AirIndicators(citychinese, monitor, aqi, qualitylevel, pm2_5,
                     pm10, co, no2, o3, o3_8h, so2, updatetime, advice)

            print str(printCount), '. ', citychinese, monitor, aqi, qualitylevel, pm2_5,\
                pm10, co, no2, o3, o3_8h, so2, updatetime, advice

            printCount += 1
            # print aqi, type(aqi)
            # print item[1].text, type(item[1].text)
            # print type(item)
            self.airindicatorsLists.append(nowMonitor)







if __name__ == '__main__':

    while 1:
        f = open('C:\\Users\\KGBUS\\PycharmProjects\\SpiderHeweather\\data\\results.txt', 'w')
        s = SpiderPm25in()
        # s.dealing()
        s.getPointData('http://www.pm25.in/zunyi', '遵义')
        for data in s.airindicatorsLists:
            # print data
            item = data.cityChinese + ' '
            item += data.monitor.encode('utf-8') + ' '
            item += data.aqi + ' '
            item += data.qualityLevel.encode('utf-8') + ' '
            item += data.pm2_5 + ' '
            item += data.pm10 + data.co + ' '
            item += data.no2 + ' '
            item += data.o3 + ' '
            item += data.o3_8h + ' '
            item += data.so2 + ' '
            item += data.updateTime.encode('utf-8') + ' '
            item += data.advice.encode('utf-8')
            item += '\n'
            f.write(item)

        f.close()
        time.sleep(3600)
