#!/usr/bin/python
# coding: utf-8

import MySQLdb
from Entity.PM25inFields import *



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
            db = MySQLdb.connect('localhost', 'dy', '', 'dydb', charset='utf8')
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
            db = MySQLdb.connect('localhost', 'dy', '', 'dydb', charset='utf8')
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


    @staticmethod
    def Search_LastitemTime(tablename):
        """
        返回str类型的数据库表最后一条item的time_point
        :param tablename: 表名
        :return:
        """
        try:
            # 打开数据库连接，设置charset为utf8，否则存入数据库时在workbench显示为乱码
            db = MySQLdb.connect('localhost', 'dy', '', 'dydb', charset='utf8')
        except MySQLdb.Error, e:
            print("Mysql Connect Error %d: %s" % (e.args[0], e.args[1]))
            return
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 创建数据表SQL语句
        sql = "SELECT time_point from " + tablename + " where test_info_id = (SELECT max(test_info_id) FROM " + tablename + ");"
        try:
            cursor.execute(sql)
        except MySQLdb.Error, e:
            # 出错时回滚
            print("Mysql Execute Error %d: %s" % (e.args[0], e.args[1]))
            db.rollback()
        # 获取所有记录列表
        result = cursor.fetchone()
        # for item in results:
        #     print str(item).decode("unicode_escape")
        try:
            # 关闭数据库连接
            db.close()
        except MySQLdb.Error, e:
            print("Mysql Close Error %d: %s" % (e.args[0], e.args[1]))
            return

        if result is None:
            return 'None'

        if result[0] is not None:
            return str(result[0])
        else:
            return 'None'


    @staticmethod
    def Search(sqlstatement):
        """
        按sql语句 进行查询
        :param sqlstatement: 查询语句

        :return:
        """
        try:
            # db = MySQLdb.connect('localhost', 'root', '', 'aqi_db', charset='utf8')
            db = MySQLdb.connect(host='joejoy.vicp.net', user='dy', passwd='', port=3306, db='dydb', charset='utf8')
        except MySQLdb.Error, e:
            print("Mysql Connect Error %d: %s" % (e.args[0], e.args[1]))
            return

        cursor = db.cursor()
        # 创建数据表SQL语句
        sql = sqlstatement
        try:
            cursor.execute(sql)
        except MySQLdb.Error, e:
            # 出错时回滚
            print("Mysql Execute Error %d: %s" % (e.args[0], e.args[1]))
            db.rollback()
        # 获取所有记录列表
        result = cursor.fetchall()
        # for item in results:
        #     print str(item).decode("unicode_escape")
        try:
            # 关闭数据库连接
            db.close()
        except MySQLdb.Error, e:
            print("Mysql Close Error %d: %s" % (e.args[0], e.args[1]))
            return

        if result is not None:
            return result
        else:
            return 'None'




    @staticmethod
    def SearchMonitors(city):
        """
        返回city的monitors
        :param city:
        :return:
        """
        try:
            db = MySQLdb.connect('localhost', 'root', '', 'aqi_db', charset='utf8')
        except MySQLdb.Error, e:
            print("Mysql Connect Error %d: %s" % (e.args[0], e.args[1]))
            return

        cursor = db.cursor()
        # 创建数据表SQL语句
        sql = "select distinct position_name from (select area,position_name from table33 where area = '" + city + "') table_p;"
        try:
            cursor.execute(sql)
        except MySQLdb.Error, e:
            # 出错时回滚
            print("Mysql Execute Error %d: %s" % (e.args[0], e.args[1]))
            db.rollback()
        # 获取所有记录列表
        result = cursor.fetchall()
        # for item in results:
        #     print str(item).decode("unicode_escape")
        try:
            # 关闭数据库连接
            db.close()
        except MySQLdb.Error, e:
            print("Mysql Close Error %d: %s" % (e.args[0], e.args[1]))
            return

        if result is not None:
            return result
        else:
            return 'None'



    @staticmethod
    def delete_huzhouData():
        """
        删除湖州的数据
        :return:
        """
        sqlstatement = "delete from table33 where area = '湖州'"
        try:
            # db = MySQLdb.connect('localhost', 'root', '', 'aqi_db', charset='utf8')
            db = MySQLdb.connect(host='joejoy.vicp.net', user='dy', passwd='', port=3306, db='dydb', charset='utf8')
        except MySQLdb.Error, e:
            print("Mysql Connect Error %d: %s" % (e.args[0], e.args[1]))
            return

        cursor = db.cursor()
        # 创建数据表SQL语句
        sql = sqlstatement
        try:
            cursor.execute(sql)
        except MySQLdb.Error, e:
            # 出错时回滚
            print("Mysql Execute Error %d: %s" % (e.args[0], e.args[1]))
            db.rollback()
        # 获取所有记录列表
        result = cursor.fetchall()
        # for item in results:
        #     print str(item).decode("unicode_escape")
        try:
            # 关闭数据库连接
            db.close()
        except MySQLdb.Error, e:
            print("Mysql Close Error %d: %s" % (e.args[0], e.args[1]))
            return

        if result is not None:
            return result
        else:
            return 'None'


if __name__ == '__main__':

    # db = PmMySQL_L()
    # db.CreateTable('table33')
    # SQLlasttime = db.Search_LastitemTime('table33')
    # if str(SQLlasttime) == '2016-03-04T13:00:00Z':
    #     print 'yes'
    PmMySQL_L.delete_huzhouData()
