#!/usr/bin/python
# coding: utf-8

from DB.DoMySQL import *
from datetime import datetime,timedelta
from scipy import stats
import numpy as np

class CorrelationAna(object):

    def __init__(self, date):
        """
        初始化一些参数
        :param date:日期
        :return:
        """
        self.date = date
        self.level_dict={}

    def setCityAQI(self):
        """
        获取各城市AQI指数
        :return:
        """
        end_date = datetime.strptime(self.date, '%Y-%m-%d')
        start_date = end_date + timedelta(-29)
        # 第一次使用时执行
        DoMySQL.CreateCityAQI()
        cities = DoMySQL.SearchCities()
        for i in range(0, 30, 1):
            results = DoMySQL.SearchCityAQI(start_date.strftime('%Y-%m-%d'))
            for city in cities:
                self.level_dict[city[0]] = ''
            for res in results:
                self.level_dict[res[1]] = res[0]

            DoMySQL.StoreCityAQI(self.level_dict, start_date.strftime('%Y%m%d'))
            start_date += timedelta(1)

    def setCityAQILevel(self):
        """
        获取各城市AQI等级
        :return:
        """
        end_date = datetime.strptime(self.date, '%Y-%m-%d')
        start_date = end_date + timedelta(-29)
        # 第一次使用时执行
        DoMySQL.CreateCityAQILevel()
        cities = DoMySQL.SearchCities()
        for i in range(0, 30, 1):
            results = DoMySQL.SearchCityAQI(start_date.strftime('%Y-%m-%d'))
            for city in cities:
                self.level_dict[city[0]] = ''
            for res in results:
                # if res[1] not in self.level_dict:
                #     self.level_dict[res[1]] = ''
                if res[0] > 300:
                    level = 'F'
                elif res[0] > 200 and res[0] < 301:
                    level = 'E'
                elif res[0] > 150 and res[0] < 201:
                    level = 'D'
                elif res[0] > 100 and res[0] < 151:
                    level = 'C'
                elif res[0] > 50 and res[0] < 101:
                    level = 'B'
                elif res[0] > 0 and res[0] < 51:
                    level = 'A'
                else:
                    level = 'None'
                self.level_dict[res[1]] = level

            DoMySQL.StoreCityAQIlevel(self.level_dict, start_date.strftime('%Y%m%d'))
            start_date += timedelta(1)

    def CalCA(self):
        """
        计算相关矩阵
        :return:
        """
        cities = DoMySQL.SearchCities()
        X = []
        cov_dict ={}
        for city in cities:
            if city[0].encode('utf-8', 'ignore') in ('黔南州', '诸暨', '黄南州') :
                continue
            cov_dict[city[0].encode('utf-8', 'ignore')] = ""
            aqis = DoMySQL.SearchAQIbyCity(city[0])
            x = []
            for aqi in aqis[0][1:]:
                x.append(float(aqi))
            X.append(x)

        # X = np.array(X)
        results = np.corrcoef(X)
        return results

if __name__ == '__main__':
    c = CorrelationAna('2016-04-05')

    # 查询并创建各城市30天AQI等级
    # c.setCityAQILevel()

    # 查询并创建各城市30天AQI指数
    c.setCityAQI()
    # 根据各城市30天AQI指数计算城市间相关系数
    c.CalCA()