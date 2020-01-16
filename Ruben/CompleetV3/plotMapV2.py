#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test.py

Purpose:
    ...

Version:
    1       First start

Date:
    dd/mm/yy

@auhor: rsl640
"""
###########################################################
### Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

###########################################################
### main
def plotPoints(mData):
    shapefile = gpd.read_file("NLD_adm0.shp")
    cities = mData[:,0]
    fig = shapefile.plot(figsize=(40,20), edgecolor ='g', color='w')
    
    for i,type in enumerate(cities):
        x = mData[i][1]
        y = mData[i][2]
        plt.scatter(x, y, c='black', s=40)
        plt.text(x-0.04, y-0.04, type, fontsize=9, rotation=0)
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)       


def plotLine(active_arcs, iColor):
    for i in active_arcs:
        x1 = i[0].city.longitude
        y1 = i[0].city.latitude
        x2 = i[1].city.longitude
        y2 = i[1].city.latitude
        linex = [x1,x2]
        liney = [y1,y2]
        plt.plot(linex, liney, c=iColor, alpha=0.4)
    plt.savefig("Nederland.png")
