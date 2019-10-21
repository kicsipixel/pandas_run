import pandas as pd
from pandas import DataFrame
import numpy as np
import maya
import datetime
import matplotlib.ticker as tkr
import matplotlib.pyplot as plt

#import csv file
df = pd.read_csv('~/Downloads/szombat.csv')
# df_xls = pd.read_excel('~/Downloads/szombat.xlsx')

# remove special characters from columns' name
df.columns = df.columns.str.replace('/', '')

# get intervals for every km
km_array = []
row = 0
while row < df.shape[0]:
    if df.loc[row].DistanceMeters != 0.0 and df.loc[row].DistanceMeters % 1000 == 0:
        km_array.append(df.loc[row])
    row += 1

# when I started to run
start_time = maya.parse(df.loc[0].Time).datetime()
firstk_time = maya.parse(km_array[0].Time).datetime()

# x-axis
array_for_x_axis = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# y-axis
array_for_y_axis =[]
i = 0
while i < len(km_array):
    time_to_process = maya.parse(km_array[i].Time).datetime()
    if i == 0:
        array_for_y_axis.append((time_to_process - start_time).seconds)
    else:
        prev_km_time = maya.parse(km_array[i-1].Time).datetime()
        array_for_y_axis.append((time_to_process - prev_km_time).seconds)
    i += 1
    
# hearbeat
heart_beat = []
j = 0
while j < len(km_array):
    heart_beat.append(km_array[j].HeartRateBpmValue)
    j += 1
    

# data set for plotting
df = pd.DataFrame({'km': array_for_x_axis, 'min/km': array_for_y_axis, 'HRB': heart_beat})

# convert seconds to minutes
def func(x, pos):
    return str(datetime.timedelta(seconds=x))
fmt = tkr.FuncFormatter(func)

def convert_time(x):
    return str(datetime.timedelta(seconds=x))


ax = df.plot(x='km', y='min/km', kind = 'bar', rot = 0, color = '#4c4b63')
ax.axhline(y=360, linestyle='dashed', color='#949396')
ax.text(y=365, x=3, s='6 min', color='#949396')
ax.text(y=min(array_for_y_axis)+5, x=array_for_y_axis.index(min(array_for_y_axis))-0.5, s=convert_time(min(array_for_y_axis)), color='#5386e4')
ax.yaxis.set_major_formatter(fmt)
ax.get_children()[(array_for_y_axis.index(min(array_for_y_axis)))].set_color('#5386e4')
ax.get_legend().remove()

ax = df.plot(x='km', y='HRB', marker='o')
i = 1
for j in heart_beat:
    ax.text(y=j, x=i, s=j, color='#000000')
    i += 1
    
plt.show()