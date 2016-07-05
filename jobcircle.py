__author__ = 'Tiago Gomes da Silva'
# -*- coding: UTF-8 -*-
import csv

# Open the earthquake data file.
filename = 'file_example.csv'

# Create empty lists for the data we are interested in.
lats, lons = [], []
gcarcs = []
statlats, statlons = [], []
stations = []

# Read through the entire file, skip the first line,
#  and pull out just the lats and lons.
with open(filename) as f:
    # Create a csv reader object.
    reader = csv.reader(f)

    # Ignore the header row.
    next(reader, 2)

    # Store the latitudes and longitudes in the appropriate lists.
    for row in reader:
        lats.append(float(row[1]))
        lons.append(float(row[2]))
        statlats.append(float(row[7]))
        statlons.append(float(row[8]))
        gcarcs.append(float(row[5]))
        stations.append(row[6])

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import pylab

#set map to Brazil coordinates

m = Basemap(projection='merc', epsg=4674, llcrnrlat=-35,urcrnrlat=10,\
            llcrnrlon=-81,urcrnrlon=-35,lat_0=-20,lon_0=-55, resolution='c')
m.drawstates(linewidth=0.25)
m.drawcountries(linewidth=1)
parallels = np.arange(-90,90,10)
m.drawparallels(parallels,labels=[True,True,True,False])
meridians = np.arange(-180.,180.,10)
m.drawmeridians(meridians,labels=[True,False,False,True])
m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 2000, verbose= True)
#m.etopo()

xs, ys = [],[]

for lon, lat, gcarc, stat, statlon, statlat in zip(lons, lats, gcarcs, stations, statlons, statlats):
    x,y = m(lon, lat) # coordenadas da estacao
    xs.append(x)
    ys.append(y)
    m.plot(x, y, 'v', markersize=10)
    plt.text(x+10000,y-100000,stat, fontsize=8 )

    m.tissot(lon, lat, gcarc/111.1,100,zorder=10,edgecolor='red',linewidth=0.6,facecolor='none')
    x,y = m(statlon, statlat)
    xs.append(x)
    ys.append(y)
    m.plot(x, y, '*', markersize=10)

m.plot(xs, ys, color='black', linewidth=0.5, label='Raio')# Plot the line station to event

#m.drawmapscale(-47.50, -33, 0, 0, 1000, barstyle='fancy', yoffset=20000)# drawmapscale

#plt.title("Evento 09\n")
plt.legend()
plt.savefig('job_mestrado2.png',dpi = 600)
plt.show()
