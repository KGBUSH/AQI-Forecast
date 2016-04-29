# -*- coding: utf-8 -*-


from datetime import datetime,timedelta
import numpy as np
import pylab as pl

# t = np.loadtxt("..\\data\\exampledata.txt", np.object)
# date = pl.datestr2num( list(t[:,0] + " " + t[:,1]) )
# value = t[:,2].astype(np.float)
#
#
# pl.plot_date(date, value)
# pl.show()
#
# # pl.plot_date(np.array(date1), value1)
# # today = datetime.now()
# # dates = [today + timedelta(days=i) for i in range(3)]
# # #values = [random.randint(1, 20) for i in range(10)]
# # values = [3,2,8]
# # pl.plot_date(pl.date2num(dates), values, linestyle='-')
# # pl.show()
#
# #
# # 2011.05.31 10:12:58    0
# # 2011.05.31 10:12:59    1
# # 2011.05.31 10:13:00    2
# # 2011.05.31 10:13:01    3
# # 2011.05.31 10:13:02    4
# # 2011.05.31 10:13:03    5
# # 2011.05.31 10:13:04    6
# # 2011.06.10 10:13:05    7
a = 1
b = 2
c = 3
threeForecastList = [a, b, c]
for i in xrange(len(threeForecastList)):
    if threeForecastList[i] >= 3:
        threeForecastList[i] = 2.5
    if threeForecastList[i] <= 1:
        threeForecastList[i] = 1.5
print threeForecastList
print a