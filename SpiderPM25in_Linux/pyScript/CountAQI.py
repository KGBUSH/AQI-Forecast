# coding: utf-8


import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from StringIO import StringIO

import matplotlib.dates as dt
from datetime import datetime,timedelta






class CountAQI(object):
    """
    based on the AQIForecast.xyArrayStr to calculate the future value
    """
    def __init__(self, xyArrayStr, futureTime, aqiUpperLimit):
        """
        initialization
        :return:
        """
        # the str(array<time+aqi>)
        self._xyArrayStr = xyArrayStr

        # notice that the 2 types of _userTime: '2016-04-18T05' 05前面那个0必须要  or '2016-04-18'
        self._forecastTime = futureTime

        # upper threshold
        self._aqiUpperLimit = aqiUpperLimit

        # the time need to forecast
        self._forecast_Value = 0


    def ForecastDraw(self):
        """
        at the day-level
        :return:
        """
        pl.title("aqi/time(day)")# give plot a title
        pl.xlabel('time')# make axis labels
        pl.ylabel('aqi')

        data = np.loadtxt(StringIO(self._xyArrayStr), dtype=np.dtype([("t", "S13"), ("v", float)]))
        datestr = np.char.replace(data["t"], "T", " ")
        t = dt.datestr2num(datestr)
        # k = pl.num2date(t)
        # k2 = dt.num2date(t)
        v = data["v"]
        if len(t) > 30:
            t = t[-30:]
            v = v[-30:]
        pl.plot_date(t, v, fmt="-o")
        self.polyfit(t, v)

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

        return self._forecast_Value


    def polyfit(self, t, v):
        """
        拟合
        :param t:
        :param v:
        :return:
        """
        t1 = t[-6:-1:2]
        v1 = v[-6:-1:2]
        z1 = np.polyfit(t1, v1, 4)
        p1 = np.poly1d(z1)
        print(p1) #在屏幕上打印拟合多项式
        yvals = p1(t1)
        plt.plot_date(t1, yvals, 'r')

        t2 = t[-5::2]
        v2 = v[-5::2]
        z2 = np.polyfit(t2, v2, 4)
        p2 = np.poly1d(z2)
        print (p2)
        yvals2 = p2(t2)
        plt.plot_date(t2, yvals2, 'm')


        # futureTime = '2016-03-14 10'
        if len(self._forecastTime) == 10:
            self._forecastTime += ' 00'
        if 'T' in self._forecastTime:
            self._forecastTime = self._forecastTime.replace('T', ' ')
        thedatenum = pl.date2num(datetime.strptime(self._forecastTime,'%Y-%m-%d %H'))  # 转化成X轴需要的数字

        # threshold control
        threeForecastList = [p1(thedatenum), p2(thedatenum), (v[-3]+v[-2]+v[-1])/3]
        for i in xrange(len(threeForecastList)):
            if threeForecastList[i] >= self._aqiUpperLimit:
                threeForecastList[i] = self._aqiUpperLimit
            if threeForecastList[i] <= 0:
                threeForecastList[i] = 0


        plt.plot_date(thedatenum, threeForecastList[0], '-o')
        plt.plot_date(thedatenum, threeForecastList[1], '-o')
        plt.plot_date(thedatenum, threeForecastList[2], '-o')

        # count the _forecast_Value
        self._forecast_Value = int((threeForecastList[0] + threeForecastList[1] + threeForecastList[2])/3)
        plt.plot_date(thedatenum, self._forecast_Value, '-*')

