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

@author: rsl640
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
    cities = mData[:,1]
    fig = shapefile.plot(figsize=(40,20), edgecolor ='g', color='w')
    
    for i,type in enumerate(cities):
        x = mData[i][3]
        y = mData[i][4]
        plt.scatter(x, y, c='black', s=40, alpha=0.6)
        plt.text(x-0.04, y-0.04, type, fontsize=9, rotation=0)
        #plt.text(x, y, )
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    
    

def plotLine(connections, mData):
    for i in range(int(np.size(connections)/2)):
        x1 = mData[connections[i][0]][3]
        y1 = mData[connections[i][0]][4]
        x2 = mData[connections[i][1]][3]
        y2 = mData[connections[i][1]][4]
        linex = [x1,x2]
        liney = [y1,y2]
        plt.plot(linex, liney, c='black', alpha=0.4)
    plt.savefig("Nederland.png")
    