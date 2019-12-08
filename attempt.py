import data as dt
import color_map as cm
import matplotlib.patches as pt
from matplotlib.collections import PatchCollection
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
from shapely.geometry import LineString, MultiLineString
import matplotlib.pyplot as plt
from shapely.geometry import LinearRing, Polygon, MultiPolygon
import shapely.wkt
from descartes.patch import PolygonPatch
import numpy as np
import geopandas as geo
import geoplot
import copy
import scipy.interpolate as sc
import pandas as pd



time_step=1
def hour(h,m=0):
    return int((h*60+m)/time_step)
def hour_end(h,m=0):
    return int((h*60+m)/time_step)+1
def get_hour(i):
    time=i*time_step
    return str(int(time/60))+"_"+str(time%60)




#percentage_mat=np.loadtxt("dati/per_mat.csv",delimiter=",")
#percentage_mat_one=np.loadtxt("dati/per_mat_one.csv",delimiter=",")

df_geo=dt.load_geodf("dati/df_geo.csv")
df_geo_one=dt.load_geodf("dati/df_geo_one.csv")





url="https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_land.geojson"
world=geo.read_file(url)

percentage_mat=dt.make_percentage_mat(1)
percentage_mat_one=dt.make_percentage_mat_one(1)

import matplotlib
matplotlib.use('Agg')
figsize=(20,10)
for i in range(hour(10),hour_end(10,15)):
    ax=geoplot.choropleth(df_geo_one,hue=percentage_mat_one[:,i],cmap="autumn",linewidth=0,legend=True,figsize=figsize)
    geoplot.polyplot(world,ax=ax,color="lightblue",extent=[-30,23, 47, 75])
    plt.savefig("img/"+get_hour(i)+".jpg")




df_geo.plot(color="blue")


help(colormap)



i=400
figsize=(20,10)
ax=geoplot.choropleth(df_geo,hue=percentage_mat[:,i],cmap=mia,linewidth=0,legend=True,figsize=figsize)
geoplot.polyplot(world,ax=ax,color="lightblue",extent=[-30,23, 47, 75])





# *******************
data1 = np.random.random((4,4))
yel_red= {'red':
                ((0.0,  0, 0),\
                (0.5, 0.9, 0.9),\
                (0.75, 0.8, 0.8),\
                (0.95, 1.0, 1.0),\
                (1.0, 1, 1.0)),\
        'green':\
                ((0.0, 0.5, 0.5),\
                (0.25, 0.8, 0.8),\
                   (0.5, 0.1, 0.1),
                   (0.75, 0.1,0.1),
                   (1.0, 0,0)),
         'blue':  ((0.0, 1, 1),
                   (0.25, 0.8, 0.8),
                   (0.5, 0.1, 0.1),
                   (0.75, 0.1,0.1),
                   (1.0, 0.0, 0.0)),
        'alpha': ((0, 1, 1),
                   (0.02,0, 0),
                    (0.5,0, 0),
                   (0.98,0, 0),
                    (1.0, 0, 0)),
          }
yr = LinearSegmentedColormap('mia', yel_red)
plt.register_cmap(cmap=yr)
plt.pcolormesh(data1, cmap=yr)
plt.colorbar()

for i in range(hour(12,30),hour_end(12,30)):
    ax=geoplot.choropleth(df_geo_one,hue=percentage_mat_one[:,i],cmap=cm.mia,linewidth=0,figsize=figsize,legend=True)
    geoplot.polyplot(world,ax=ax,color="#ccd9ff",extent=[-3,35, 40, 50])


np.mean(percentage_mat[:,i])


plt.plot(percentage_mat[:,i])




w=np.array([280,90,80,65,60,50,25,22,20,12])
sat=np.array([i for i in range(10,0,-1)])
x=np.flip(w)
sat
plt.bar(np.flip(w)+2,sat,width=w)
