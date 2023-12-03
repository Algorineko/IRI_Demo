import matplotlib.pyplot as plt
import iri2016
import numpy as np
from joblib import Parallel, delayed
import time
import iri2016.profile as iri
from datetime import datetime, timedelta
from matplotlib.pyplot import figure, show
import pandas as pd
iri2016.IRI('2020-12-31T00',(100, 1000, 10.0),80,120) #截止到2020-12-31
import math
def get_timeSeq(start_time, stop_time, interval_min):
    time_seq = []
    start = datetime.strptime(start_time, '%Y-%m-%d %H')
    end = datetime.strptime(stop_time, '%Y-%m-%d %H')
    time_interval = end - start
    minutes = (time_interval.seconds)/60 + time_interval.days*24*60
    tec_count = math.ceil(minutes/interval_min)
    print("tec_count = ", tec_count)
    delta = timedelta(minutes=interval_min)
    for i in range(tec_count):
        data = (start + delta*i).strftime('%Y-%m-%d %H')
        time_seq.append('{}T{}'.format(data[:-3], data[-2:]))
    return time_seq, tec_count
def cal_TEC(time_seq, high_range, lat_seq, lon_seq):
    print(time_seq[0], "====", time_seq[-1])
    start = time.time()
    result = Parallel(n_jobs=-20)(delayed(lambda t,h,lat,lon:iri2016.IRI(t,h,lat,lon).TEC.values[0])(time,high_range,i,j)for time in time_seq for i in lat_seq for j in lon_seq)
    end = time.time()
    print('{:.4f} s\n'.format(end-start))
    return result
start_time = '2011-01-04 00'
# start_time = '2017-04-21 00'
end_time = '2011-01-04 01'
interval_min = 60 #每小时监测一个tec
time_seq, tec_count = get_timeSeq(start_time, end_time, interval_min)

lat_seq = [lat for lat in range(-90,91,3)]
lon_seq = [lan for lan in range(-180,181,6)]
high_range = [100,1000,10000]
tec_result = cal_TEC(time_seq, high_range, lat_seq, lon_seq)
tec_result = np.array(tec_result).reshape(1, -1, 61)

print(tec_result)