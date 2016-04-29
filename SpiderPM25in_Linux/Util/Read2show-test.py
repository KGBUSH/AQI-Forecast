# coding: utf-8

from PmMySQL import *
import numpy as np
import pylab as pl
# x = [1, 2, 3, 4, 5]# Make an array of x values
# y = [1, 4, 9, 16, 25]# Make an array of y values for each x value
# pl.plot(x, y)# use pylab to plot x and y
# pl.show()# show the plot on the screen

sqlstatement = "select pm2_5,time_point from table33 where position_name = '农展馆';"
mysql_result = PmMySQL_L.Search(sqlstatement)

result = PmMySQL_L.SearchMonitors('成都')
x = ['2016-03-20 11:45:39', '2016-03-20 12:45:39', '2016-03-20 13:45:39','2016-03-20 17:45:39']
date = pl.datestr2num(x)
y = [4,5,5,1]
# count = 1
# for tuple in mysql_result:
#     pm2_5 = int(tuple[0])
#     x.append(count)
#     count += 1
#     y.append(pm2_5)

pl.title('pm25/time')# give plot a title
pl.plot(date, y, 'r')# use pylab to plot x and y
pl.xlabel('time')# make axis labels
pl.ylabel('pm2.5')

# pl.ylim(0.0, 300.)
pl.show()# show the plot on the screen