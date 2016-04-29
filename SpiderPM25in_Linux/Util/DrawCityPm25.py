# coding: utf-8

from PmMySQL import *
import numpy as np
import pylab as pl
from StringIO import StringIO



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
        self.monitorsList = []
        self.numMonitors = 0

        # self.timePointsList = []  # [[],[],[],...] 每个item的长度和cityPm25List的item一样。
        self.cityPm25List = []  #[  "","",""...   ] length = numMonitors

        self.setMonitorsList()

        for item in self.monitorsList:
            print item


    def setMonitorsList(self):
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


    def drawCity(self):
        """
        作图
        :return:
        """
        pl.title("pm25 / time   " + str(self.numMonitors) + "_monitors")# give plot a title
        pl.xlabel('time')# make axis labels
        pl.ylabel('pm2.5')
        self.fill_cityPm25List()


        for monitorStr in self.cityPm25List:
            data = np.loadtxt(StringIO(monitorStr), dtype=np.dtype([("t", "S13"),("v", float)]))
            datestr = np.char.replace(data["t"], "T", " ")
            t = pl.datestr2num(datestr)
            v = data["v"]
            pl.plot_date(t, v, fmt="-o")



        pl.subplots_adjust(bottom=0.3)
        # pl.legend(loc=4)#指定legend的位置,读者可以自己help它的用法
        ax = pl.gca()
        ax.fmt_xdata = pl.DateFormatter('%Y-%m-%d %H:%M:%S')
        pl.xticks(rotation=70)
        # pl.xticks(t, datestr) # 如果以数据点为刻度，则注释掉这一行
        ax.xaxis.set_major_formatter(pl.DateFormatter('%Y-%m-%d %H:%M'))
        pl.grid()
        pl.show()# show the plot on the screen



    def fill_cityPm25List(self):
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
                pm2_5 = int(item[0])
                timepoint = item[1].encode('utf-8')[:-7]
                monitorStr += timepoint + ' ' + str(pm2_5) + '\n'
            self.cityPm25List.append(monitorStr)
            #
            # for i in xrange(len(monitorData)):
            #     timePoints.append(i)
            # self.timePointsList.append(timePoints)






if __name__ == '__main__':
    d = DrawCityPm25('上海')
    d.drawCity()