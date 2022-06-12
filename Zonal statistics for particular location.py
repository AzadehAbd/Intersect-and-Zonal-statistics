# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 11:22:58 2022

@author: azade
"""
import geopandas as gpd
import rasterio 
import rasterstats 
import matplotlib.pyplot as plt
import pandas as pd 
import os 
import numpy as np 
from rasterstats import zonal_stats

village = gpd.read_file(r"D:/GitHub Uploads/Intersect-and-Zonal-statistics/villages2.shp")
village.plot()


#if you want to just do the work for some villages you need to check te number of the village 
#in te console section and convert it to pandas data franme 

Omuhonga_df = pd.DataFrame(village.loc[1]).transpose()
Omuhonga_point=gpd.GeoDataFrame(Omuhonga_df, geometry="geometry" )
#with the above line to separate the village from the rest and yop can plot it by Omuhonga_point.plot() in separeate map
 #you need to define the coordinate too 
Omuhonga_point.crs=village.crs
 
 
#you can do it with the same approach 
Omena_df = pd.DataFrame(village.loc[234]).transpose()
Omena_point=gpd.GeoDataFrame(Omena_df, geometry="geometry" )
Omena_point.crs=village.crs

# village.crs in the consle shhow you te coordinate system 


#create a empty pandas Dataframe to save the extracted data , its one to 5 becuase we have 4 raster file 
data = pd.DataFrame("", columns=["layer", "omena", "vomuhonga"], index= np.arange(1,5))



# reading the weather rasters from file and doing te zonal statistics during each ittration

i=1
for rast in os.listdir(r'D:/GitHub Uploads/Intersect-and-Zonal-statistics'):
    #only files that the last four digits are .tif
    if rast[-4:]==".tif":
        ras=rasterio.open('D:/GitHub Uploads/Intersect-and-Zonal-statistics' + "\\" + rast)
        rast_array=ras.read(1)
        affine=ras.transform
        
        #for omena
        aver_omena = zonal_stats(Omena_point, rast_array, 
                                                   affine=affine,
                                                   stats=["mean"],
                                                   geojason_out=True)
        
        aver_omena =aver_omena[0]["mean"]
        
        
        #for Omuhonga
        aver_Omuhonga= zonal_stats(Omuhonga_point, rast_array, 
                                                   affine=affine,
                                                   stats=["mean"],
                                                   geojason_out=True)
        
        aver_Omuhonga=aver_Omuhonga[0]["mean"]
        
        
        data.loc[i]["layer"]=rast[:-4]
        data.loc[i]["omena"]= aver_omena
        data.loc[i]["vomuhonga"]=aver_Omuhonga
        i=i+1
        
        print(rast)


fig, (ax1, ax2) = plt.subplots (2,1, figsize =(10,8))
data.plot(x="layer", y="omena", kind="bar", ax=ax1, title= "omeno")
data.plot(x="layer", y="vomuhonga", kind="bar", ax=ax2, title= "omeno")
plt.subplots_adjust(hspace= 0.8)
plt.show()




