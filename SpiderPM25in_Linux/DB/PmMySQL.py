#!/usr/bin/python
# coding: utf-8

import MySQLdb



class PmMySQL_L(object):
    """
    将数据存入本地数据库
    """

    @staticmethod
    def CreateTable(tableName):
        """
        :param tableName: 表名
        :return:
        """
        try:
            db = MySQLdb.connect('localhost', 'root', '123456', 'DYBD', charset='utf8')
        except MySQLdb.Error, e:
            print "Mysql Connect Error %d: %s" % (e.args[0], e.args[1])
            return

        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS " + tableName)
        sql = """CREATE TABLE """ + tableName + """ (
              test_info_id INT NOT NULL AUTO_INCREMENT COMMENT '',
              aqi INT(5) NOT NULL COMMENT '',
              area VARCHAR(50) NOT NULL COMMENT '',
              co VARCHAR(5) NOT NULL COMMENT '',
              co_24h VARCHAR(7) NOT NULL COMMENT '',
              no2 INT(5) NOT NULL COMMENT '',
              no2_24h INT(5) NOT NULL COMMENT '',
              o3 INT(5) NOT NULL COMMENT '',
              o3_24h INT(5) NOT NULL COMMENT '',
              o3_8h INT(5) NOT NULL COMMENT '',
              o3_8h_24h INT(5) NOT NULL COMMENT '',
              pm10 INT(5) NOT NULL COMMENT '',
              pm10_24h INT(5) NOT NULL COMMENT '',
              pm2_5 INT(5) NOT NULL COMMENT '',
              pm2_5_24h INT(5) NOT NULL COMMENT '',
              position_name VARCHAR(50) NOT NULL COMMENT '',
              primary_pollutant VARCHAR(50) NOT NULL COMMENT '',
              quality VARCHAR(10) NOT NULL COMMENT '',
              so2 INT(5) NOT NULL COMMENT '',
              so2_24h INT(5) NOT NULL COMMENT '',
              station_code VARCHAR(10) NOT NULL COMMENT '',
              time_point VARCHAR(30) NOT NULL COMMENT '',
              PRIMARY KEY (test_info_id)  COMMENT '')
            ENGINE = InnoDB
            DEFAULT CHARACTER SET = utf8;"""
        cursor.execute(sql)
        try:
            # 关闭数据库
            db.close()
        except MySQLdb.Error, e:
            print "Mysql Close Error %d: %s" % (e.args[0], e.args[1])
            return





    @staticmethod
    def InsertItem(tableName, item):
        """

        :param tableName: 表名
        :param item: PM25inFields对象
        :return:
        """

        try:
            # 打开数据库连接，设置charset为utf8，否则存入数据库时在workbench显示为乱码
            db = MySQLdb.connect('localhost', 'root', '123456', 'DYBD', charset='utf8')
        except MySQLdb.Error, e:
            print("Mysql Connect Error %d: %s" % (e.args[0], e.args[1]))
            return
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 创建数据表SQL语句
        sql = "INSERT INTO " + tableName + " (aqi, area, co, co_24h, no2, no2_24h, o3, o3_24h, o3_8h, " \
                                           "o3_8h_24h, pm10, pm10_24h, pm2_5, pm2_5_24h, position_name, " \
                                           "primary_pollutant, quality, so2, so2_24h, station_code, time_point)"\
              + " VALUES (" + str(item.aqi) +",'"+ str(item.area) +"',"+ str(item.co) +","+ str(item.co_24h)\
              +","+ str(item.no2) +","+ str(item.no2_24h) +","+ str(item.o3) +","+ str(item.o3_24h)\
              +","+ str(item.o3_8h) +","+ str(item.o3_8h_24h) +","+ str(item.pm10) +","+ str(item.pm10_24h)\
              +","+ str(item.pm2_5) +","+ str(item.pm2_5_24h) +",'"+ str(item.position_name)\
              +"','"+ str(item.primary_pollutant) +"','"+ str(item.quality) +"',"+ str(item.so2)\
              +","+ str(item.so2_24h) +",'"+ str(item.station_code) +"','"+ item.time_point +"')"
        try:
            # 使用execute方法执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except MySQLdb.Error, e:
            # 出错时回滚
            print("Mysql Execute Error %d: %s" % (e.args[0], e.args[1]))
            db.rollback()
        try:
            # 关闭数据库连接
            db.close()
        except MySQLdb.Error, e:
            print("Mysql Close Error %d: %s" % (e.args[0], e.args[1]))
            return



if __name__ == '__main__':

    db = PmMySQL_L()
    db.CreateTable('table33')