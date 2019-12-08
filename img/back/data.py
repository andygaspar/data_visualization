

import pandas as pd
import numpy as np

#import matplotlib.patches as pt
#from matplotlib.collections import PatchCollection
from shapely.geometry import LineString, MultiLineString
import matplotlib.pyplot as plt
from shapely.geometry import LinearRing, Polygon, MultiPolygon
import shapely.wkt
from descartes.patch import PolygonPatch
import numpy as np
import geopandas as geo
import geoplot
import copy




# data frames and sector list makers *****************************************+
def make_sectors():
    df=pd.read_csv("dati/sector_hours.csv")
    df.drop(columns=["id","id_capacities","minimum_tw","criterion","model","id.1","sector_hour"],inplace=True)
    columnsTitles=["icao","minute_start",	"minute_end", "capacity_utilization" ,"capacity"	,		"role"	,	"criticality_index"]
    df = df.reindex(columns=columnsTitles)
    return df[df["role"]=="E"]

def make_sectors_bound():
    df_bounds=pd.read_csv("dati/boundaries.csv")
    title=list(df_bounds.columns)
    title[4]="pol_bound"
    df_bounds.columns=title
    return df_bounds

def get_sector_list():
    sectors=make_sectors()
    return list(sectors["icao"].unique())


def get_sector_bound_list():
    sectors=make_sectors_bound()
    return list(sectors["icao"].unique())




def swap_xy(geom):
    if geom.is_empty:
        return geom

    if geom.has_z:
        def swap_xy_coords(coords):
            for x, y, z in coords:
                yield (y, x, z)
    else:
        def swap_xy_coords(coords):
            for x, y in coords:
                yield (y, x)

    # Process coordinates from each supported geometry type
    if geom.type in ('Point', 'LineString', 'LinearRing'):
        return type(geom)(list(swap_xy_coords(geom.coords)))

    elif geom.type == 'Polygon':
        ring = geom.exterior
        shell = type(ring)(list(swap_xy_coords(ring.coords)))
        holes = list(geom.interiors)
        for pos, ring in enumerate(holes):
            holes[pos] = type(ring)(list(swap_xy_coords(ring.coords)))
        return type(geom)(shell, holes)

    elif geom.type.startswith('Multi') or geom.type == 'GeometryCollection':
        # Recursive call
        return type(geom)([swap_xy(part) for part in geom.geoms])
    else:
        raise ValueError('Type %r not recognized' % geom.type)



def get_pol(df_local):
    pol=[]
    for i in range(df_local.shape[0]):
        pol.append(shapely.wkt.loads(df_local["pol_bound"].iloc[i]))
    return pol




def get_percentage(df_local):
    return (np.array(df_local["capacity_utilization"].values)/np.array(df_local["capacity"].values))



def get_sector_time(df,t):
    new_df=df.copy()
    new_df=new_df[new_df["minute_start"]<=t]
    new_df=new_df[new_df["minute_end"]>t]
    return new_df

#line_a = LineString([(0, 0), (1, 1)])



def plot_sect(pol):

    o=Polygon([(85,-200),(90,-200),(90,-150),(85,-150)])
    figsize=(15,10)

    # img = plt.imread("eu.png")
    # fig = plt.figure(1, figsize=figsize)
    # ax = fig.add_subplot(111)
    # ax.set_aspect(aspect=1.5)
    # ax.imshow(img,extent=[-50, 69, 28, 66])
    for i in range(len(pol)):
        try:
            fig = plt.figure(1, figsize=figsize)
            x,y=pol[i].exterior.coords.xy
            ax = fig.add_subplot(111)
            ax.fill(y,x,alpha=0.2)
        except:
            p_list=list(pol[i])
            for pl in p_list:
                if not o.contains(pl):
                    fig = plt.figure(1, figsize=figsize)
                    x,y=pl.exterior.coords.xy
                    ax = fig.add_subplot(111)
                    ax.fill(y,x,alpha=0.2)

def unify_pol(pol):
    uni=pol[0]
    for p in pol[1:]:
        uni=uni.union(p)
    return uni





def make_df():
    df_bounds=make_sectors_bound()
    df=make_sectors()
    df.sort_values(["icao","minute_start"],inplace=True)
    df.reset_index()
    sector_list=get_sector_list()
    sector_list.sort()
    new_pol=[]
    b=[]

    for sec in sector_list:
        sector=df_bounds[df_bounds["icao"]==sec]
        pol=unify_pol(get_pol(sector))
        for i in range(df[df["icao"]==sec].shape[0]):
            new_pol.append(pol)
        b.append(pol)
    n=new_pol
    new_pol=geo.GeoSeries(new_pol)
    df["geometry"]
    for i in range(len(new_pol)):
        df["geometry"].iloc[i]=new_pol[i]#.geometry.map(swap_xy)
    df["percentage"]=get_percentage(df)
    columnsTitles=['icao', 'minute_start', 'minute_end', 'percentage', 'capacity_utilization','capacity', 'role', 'criticality_index', 'geometry']
    df = df.reindex(columns=columnsTitles)
    return n,b,geo.GeoDataFrame(df)



len(n)
df.shape
#df.shape
n,b,df=make_df()
m=geo.GeoSeries(n.copy())
n[290:300]
n[300]
m[300]
df["geometry"]=m
df["geometry"].iloc[300]=m[300]

for i in range(len(m)):
    df["geometry"].iloc[i]=m[i]

df.iloc[300]
b=geo.GeoSeries(b)
b
b=geo.GeoDataFrame(b)

b.columns=["geometry"]
b
b["geometry"]=b.geometry.map(swap_xy)
b
b["percentage"]=np.random.uniform(size=b.shape[0])
b
d_test=df.iloc[290:300].copy()
d_test
df_back=df.copy()
df_back

df=df.geometry.map(swap_xy)
df.columns=["geometry"]
df_back["geometry"]=df




df=df_back.copy()




url="https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_land.geojson"
world=geo.read_file(url)


for i in range(20):
    dt_hour=get_sector_time(df,500+i*20)

    ax=geoplot.choropleth(dt_hour,hue=dt_hour["percentage"],cmap='Blues',alpha=0.5,linewidth=0)
    world.plot(ax=ax,color="grey",figsize=(15,12),alpha=0.5)
    plt.savefig(str(i)+".png")

help(geoplot.choropleth)
