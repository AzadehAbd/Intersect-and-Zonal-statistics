# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 10:22:14 2022

@author: azade
"""


import geopandas as gpd
import rasterio 
import rasterstats
from rasterio.plot import show

#read the district shapefile

village = gpd.read_file(r"D:/GitHub Uploads/Intersect-and-Zonal-statistics/villages2.shp")

#village.plot()

#importing the rasters

rf=rasterio.open(r"D:/GitHub Uploads/Intersect-and-Zonal-statistics/mprec_2019.tif", mode= "r")

#show(rf)

#plotting the raster and shhape file togetherdata
import matplotlib.pyplot as plt
from rasterio.plot import show_hist

fig, (ax1, ax2) =plt.subplots(1,2, figsize=(10,4))
show(rf, ax=ax1, title ="Precipitaion 2019")
village.plot(ax=ax1, facecolor="none", edgecolor ="red")
show_hist(rf, title= "Histogram", ax=ax2)
plt.show()

#Assign raster values to a numpy nd array

prec2011_array= rf.read(1)
affine = rf.transform

#calculating the zonal statistics
statdes_rf=rasterstats.zonal_stats(village,prec2011_array, affine=affine,
                                   stats= ["mean", "min", "max"],
                                   geojson_out= True)


# Extraction the needed data from list 
#first create an empty list

statdscrptiv =[]
i= 0

while i < len(statdes_rf):
    statdscrptiv.append(statdes_rf[i]["properties"])
    i = i+1
    
#convert data from list to pandas data frame 
import pandas as pd

stat_rf=pd.DataFrame(statdscrptiv)
print(stat_rf)


stat_rf.plot(x= "max", y="mean", kind="scatter", title= "Precipitation 2019")



    