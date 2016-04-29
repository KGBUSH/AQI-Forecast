#!/usr/bin/python
# coding: utf-8

class PM25inFields(object):
    """
    PM25.in的API涉及到的数据字段
    """

    def __init__(self, aqi, area, co, co_24h, no2, no2_24h, o3, o3_24h,
                 o3_8h, o3_8h_24h, pm10, pm10_24h, pm2_5, pm2_5_24h,
                 position_name, primary_pollutant, quality, so2, so2_24h, station_code, time_point):
        """
        :param aqi	空气质量指数(AQI)，即air quality index，是定量描述空气质量状况的无纲量指数
        :param area	城市名称
        :param position_name	监测点名称
        :param station_code	监测点编码
        :param so2	二氧化硫1小时平均
        :param so2_24h	二氧化硫24小时滑动平均
        :param no2	二氧化氮1小时平均
        :param no2_24h	二氧化氮24小时滑动平均
        :param pm10	颗粒物（粒径小于等于10μm）1小时平均
        :param pm10_24h	颗粒物（粒径小于等于10μm）24小时滑动平均
        :param co	一氧化碳1小时平均
        :param co_24h	一氧化碳24小时滑动平均
        :param o3	臭氧1小时平均
        :param o3_24h	臭氧日最大1小时平均
        :param o3_8h	臭氧8小时滑动平均
        :param o3_8h_24h	臭氧日最大8小时滑动平均
        :param pm2_5	颗粒物（粒径小于等于2.5μm）1小时平均
        :param pm2_5_24h	颗粒物（粒径小于等于2.5μm）24小时滑动平均
        :param primary_pollutant	首要污染物
        :param quality	空气质量指数类别，有“优、良、轻度污染、中度污染、重度污染、严重污染”6类
        :param time_point	数据发布的时间

        :return:
        """

        self.aqi = aqi
        self.area = area
        self.co = co
        self.co_24h = co_24h
        self.no2 = no2
        self.no2_24h = no2_24h
        self.o3 = o3
        self.o3_24h = o3_24h
        self.o3_8h = o3_8h
        self.o3_8h_24h = o3_8h_24h
        self.pm10 = pm10
        self.pm10_24h = pm10_24h
        self.pm2_5 = pm2_5
        self.pm2_5_24h = pm2_5_24h
        self.position_name = position_name
        self.primary_pollutant = primary_pollutant
        self.quality = quality
        self.so2 = so2
        self.so2_24h = so2_24h
        self.station_code = station_code
        self.time_point = time_point



