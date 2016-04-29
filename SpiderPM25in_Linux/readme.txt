/data:（已无用）
CityID.txt：	heweather上抓取的city details
pm25in_cityInfo.txt：	pm25.in的cityname和url地址对应表（要访问需要在前面添加pm25.in的homeUrl）


/DB：
PmMySQL.py:
class PmMySQL_L暂时有两个静态函数，createTable和InsertItem，注意修改数据库名表名等。


/Entity:
PM25inFields.py: 用一个classPM25inFields来接住API返回的一条item里的所有字段，详情见__init__。


/Util:
SpiderPm25in_key.py: 
通过网站提供的API获取全国300个城市的所有监测点的实时数据（API就是self.aqiUrl，一个小时只能用5次）。每个城市有多个监测点（如上海有普陀，浦东川沙等十个监测点）。该类的目的就是获取全国所有检测点

API返回的并不是一个严格的json，而是一个list：API返回的并不是一个严格的json，而是一个list：[{},{},{},{}],每一个字典是一个监测点的数据。

DrawCityPm25.py是画图代码

/Forecast:
这个模块是预测分析模块




