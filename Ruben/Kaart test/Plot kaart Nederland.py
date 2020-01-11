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
    fig = plt.figure(figsize=(40,20))
    fig = shapefile.plot()
    
    mData = readData()
    for i in range(29):
        fig.scatter(mData[i][3], mData[i][4], zorder=1, alpha= 0.2, c='black', s=10)       
    
    plt.savefig("Nederland.jpg")
    # Output

###########################################################
### start main
if __name__ == "__main__":
    main()
