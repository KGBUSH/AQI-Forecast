# coding: utf-8

from PmMySQL import *
import numpy as np
import pylab as pl




class DrawCityPm25(object):
    """
    根据时间和pm2_5 对city，包含n*monitors 条曲线
    老版本，x轴是1,2,3,4,5....
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

        self.timePointsList = []  # [[],[],[],...] 每个item的长度和cityPm25List的item一样。
        self.cityPm25List = []  #[  [],[],[]...   ] length = numMonitors

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
        pl.title("pm25/time   " + str(self.numMonitors))# give plot a title
        pl.xlabel('time')# make axis labels
        pl.ylabel('pm2.5')
        self.fill_cityPm25List()


        for i in xrange(self.numMonitors):
            pl.plot(self.timePointsList[i], self.cityPm25List[i], 'r')

        pl.show()# show the plot on the screen



    def fill_cityPm25List(self):
        """
        构建cityPm25List
        赋值 self.timePoints, self.cityPm25List
        :return:
        """
        for monitor in self.monitorsList:
            monitorData = []
            timePoints = []

            sql = "select pm2_5,time_point from table33 where area = '" + self.city.decode('utf-8') + "' and position_name = '" + monitor + "';"
            results = PmMySQL_L.Search(sqlstatement=sql)

            for item in results:
                pm2_5 = int(item[0])
                monitorData.append(pm2_5)
            self.cityPm25List.append(monitorData)

            for i in xrange(len(monitorData)):
                timePoints.append(i)
            self.timePointsList.append(timePoints)






if __name__ == '__main__':
    d = DrawCityPm25('昆明')
    d.drawCity()