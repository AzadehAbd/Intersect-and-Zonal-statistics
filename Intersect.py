# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 16:19:13 2022

@author: azade
"""

import geopandas as gpd
import rasterio as rio
import rasterstats 
import os


village = gpd.read_file(r"D:/GitHub Uploads/Intersect-and-Zonal-statistics/villages2.shp")

village ["mprec_2018"]=0

for index, row in village.iterrows():
    city= row["Village_na"]
    longitude =row["geometry"].x
    latitide =row["geometry"].y
    
    prec2011_ras=rio.open(r'D:/GitHub Uploads/Intersect-and-Zonal-statistics/mprec_2018.tif')
    prec2011_data=prec2011_ras.read(1)
    rowIndex, colIndex =prec2011_ras.index(longitude, latitide)
    
    print(city + "    " + str(prec2011_data[rowIndex, colIndex]))
    
    village["mprec_2018"].loc[index] = str(prec2011_data[rowIndex, colIndex])

village= village[["Village_na","mprec_2018",]]

village.to_csv("villages with mprec_2018")