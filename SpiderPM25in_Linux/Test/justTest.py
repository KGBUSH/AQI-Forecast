# coding: utf-8
import matplotlib.pyplot as plt
import numpy as np
#潘海东,2014/1/13

x = np.arange(1, 17, 1)
y = np.array([4.00, 6.40, 8.00, 8.80, 9.22, 9.50, 9.70, 9.86, 10.00, 10.20, 10.32, 10.42, 10.50, 10.55, 10.58, 10.60])

x2 = np.ndarray

z1 = np.polyfit(x, y, 4)#用2次多项式拟合
p1 = np.poly1d(z1)
yy = p1(20)  # 打印多项式y = f(x)的值
print yy
print(p1) #在屏幕上打印拟合多项式



yvals=p1(x)#也可以使用yvals=np.polyval(z1,x)
plot1=plt.plot(x, y, '*',label='original values')
plot2=plt.plot(x, yvals, 'r',label='polyfit values')
plt.xlabel('x axis')
plt.ylabel('y axis')
plt.xlim((0,30))
plt.legend(loc=2)#指定legend的位置,读者可以自己help它的用法
plt.title('polyfitting')
plt.show()


