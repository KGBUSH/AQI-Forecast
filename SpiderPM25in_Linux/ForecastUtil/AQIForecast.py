# coding: utf-8

from DB.PmMySQL_L import *
from CountAQI import *

import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from StringIO import StringIO

import matplotlib.dates as dt
from datetime import datetime,timedelta
import json



def hoursSub(bigtime, smalltime):
    """
    return hours gap
    :param bigtime:
    :param smalltime:
    :return:
    """
    # bigtime = bigtime.replace('T', ' ')
    # smalltime = smalltime.replace('T', ' ')
    daygap = (datetime.strptime(bigtime.split('T')[0],'%Y-%m-%d') - datetime.strptime(smalltime.split('T')[0],'%Y-%m-%d')).days
    if 'T' in bigtime:
        hourgap = int(bigtime.split('T')[1]) - int(smalltime.split('T')[1])
    else:
        hourgap = -int(smalltime.split('T')[1])
    return daygap*24 + hourgap



class AQIForecast(object):
    """
    Air quality forecast based on the given location and time
    """

    def __init__(self, location, time):
        """
        初始化
        :param location:
        :param time:
        :return:
        """
        self._userLocation = location #这个定义需要再改下！！！！！
        self._userTime = time  # validInput: '2016-03-05T15';'2016-03-05'

        self.city = ''  # based on the locType to split the _userLocation
        self.monitor = ''  # only if the locType is 'monitor', it works and not equal to ''

        self.locValid = True  # if neither city nor monitor, False
        self.locType = ''  # 'city' or 'monitor'
        self.timeValid = True  # if time is before,False
        self.timeType = ''  # 'future' or 'database'

        self.mintime_database = ''
        self.maxtime_database = ''

        # forecast variable
        self.forecastAqi = -1
        self.xyArrayStr = ""
        self.cityHighestAqi = 0


        self.checkInput()

    def checkInput(self):
        """
        as the name
        :return:
        """
        sql = "select area, position_name from table33 where concat(area,position_name) like '" + self._userLocation + "%';"
        sqlresults = PmMySQL_L.Search(sqlstatement=sql)
        if len(sqlresults) <= 0:
            self.locValid = False  # location invalid
            return
        # judge the location's type
        if sqlresults[0][1] == sqlresults[1][1]:
            self.locType = 'monitor'
            self.city = sqlresults[0][0].encode('utf-8')
            self.monitor = sqlresults[0][1].encode('utf-8')
        else:
            self.locType = 'city'
            self.city = sqlresults[0][0].encode('utf-8')
            self.monitor = ''

        self.set_parameterTime()

        # 格式不对或者在before，均为False
        if self._userTime < self.mintime_database or (len(self._userTime) != 10 and len(self._userTime) != 13):
            self.timeValid = False  # time invalid
            return
        # judge the time's type
        if self.mintime_database <= self._userTime <=self.maxtime_database:
            self.timeType = 'database'
        else:
            self.timeType = 'future'


    def set_parameterTime(self):
        """
        找到数据库中最大最小时间
        :return:
        """
        try:
            if self.locType == 'city':
                timesql = "select min(time_point) from table33 where area = '" + self.city + "';"
                sqlresults2 = PmMySQL_L.Search(timesql)
                self.mintime_database = sqlresults2[0][0].encode('utf-8')[:-7]

                timesql = "select max(time_point) from table33 where area = '" + self.city + "';"
                sqlresults3 = PmMySQL_L.Search(timesql)
                self.maxtime_database = sqlresults3[0][0].encode('utf-8')[:-7]

            if self.locType == 'monitor':
                timesql = "select min(time_point) from table33 where position_name = '" + self.monitor + "';"
                sqlresults2 = PmMySQL_L.Search(timesql)
                self.mintime_database = sqlresults2[0][0].encode('utf-8')[:-7]

                timesql = "select max(time_point) from table33 where position_name = '" + self.monitor + "';"
                sqlresults3 = PmMySQL_L.Search(timesql)
                self.maxtime_database = sqlresults3[0][0].encode('utf-8')[:-7]
        except Exception, e:
            print "set_parameterTime ERROR: ", e





    # forecast module

    def forecast(self):
        """
        forecast based on the location and time
        :return:
        """
        if not self.locValid:
            print 'InputLocation Error'
            return
        if not self.timeValid:
            print 'InputTime Error'
            return

        if self.timeType == 'database':
            self.forecastAqi = self.find_InDB()
        if self.timeType == 'future':
            self.forecastAqi = self.forcast_InFuture()

        print "Forecast: ", self.city+self.monitor, "'s AQI at ", self._userTime, " is ", self.forecastAqi



    def find_InDB(self):
        """
        time is during the minTime~maxTime
        :return:
        """
        self.fill_xyArrayStr_hour()
        xyArray = self.xyArrayStr.split('\n')
        count = 0
        aqi_total = 0
        avg_aqi = 0
        for item in xyArray:
            if self._userTime in item:
                count += 1
                aqi_total += int(item.split()[1])
        if count > 0:
            avg_aqi = aqi_total/count
        else:
            for i in xrange(len(xyArray)):
                if xyArray[i].split()[0] > self._userTime:
                    next_value = int(xyArray[i].split()[1])
                    prior_value = int(xyArray[i-1].split()[1])
                    avg_aqi = (prior_value + next_value)/2
                    break
        return avg_aqi



    def forcast_InFuture(self):
        """
        time is in the future
        :return:
        """
        # the gap between InputTime and maxTime in database
        hourgap = hoursSub(bigtime=self._userTime, smalltime=self.maxtime_database)
        self.fill_cityhighestAqi()

        # count as day-level,
        # notice that the 2 types of _userTime: '2016-04-18T05' 05前面那个0必须要  or '2016-04-18'
        if hourgap >= 24:
            self.fill_xyArrayStr_day()
            c1 = CountAQI(xyArrayStr=self.xyArrayStr, futureTime=self._userTime, aqiUpperLimit=self.cityHighestAqi)
            return c1.ForecastDraw()
        # if the gap is between(0hour, 24hours)
        else:
            self.fill_xyArrayStr_hour()
            c2 = CountAQI(xyArrayStr=self.xyArrayStr, futureTime=self._userTime, aqiUpperLimit=self.cityHighestAqi)
            return c2.ForecastDraw()



        #
        # if self.locType == 'city':
        #     print 21
        #
        #
        #
        # if self.locType == 'monitor':
        #     print 22







    def fill_cityhighestAqi(self):
        """
        find the maxValue AQI of city in database
        :return:
        """
        sql = "select MAX(aqi) from table33 where area = '" + self.city + "';"
        results = PmMySQL_L.Search(sqlstatement=sql)
        self.cityHighestAqi = int(results[0][0])



    def fill_xyArrayStr_hour(self):
        """
        构建 self.xyArrayStr
        x: every time_point
        y: corresponding AQI value of time_point in database

        :return:
        """
        self.xyArrayStr = ""
        if self.locType == 'city':
            sql = "select sum(aqi)/count(*) as ave_aqi, time_point from table33 where area = '" + self.city.decode('utf-8') + "'group by time_point;"
        if self.locType == 'monitor':
            sql = "select aqi, time_point from table33 where area = '" + self.city.decode('utf-8') + "' and position_name = '" + self.monitor.decode('utf-8') + "';"

        results = PmMySQL_L.Search(sqlstatement=sql)
        for item in results:
            aqi = int(item[0])
            timepoint = item[1].encode('utf-8')[:-7]
            self.xyArrayStr += timepoint + ' ' + str(aqi) + '\n'


    def fill_xyArrayStr_day(self):
        """
        构建 self.xyArrayStr
        x: every time_point
        y: corresponding AQI value of time_point in database

        :return:
        """
        self.xyArrayStr = ""
        if self.locType == 'city':
            sql = "select sum(aqi)/count(*) as ave_aqi, time_point from table33 where area = '" + self.city.decode('utf-8') + "' and time_point LIKE '%00:00:00%' group by time_point;"
        if self.locType == 'monitor':
            sql = "select aqi, time_point from table33 where area = '" + self.city.decode('utf-8') + "' and position_name = '" + self.monitor.decode('utf-8') + "' and time_point LIKE '%00:00:00%';"

        results = PmMySQL_L.Search(sqlstatement=sql)
        for item in results:
            aqi = int(item[0])
            timepoint = item[1].encode('utf-8')[:-7]
            self.xyArrayStr += timepoint + ' ' + str(aqi) + '\n'




    """
    PHP Interaction
    """
    def jsonData(self):
        """
        :return: the json including: userLoc,userTime,  forecastAqi
        """
        dictData = {'userLoc':self._userLocation, 'userTime':self._userTime, 'inquiryAqi':self.forecastAqi}
        jData = json.dumps(dictData, ensure_ascii=False, indent=2)
        return jData



if __name__ == '__main__':
    # timeType : '2016-04-18T05' 05前面那个0必须要  or '2016-04-18'
    a = AQIForecast(location="上海杨浦", time="2016-04-28T20")
    a.forecast()
    print a.jsonData()