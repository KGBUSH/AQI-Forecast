#!/usr/bin/python
# coding: utf-8

import MySQLdb

class DoMySQL(object):
    """
    将数据存入本地数据库
    """

    @staticmethod
    def ConnectDB():
        """
        连接数据库
        :return:
        """
        # 连接数据库
        try:
            db = MySQLdb.connect('localhost', 'root', '', 'dydb', charset='utf8')
        except MySQLdb.Error, e:
            print "Mysql Connect Error %d: %s" % (e.args[0], e.args[1])
            return
        return db

    @staticmethod
    def CloseDB(db):
        """
        关闭数据库连接
        :return:
        """
        # 关闭数据库连接
        try:
            db.commit()
            db.close()
        except MySQLdb.Error, e:
            print("Mysql Close Error %d: %s" % (e.args[0], e.args[1]))
            return

    @staticmethod
    def SelectSQL(db, sql):
        """
        查询sql语句
        :param sql: 执行的sql语句
        :return:
        """
        cursor = db.cursor()
        # 执行sql语句
        try:
            cursor.execute(sql)
        except MySQLdb.Error, e:
            # 出错时回滚
            print("Mysql Execute Error %d: %s" % (e.args[0], e.args[1]))
            db.rollback()
        # 获取所有记录列表
        result = cursor.fetchall()

        if result is not None:
            return result
        else:
            return 'None'

    @staticmethod
    def CreateTableSQL(db, tablename):
        """
        新建表格
        :param sql: 执行的sql语句
        :return:
        """
        cursor = db.cursor()
        # 创建数据表
        sql = "create table if not exists " + tablename + "(city varchar(50));"
        try:
            cursor.execute(sql)
        except MySQLdb.Error, e:
            # 出错时回滚
            print("Mysql Execute Error %d: %s" % (e.args[0], e.args[1]))
            db.rollback()

    @staticmethod
    def AlterDataSQL(db, sql):
        """
        插入或修改数据
        :param sql: 执行的sql语句
        :return:
        """
        cursor = db.cursor()
        # 执行语句
        try:
            cursor.execute(sql)
        except MySQLdb.Error, e:
            # 出错时回滚
            print("Mysql Execute Error %d: %s" % (e.args[0], e.args[1]))
            db.rollback()

    @staticmethod
    def SearchCities():
        """
        返回所有城市
        :return:
        """
        db = DoMySQL.ConnectDB()
        # 查询数据表SQL语句
        sql = "select distinct area from table33;"
        results = DoMySQL.SelectSQL(db, sql)
        DoMySQL.CloseDB(db)
        return results

    @staticmethod
    def CreateCityAQI():
        db = DoMySQL.ConnectDB()
        # 创建city_aqi数据表
        DoMySQL.CreateTableSQL(db, 'city_aqi')
        # 插入城市数据
        cities = DoMySQL.SearchCities()
        for city in cities:
            sql = "insert into city_aqi values('" + city[0] + "');"
            DoMySQL.AlterDataSQL(db, sql)
        DoMySQL.CloseDB(db)

    @staticmethod
    def CreateCityAQILevel():
        db = DoMySQL.ConnectDB()
        # 创建city_aqi_level数据表
        DoMySQL.CreateTableSQL(db, 'city_aqi_level')
        # 插入城市数据
        cities = DoMySQL.SearchCities()
        for city in cities:
            sql = "insert into city_aqi_level values('" + city[0] + "');"
            DoMySQL.AlterDataSQL(db, sql)
        DoMySQL.CloseDB(db)

    @staticmethod
    def SearchCityAQI(date):
        """
        返回所有城市该日期的AQI指数
        :param date:
        :return:
        """
        db = DoMySQL.ConnectDB()
        # 查询数据表SQL语句
        sql = "select sum(aqi)/count(*) as ave_aqi, area from table33 where time_point like '" + date + "%' group by area;"
        results = DoMySQL.SelectSQL(db, sql)
        DoMySQL.CloseDB(db)
        return results

    @staticmethod
    def SearchAQIbyCity(city):
        """
        返回该城市所有日期的AQI指数
        :param date:
        :return:
        """
        db = DoMySQL.ConnectDB()
        # 查询数据表SQL语句
        sql = "SELECT * FROM dydb.city_aqi where city = '" + city + "';"
        results = DoMySQL.SelectSQL(db, sql)
        DoMySQL.CloseDB(db)
        return results

    @staticmethod
    def StoreCityAQI(level_dict, date):
        """
        将各城市的AQI指数存入数据库
        :param level_dict:
        :param date:该日期之前的30天的AQI数据（包含该日期）
        :return
        """
        db = DoMySQL.ConnectDB()
        # 添加日期字段
        sql = "alter table city_aqi add column d" + date + " varchar(30);"
        DoMySQL.AlterDataSQL(db, sql)
        # 添加各日期AQI指数
        for key, value in enumerate(level_dict):
            sql = "update city_aqi set d" + date + " = '" + str(level_dict[value]) + "' where city = '" + value + "';"
            DoMySQL.AlterDataSQL(db, sql)
        DoMySQL.CloseDB(db)

    @staticmethod
    def StoreCityAQIlevel(level_dict, date):
        """
        将各城市的AQI等级存入数据库
        :param level_dict:
        :param date:该日期之前的30天的AQI数据（包含该日期）
        :return
        """
        db = DoMySQL.ConnectDB()
        # 添加日期字段
        sql = "alter table city_aqi_level add column d" + date + " varchar(30);"
        DoMySQL.AlterDataSQL(db, sql)
        # 添加各日期AQI指数
        for key, value in enumerate(level_dict):
            sql = "update city_aqi_level set d" + date + " = '" + level_dict[value] + "' where city = '" + value + "';"
            DoMySQL.AlterDataSQL(db, sql)
        DoMySQL.CloseDB(db)