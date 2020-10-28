import xarray as xr
import math
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

xdss = xr.open_dataset("HELSINKI_100x100m_7d.nc4", decode_times=False)
xds = xdss.head(288) #first day


def getMean(latN, lonN, var):
    cell = xds.loc[dict(lat=latN, lon=lonN)]
    df = cell[var].to_dataframe()
    return df[df[var] != 0][var].mean()

def displayHeatMap(tab):
    a = np.array(tab)
    plt.imshow(a, cmap='hot', interpolation='nearest')
    plt.show()

def toScaleAQI(nb):
    if math.isnan(nb):
        return 0
    if nb>4:
        return 1
    if nb>3:
        return 0.5
    if nb>2:
        return -0.5
    return -1

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

def toScale(var, values, nb):
    for i in range(len(values)):
        if nb>values[i]:
            return len(values)-i+1
    return 1

def calculateArray():
    dic={}
    dicNb=0
    for lat in range(START_LAT, END_LAT):
        for lon in range(START_LON, END_LON):
            no = toScale("no",[2.5,2,1.5,1,0.7,0.5,0.3],getMean(xds.lat.values[lat],xds.lon.values[lon],"fmi_no"))
            no2 = toScale("no2",[3,2.5,2,1.5,1,0.7,0.5],getMean(xds.lat.values[lat],xds.lon.values[lon],"fmi_no2"))
            pm10 = toScale("pm10",[13,11,9,7,5,3,2,1],getMean(xds.lat.values[lat],xds.lon.values[lon],"fmi_pm10p0"))
            pm2 = toScale("pm2",[3,2.5,2,1.5,1,0.7,0.5,0.3],getMean(xds.lat.values[lat],xds.lon.values[lon],"fmi_pm2p5"))
            so = toScale("so",[0.27,0.23,0.2,0.16,0.12,0.08,0.05],getMean(xds.lat.values[lat],xds.lon.values[lon],"fmi_so2"))
            aqi = toScaleAQI(getMean(xds.lat.values[lat],xds.lon.values[lon],"megasense_aqi"))
            o3 = toScaleO3(getMean(xds.lat.values[lat],xds.lon.values[lon],"megasense_o3"))
            means[END_LAT-lat-1][lon-START_LON] = no+no2+pm10+pm2+so+aqi+o3
            concat = str(no)+str(no2)+str(pm10)+str(pm2)+str(so)
            if concat in dic:
                concats[END_LAT-lat-1][lon-START_LON] = dic[concat]
            else:
                dicNb+=1
                dic[concat] = dicNb
                concats[END_LAT-lat-1][lon-START_LON] = dic[concat]


START_LAT=0
START_LON=0

SIZE_LAT=164 #164
SIZE_LON=127 #127

END_LAT=START_LAT+SIZE_LAT
END_LON=START_LON+SIZE_LON

means=[[0]*SIZE_LON for i in range(SIZE_LAT)]
concats=[[0]*SIZE_LON for i in range(SIZE_LAT)] #used for component labelling


calculateArray()
displayHeatMap(means)

