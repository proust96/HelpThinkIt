import xarray as xr
import math
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

xdss = xr.open_dataset("HELSINKI_100x100m_7d.nc4", decode_times=False)
xds = xdss.head(288) #one day

var = "fmi_pm2p5"

def printNice(tab):
    s = [[str(e) for e in row] for row in tab]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))

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

def toCelcius(nb):
    return nb-273

def calculateArray():
    for lat in range(START_LAT, END_LAT):
        for lon in range(START_LON, END_LON):
            means[lat-START_LAT][lon-START_LON] = validNb(getMean(xds.lat.values[lat],xds.lon.values[lon]),0.01)

START_LAT=0
START_LON=0

SIZE_LAT=164 #164
SIZE_LON=127 #127

END_LAT=START_LAT+SIZE_LAT
END_LON=START_LON+SIZE_LON

means=[[0]*SIZE_LON for i in range(SIZE_LAT)]


calculateArray()
#printNice(means)
displayHeatMap(means)

#print(xds)

