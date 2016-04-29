#!/usr/bin/env_python
#encoding: utf-8

import numpy as np
import pylab as pl
from StringIO import StringIO

data_str = """

2012-04-01_02 68
2012-04-01_05 70
2012-04-01_08 69
2012-04-01_11 71
2012-04-01_14 72
2012-04-01_20 70
2012-04-02_02 71
2012-04-02_05 70
2012-04-02_08 69
2012-04-02_11 71

2012-04-02_14 69

2012-04-02_20 71

2012-04-03_02 74

2012-04-03_05 73

2012-04-03_08 77

2012-04-03_11 70

2012-04-03_14 71

2012-04-03_20 70
2012-04-04_02 70

2012-04-04_05 72
2012-04-04_08 72

2012-04-04_11 69

2012-04-04_14 71

2012-04-04_20 69

2012-04-07_02 75

"""

data = np.loadtxt(StringIO(data_str), dtype=np.dtype([("t", "S13"),("v", float)]))

datestr = np.char.replace(data["t"], "_", " ")

t = pl.datestr2num(datestr)

v = data["v"]

pl.plot_date(t, v, fmt="-o")

pl.subplots_adjust(bottom=0.3)

ax = pl.gca()
ax.fmt_xdata = pl.DateFormatter('%Y-%m-%d %H:%M:%S')

pl.xticks(rotation=90)
# pl.xticks(t, datestr) # 如果以数据点为刻度，则注释掉这一行

ax.xaxis.set_major_formatter(pl.DateFormatter('%Y-%m-%d %H:%M'))

pl.grid()
pl.show()