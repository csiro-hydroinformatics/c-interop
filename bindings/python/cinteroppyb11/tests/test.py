import cinteroppyb11 as c
import numpy as np

d = c.DateTimeToSecond()
c.test_date_time_to_second(d, 0.0, 0, 0, 0, 0, 0)

d = c.DateTimeToSecond()
d.year = 2000
d.month = 1
d.day = 1

mts = c.MultiRegularTimeSeries()
mts.clear_numeric_data()
mts.ensemble_size = 1

n = 365
geom = c.RegularTimeSeriesGeometry()
geom.length = n
geom.start = d
geom.time_step_seconds = 86400

mts.time_series_geometry = geom

x = np.random.normal(size=n)
mts.set_numeric_data([x])
