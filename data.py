

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
import scipy.interpolate as sc




# data frames and sector list makers *****************************************+


def get_percentage(df_local):
    return (np.array(df_local["capacity_utilization"].values)/np.array(df_local["capacity"].values))




def make_sectors():
    df=pd.read_csv("dati/sector_hours.csv")
    df.drop(columns=["id","id_capacities","minimum_tw","criterion","model","id.1","sector_hour"],inplace=True)
    df["percentage"]=get_percentage(df)
    columnsTitles=['icao', 'minute_start', 'minute_end', 'percentage', 'capacity_utilization','capacity', 'role', 'criticality_index']
    df = df.reindex(columns=columnsTitles)
    df.sort_values(["icao","minute_start"],inplace=True)
    return df[df["role"]=="E"]

def make_sectors_bound():
    df_bounds=pd.read_csv("dati/boundaries.csv")
    title=list(df_bounds.columns)
    title[4]="pol_bound"
    df_bounds.columns=title
    df_bounds.sort_values(["icao"],inplace=True)
    return df_bounds

def get_sector_list():
    sectors=make_sectors()
    sector_list=list(sectors["icao"].unique())
    sector_list.sort()
    return sector_list

def get_sector_bound_list():
    sectors=make_sectors_bound()
    sector_list=list(sectors["icao"].unique())
    sector_list.sort()
    return sector_list



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





def pre_make_df():
    df_bounds=make_sectors_bound()
    df=make_sectors()
    df.sort_values(["icao","minute_start"],inplace=True)
    df.reset_index()
    sector_list=get_sector_list()
    sector_list.sort()
    new_pol=[]

    for sec in sector_list:
        sector=df_bounds[df_bounds["icao"]==sec]
        pol=unify_pol(get_pol(sector))
        for i in range(df[df["icao"]==sec].shape[0]):
            new_pol.append(pol)
    n=new_pol
    new_pol=geo.GeoDataFrame(geo.GeoSeries(new_pol))
    new_pol.columns=["geometry"]
    new_pol=(new_pol.geometry.map(swap_xy)).copy()
    df["geometry"]=new_pol
    df["percentage"]=get_percentage(df)
    columnsTitles=['icao', 'minute_start', 'minute_end', 'percentage', 'capacity_utilization','capacity', 'role', 'criticality_index', 'geometry']
    df = df.reindex(columns=columnsTitles)
    return new_pol,geo.GeoDataFrame(df)

def swap(n):
    return (n.geometry.map(swap_xy)).copy()

def make_df():
    n,dff=pre_make_df()
    for i in range(len(n)):
        dff["geometry"].iloc[i]=n[i]
    return dff





def df_geo():
    df_bounds=make_sectors_bound()
    sector_list=get_sector_list()
    df=geo.GeoDataFrame({"icao":sector_list})
    new_pol=[]

    for sec in sector_list:
        sector=df_bounds[df_bounds["icao"]==sec]
        pol=unify_pol(get_pol(sector))
        new_pol.append(pol)

    new_pol=geo.GeoDataFrame(geo.GeoSeries(new_pol))
    new_pol.columns=["geometry"]
    new_pol=(new_pol.geometry.map(swap_xy))
    df["geometry"]=new_pol
    df.sort_values(["icao"],inplace=True)
    return df








def get_sector_time_pre(df,t):
    new_df=df.copy()
    new_df=new_df[new_df["minute_start"]<=t]
    new_df=new_df[new_df["minute_end"]>t]
    return new_df

def get_sector_time(df,t):
    dt_hour=get_sector_time_pre(df,t)
    dt_h_list=list(dt_hour["icao"].unique())
    missing = [ele for ele in sector_list if ele not in  dt_h_list]
    for icao in missing:
        to_add=geo.GeoDataFrame({"icao":icao,"minute_start":0,"minute_end":0,"percentage":0,	"capacity_utilization":0,	"capacity":0,	"role":"E",	"criticality_index":0,	"geometry":geo.GeoSeries(df[df["icao"]==icao].iloc[0]["geometry"])})
        dt_hour=dt_hour.append(to_add)
    dt_hour.reset_index()
    return dt_hour



def correct_values(t,perc):
    if t[0]!=0:
        t=np.insert(t,0,0)
        perc=np.insert(perc,0,0)
    if t[-1]!=1440:
        t=np.append(t,1440)
        perc=np.append(perc,0)

    i=0
    while i<len(t)-1:
        if t[i+1]-t[i]>60:
            step=(t[i+1]-t[i])/3
            t=np.insert(t,i+1,np.array([i for i in np.arange(t[i]+step,t[i+1]-1,step)]))
            perc=np.insert(perc,i+1,np.zeros(2))
            i+=3
        else :
            i+=1
    return t,perc


def spline(x_points,y_points,x_new,k=3):
    tck = sc.splrep(x_points, y_points,k=k)
    return sc.splev(x_new, tck)






def make_percentage_mat(time_step=5):
    df=make_sectors()
    sector_list=get_sector_list()
    time=np.arange(0,1441,time_step)
    sector_list=get_sector_list()
    percentage_mat=np.zeros((len(sector_list),len(time)))
    for i in range(len(sector_list)):
        to_interp=df[df["icao"]==sector_list[i]]
        t=np.array((to_interp["minute_start"]+to_interp["minute_start"])/2)
        perc=np.array(to_interp["percentage"])
        t,perc=correct_values(t,perc)
        vect=spline(t,perc,time,1)
        vect=[i if i>=0 else 0 for i in vect ]
        percentage_mat[i]=vect
    return percentage_mat

def make_percentage_mat_one(time_step=5):
    mat=make_percentage_mat(time_step)
    mat=np.vstack([mat,np.array([1 for i in range(mat[1].size)])])
    return mat



def load_geodf(file_name):
    df=pd.read_csv(file_name)
    pol=[]
    for i in range(df.shape[0]):
        pol.append(shapely.wkt.loads(df["geometry"].iloc[i]))
    df["geometry"]=geo.GeoSeries(pol)
    return geo.GeoDataFrame(df)




def make_matrix(): #to fix if needed
    pol=Polygon(((6,50),(6.01,60.01),(6,60.01)))
    dff=df_geo
    dff=dff.append(geo.GeoDataFrame({"icao":"ZZZ NULL","geometry":geo.GeoSeries(pol)}),ignore_index=True)

    pp=np.vstack([percentage_mat,np.array([1 for i in range(percentage_mat[1].size)])])

    ppp=np.loadtxt("dati/per_mat_one.csv",delimiter=",")
