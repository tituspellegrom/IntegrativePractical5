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
def readData():
    sData = "TestDATA1.xlsx"
    dData = pd.read_excel(sData)
    mData = dData.values
    return mData

def main():
    # Initialisation
    shapefile = gpd.read_file("NLD_adm0.shp")
    mData = readData()
    cities = mData[:,1]
    fig = shapefile.plot(figsize=(40,20))
    
    for i,type in enumerate(cities):
        x = mData[i][3]
        y = mData[i][4]
        plt.scatter(x, y, c='black', s=40, alpha=0.6)
        plt.text(x-0.04, y-0.04, type, fontsize=9, rotation=0)
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.savefig("Nederland.jpg")
    
    # Output

###########################################################
### start main
if __name__ == "__main__":
    main()
