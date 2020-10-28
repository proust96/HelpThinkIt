import xarray as xr
import math
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

xdss = xr.open_dataset("HELSINKI_100x100m_7d.nc4", decode_times=False)
xds = xdss.head(288) #one day

var = "megasense_o3"

def getMean(latN, lonN):
    cell = xds.loc[dict(lat=latN, lon=lonN)]
    df = cell[var].to_dataframe()
    return df[df[var] != 0][var].mean()

def displayHeatMap(tab):
    a = np.array(tab)
    plt.imshow(a, cmap='hot', interpolation='nearest')
    plt.show()

def validNb(nb, limit):
    if nb < limit:
        return limit
    return nb

def toScaleO3(nb):
    if math.isnan(nb):
        return 0
    if nb>200:
        return 1
    if nb>100:
        return 0.5
    if nb>20:
        return -0.5
    return -1

def calculateArray():
    for lat in range(START_LAT, END_LAT):
        for lon in range(START_LON, END_LON):
            means[END_LAT-lat-1][lon-START_LON] = toScaleO3(getMean(xds.lat.values[lat],xds.lon.values[lon]))

START_LAT=0
START_LON=0

SIZE_LAT=164 #164
SIZE_LON=127 #127

END_LAT=START_LAT+SIZE_LAT
END_LON=START_LON+SIZE_LON

means=[[0]*SIZE_LON for i in range(SIZE_LAT)]

calculateArray()
displayHeatMap(means)


