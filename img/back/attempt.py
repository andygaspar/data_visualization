import data as dt

import matplotlib.patches as pt
from matplotlib.collections import PatchCollection
from shapely.geometry import LineString, MultiLineString
import matplotlib.pyplot as plt
from shapely.geometry import LinearRing, Polygon, MultiPolygon
import shapely.wkt
from descartes.patch import PolygonPatch
import numpy as np
import geopandas as geo
import geoplot

#sectors=dt.make_sectors()
#sectors_bound=dt.make_sectors_bound()
#sector_list=dt.get_sector_list()
#sector_bound_list=dt.get_sector_bound_list()





df=dt.make_df()
a=df["percentage"]
a.isinf().values.any()
for val in df["percentage"]:
    if np.isinf(val):
        print(val)
df["percentage"]
url="https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_land.geojson"
ooo=geo.read_file(url)

df.plot()
df.columns

df[df["geometry"]==None]
sectors.sort_values(["icao","minute_start"],inplace=True)
sectors.reset_index()

ax=ooo.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
df.plot(ax=ax,alpha=0.01,color="red",edgecolor="k")
ax.axis([-50,50,10,80])
#plot_sect(p)

df

d_test=df.iloc[400:1000].copy()
d_test["percentage"]=np.random.uniform(size=d_test.shape[0])
d_test
geoplot.choropleth(d_test,hue=d_test["percentage"])


help(geoplot.choropleth)
