# coding: utf-8


class AirIndicators(object):

    def __init__(self, citychinese, monitor, aqi, qualitylevel, pm2_5,
                 pm10, co, no2, o3, o3_8h, so2, updatetime, advice):
        self.cityChinese = citychinese
        self.monitor = monitor

        self.aqi = aqi
        self.qualityLevel = qualitylevel
        self.pm2_5 = pm2_5
        self.pm10 = pm10
        self.co = co
        self.no2 = no2
        self.o3 = o3
        self.o3_8h = o3_8h
        self.so2 = so2

        self.updateTime = updatetime
        self.numericSymbols = 'μg/m3'
        self.advice = advice
