
# coding: utf-8

#import sys
#sys.path.append("../")

from PM25inFields import *
# from settings import *
from PmMySQL import *

import urllib2
import time


class SpiderPm25in(object):
    """
    爬虫：Pm25in。使用AppKey
    """

    def __init__(self):
        """
        初始化一些参数
        :return:
        """
        self.airindicatorsLists = []  # List<PM25inFields>
        self.homeUrl = 'http://www.pm25.in'

        self.aqiUrl = 'http://www.pm25.in/api/querys/all_cities.json?token=5A8qhLa16LvavqY1LUjb'
        self.getJsons = True  # API是否返回正确的数据

        self.flag_getTime = False
        self.nowTime = ''  # 记录当前时间

    @property
    def NowTime(self):
        return self.nowTime
    @property
    def GetJsons(self):
        return self.getJsons


    def dealing(self):
        """
        把API返回的数据用class: PM25inFields接受，然后存入self.airindicatorsLists
        :return:
        """
        print 'Program Running at ' + str(time.strftime('%Y-%m-%d %H:%M:%S'))

        req = urllib2.Request(self.aqiUrl)
        page = urllib2.urlopen(req, timeout=30)
        jsons = page.read()

        
        if len(jsons) > 1000:
            print 'API return successfully at: ' + str(time.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            print 'API return ERROR at: ' + str(time.strftime('%Y-%m-%d %H:%M:%S'))
            self.getJsons = False
            return



        nowLocation = 0

        while jsons.find('{', nowLocation) != -1:
            dictBegin = jsons.find('{', nowLocation)
            nowLocation = dictBegin
            dictEnd = jsons.find('}', nowLocation)
            nowLocation = dictEnd
            monitorStr = jsons[dictBegin: dictEnd+1]
            # 剔除掉没有数据的监测点
            if monitorStr[7] == '0':
                continue
            if '"primary_pollutant":null' in monitorStr:
                monitorStr = monitorStr.replace('"primary_pollutant":null', '"primary_pollutant":"_"')
            # 后面的指数如果为‘_’，API返回为0；意味着后面数据库中读出指数为0代表这个指标是无效，并没有检测到的。

            monitorDict = eval(monitorStr)
            m = PM25inFields(aqi=monitorDict['aqi'],
                             area=monitorDict['area'],
                             co=monitorDict['co'],
                             co_24h=monitorDict['co_24h'],
                             no2=monitorDict['no2'],
                             no2_24h=monitorDict['no2_24h'],
                             o3=monitorDict['o3'],
                             o3_24h=monitorDict['o3_24h'],
                             o3_8h=monitorDict['o3_8h'],
                             o3_8h_24h=monitorDict['o3_8h_24h'],
                             pm10=monitorDict['pm10'],
                             pm10_24h=monitorDict['pm10_24h'],
                             pm2_5=monitorDict['pm2_5'],
                             pm2_5_24h=monitorDict['pm2_5_24h'],
                             position_name=monitorDict['position_name'],
                             primary_pollutant=monitorDict['primary_pollutant'],
                             quality=monitorDict['quality'],
                             so2=monitorDict['so2'],
                             so2_24h=monitorDict['so2_24h'],
                             station_code=monitorDict['station_code'],
                             time_point=monitorDict['time_point']
                             )

            if not self.flag_getTime:
                self.nowTime = m.time_point
                self.flag_getTime = True
            self.airindicatorsLists.append(m)


    def InputDB(self, tableName):
        """
        把self.airindicatorsLists  # List<PM25inFields> 录入数据库
        :return:
        """
        num = 0
        for item in self.airindicatorsLists:
            PmMySQL_L.InsertItem(tableName=tableName, item=item)
            num += 1
        print str(num) + ' items inserted at  ' + self.nowTime




if __name__ == '__main__':

    mytable = 'table33'

    s = SpiderPm25in()
    s.dealing()

    if s.GetJsons:
        sql_lasttime = PmMySQL_L.Search_LastitemTime(mytable)
        if (s.NowTime != sql_lasttime) or (sql_lasttime == 'None') :
            s.InputDB(mytable)
            print 'Inserted ok!'
        else:
            print 'date repeat..'


    print '\n'