#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Groep 5.py

Purpose:
    Outputs Tomatoes sold per day per store for J, AH and K in Excell files
    Tests the data by OLS

Version:
    3

Date:
    08/01/20

@author: 
"""
###########################################################
### Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm


###########################################################
### main

def readData(sSheet):
    sData = "Logistics2.xlsx"
    dData = pd.read_excel(sData, sheet_name = sSheet)
    dData.fillna(0, inplace=True)
    mData = dData.values
    return mData

def readDay(sDay):
    mDay = readData(sDay)

    return mDay

def readStore(sStore):
    mStore = readData(sStore)
    
    return mStore

'''
def plotData(mDay):
    plt.plot(mDay[:,0], mDay[:,2])
    plt.show()
    plt.plot(mDay[:,1], mDay[:,2])
'''

def checkOlsDay(sDay):
    mDay = readDay(sDay)
    model = sm.OLS(mDay[:,2], mDay[:,1])
    results = model.fit()
    print(results.summary())

def salesTomatoesSquaredMeter(mDay):
    return sum(mDay[:,2])/sum(mDay[:,0])
 
def tomatoesStoreDay(iSalesTomatoesSquaredMeter, mStore):
    mTomatoesStoreDay = mStore[:,0]
    mTomatoesStoreDay = mTomatoesStoreDay.reshape(-1,1)
    
    for i in range(5):
        test = iSalesTomatoesSquaredMeter*mStore[:,i+1]
        test = test.reshape(-1,1)
        mTomatoesStoreDay = np.append(mTomatoesStoreDay, test, axis = 1)
    
    return mTomatoesStoreDay

def showSalesPerStorePerDay(sStore):
    vDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    mStore = readStore(sStore)
    writer = pd.ExcelWriter("Tomatoes per store per day %s.xlsx" % sStore, engine ='xlsxwriter')
    
    for i in range(np.size(vDays)):
        mDay = readDay(vDays[i])
        iSalesTomatoesSquaredMeter = salesTomatoesSquaredMeter(mDay)
        mtomatoesStoreDay = pd.DataFrame(tomatoesStoreDay(iSalesTomatoesSquaredMeter, mStore))
        mtomatoesStoreDay.to_excel(writer, sheet_name=vDays[i], index = False, header = False)

    writer.save()
    
def main():
    # Initialisation
    vStores = ["J", "AH", "K"]
    checkOlsDay("Saturday")
    
    # Output
    for i in range(np.size(vStores)):
        showSalesPerStorePerDay(vStores[i])
  
###########################################################
### start main
if __name__ == "__main__":
    main()
