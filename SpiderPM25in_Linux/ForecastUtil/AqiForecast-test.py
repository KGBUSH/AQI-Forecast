# coding: utf-8

from DB.PmMySQL_L import *
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from StringIO import StringIO

import matplotlib.dates as dt
from datetime import datetime,timedelta

def polyfit(t,v):
    """
    拟合
    :param t:
    :param v:
    :return:
    """
    date = '2016-03-14'
    if len(date) == 10:
        date += ' 00'
    # thedatenum = dt.date2num(datetime.strptime(date,'%Y-%m-%d %H'))
    thedatenum = pl.date2num(datetime.strptime(date,'%Y-%m-%d %H'))  # 转化成X轴需要的数字


    t1 = t[-6:-1:2]
    v1 = v[-6:-1:2]
    z1 = np.polyfit(t1, v1, 3)
    p1 = np.poly1d(z1)
    print(p1) #在屏幕上打印拟合多项式
    # t1.append(thedatenum)
    yvals = p1(t1)
    plt.plot_date(t1, yvals, 'r')

    t2 = t[-7:-2:2]
    v2 = v[-7:-2:2]
    z2 = np.polyfit(t2, v2, 3)
    p2 = np.poly1d(z2)
    print (p2)
    # t2.append(thedatenum)
    yvals2 = p2(t2)
    plt.plot_date(t2, yvals2, 'm')



    plt.plot_date(thedatenum, p1(thedatenum), '-o')
    plt.plot_date(thedatenum, p2(thedatenum), '-o')
    plt.plot_date(thedatenum, (v[-3]+v[-2]+v[-1])/3, '-o')
    return 200




class DrawCityPm25(object):
    """
    根据时间和pm2_5 对city，包含n*monitors 条曲线
    新版本，X轴是时间
    """

    def __init__(self, cityname):
        """
        初始化一些参数
        :param cityname:城市名
        :return:
        """

        self.city = cityname
        self.city_highestAqi = 0
        self.monitorsList = []
        self.numMonitors = 0

        # self.timePointsList = []  # [[],[],[],...] 每个item的长度和cityPm25List的item一样。
        self.cityAqiList = []  #[  "","",""...   ] length = numMonitors
        self.cityAqiAVG_hour = ""  # 格式和cityAqiList中的元素一样，str
        self.cityAqiAVG_day = ""  # 格式和cityAqiList中的元素一样，str

        self.set()

        for item in self.monitorsList:
            print item


    def set(self):
        """
        找到城市下面的monitors,
        给两个参数赋值self.monitorsList, self.numMonitors
        :return:
        """
        monitors = []
        results = PmMySQL_L.SearchMonitors(city=self.city)
        for tuple in results:
            monitor_name = tuple[0]
            monitors.append(monitor_name)
        self.numMonitors = len(monitors)
        self.monitorsList = monitors

        sql = "select MAX(aqi) from table33 where area = '" + self.city + "';"
        result = PmMySQL_L.Search(sqlstatement=sql)
        self.city_highestAqi = int(result[0][0])


    def drawCityAQI_monitors(self):
        """
        作图,绘制monitors的曲线
        :return:
        """
        pl.title("aqi/time   " + str(self.numMonitors) + "_monitors")# give plot a title
        pl.xlabel('time')# make axis labels
        pl.ylabel('aqi')
        self.fill_cityAqiList()


        for monitorStr in self.cityAqiList:
            data = np.loadtxt(StringIO(monitorStr), dtype=np.dtype([("t", "S13"),("v", float)]))
            datestr = np.char.replace(data["t"], "T", " ")
            t = pl.datestr2num(datestr)
            v = data["v"]

            pl.plot_date(t, v, fmt="-o")
            # polyfit(t,v)

            # break



        pl.subplots_adjust(bottom=0.3)
        # pl.legend(loc=4)#指定legend的位置,读者可以自己help它的用法
        ax = pl.gca()
        ax.fmt_xdata = pl.DateFormatter('%Y-%m-%d %H:%M:%S')
        pl.xticks(rotation=70)
        # pl.xticks(t, datestr) # 如果以数据点为刻度，则注释掉这一行
        ax.xaxis.set_major_formatter(pl.DateFormatter('%Y-%m-%d %H:%M'))
        pl.grid()
        pl.show()# show the plot on the screen



    def drawCityAQI_avg(self):
        """
        绘制city级别的AQI曲线
        :return:
        """
        pl.title("AVGaqi/time   ")# give plot a title
        pl.xlabel('time')# make axis labels
        pl.ylabel('aqi')
        self.fill_cityAqiAVG_hour()

        # # 画出每个时间点
        # data = np.loadtxt(StringIO(self.cityAqiAVG_hour), dtype=np.dtype([("t", "S13"), ("v", float)]))
        # datestr = np.char.replace(data["t"], "T", " ")
        # t = pl.datestr2num(datestr)
        # t1 = dt.datestr2num(datestr)
        # k = pl.num2date(t)
        # v = data["v"]
        # pl.plot_date(t[-20:], v[-20:], fmt="-o")
        # # polyfit(t[-20:], v[-20:])

        # 画出每天00:00的图
        self.fill_cityAqiAVG_day()
        data = np.loadtxt(StringIO(self.cityAqiAVG_day), dtype=np.dtype([("t", "S13"), ("v", float)]))
        datestr = np.char.replace(data["t"], "T", " ")
        t = pl.datestr2num(datestr)
        k = pl.num2date(t)
        k2 = dt.num2date(t)
        v = data["v"]
        pl.plot_date(t, v, fmt="-o")
        teet = polyfit(t, v)




        pl.subplots_adjust(bottom=0.3)
        # pl.legend(loc=4)#指定legend的位置,读者可以自己help它的用法
        ax = pl.gca()
        ax.fmt_xdata = pl.DateFormatter('%Y-%m-%d %H:%M:%S')
        pl.xticks(rotation=70)
        # pl.xticks(t, datestr) # 如果以数据点为刻度，则注释掉这一行
        ax.xaxis.set_major_formatter(pl.DateFormatter('%Y-%m-%d %H:%M'))
        # pl.xlim(('2016-03-09 00:00', '2016-03-12 00:00'))
        pl.grid()  # 有格子
        pl.show()# show the plot on the screen
        print 'over'








    def fill_cityAqiList(self):
        """
        构建cityPm25List
        赋值 self.cityPm25List
        :return:
        """
        for monitor in self.monitorsList:
            monitorStr = ""

            sql = "select aqi,time_point from table33 where area = '" + self.city.decode('utf-8') + "' and position_name = '" + monitor + "';"
            results = PmMySQL_L.Search(sqlstatement=sql)

            for item in results:
                aqi = int(item[0])
                timepoint = item[1].encode('utf-8')[:-7]
                monitorStr += timepoint + ' ' + str(aqi) + '\n'
            self.cityAqiList.append(monitorStr)
            #
            # for i in xrange(len(monitorData)):
            #     timePoints.append(i)
            # self.timePointsList.append(timePoints)

    def fill_cityAqiAVG_hour(self):
        """
        构建 self.cityAqiAVG_hour
        每个时间点
        :return:
        """
        self.cityAqiAVG_hour = ""
        # 给定city 求每个时刻的AQI平均值
        sql = "select sum(aqi)/count(*) as ave_aqi, time_point from table33 where area = '" + self.city.decode('utf-8') + "'group by time_point;"
        results = PmMySQL_L.Search(sqlstatement=sql)
        for item in results:
            ave_aqi = int(item[0])
            timepoint = item[1].encode('utf-8')[:-7]
            self.cityAqiAVG_hour += timepoint + ' ' + str(ave_aqi) + '\n'

    def fill_cityAqiAVG_day(self):
        """
        构建 self.cityAqiAVG_day
        每一天00:00的数据
        :return:
        """
        self.cityAqiAVG_day = ""
        # 给定city 求每个时刻的AQI平均值
        sql = "select sum(aqi)/count(*) as ave_aqi, time_point from table33 where area = '" + self.city.decode('utf-8') + "' and time_point LIKE '%00:00:00%' group by time_point;"
        results = PmMySQL_L.Search(sqlstatement=sql)
        for item in results:
            ave_aqi = int(item[0])
            timepoint = item[1].encode('utf-8')[:-7]
            self.cityAqiAVG_day += timepoint + ' ' + str(ave_aqi) + '\n'









if __name__ == '__main__':
    d = DrawCityPm25('北京')
    # d.drawCityAQI_monitors()
    d.drawCityAQI_avg()
    # d.drawCityAQI_monitors()