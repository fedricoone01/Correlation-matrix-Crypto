# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 15:34:57 2022

@author: Fede
"""

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
api_key = ""

monedas = ["BTC","ETH","XRP","LUNA","BNB","SOL","AVAX","ADA","DOT","DOGE","MATIC","LINK","SHIB"]


#Matriz de correlación
def graficaCorr(dfCorr, title=""):
    
    fig=plt.figure(figsize=(14,9))
    plt.matshow(dfCorr, fignum=fig.number, cmap='YlGn')
    plt.xticks(range(dfCorr.shape[1]), dfCorr.columns, rotation=90, fontsize=17,fontweight="bold")
    plt.yticks(range(dfCorr.shape[1]), dfCorr.columns, fontsize=17,fontweight="bold")

    cb=plt.colorbar(orientation="vertical", label="Correlación")
    cb.ax.tick_params(labelsize=15)
    plt.title("  Matriz de correlación - Cryptomonedas de mayor capitalización", fontsize=23, y=1.15,fontweight="bold", C="red")
    
    ax = plt.gca()
    ax.set_xticks(np.arange(-.5, len(dfCorr), 1), minor=True);
    ax.set_yticks(np.arange(-.5, len(dfCorr), 1), minor=True);
    ax.grid(which="minor", color="black", linestyle="-", linewidth=3)
    ax.grid(which="major", color="none", linestyle="-", linewidth=3)
    
    for i in range(dfCorr.shape[0]):
        for j in range(dfCorr.shape[1]):
            if dfCorr.iloc[i,j]>0.9:
                color = "white"
            else:
                color = "black"
            fig.gca().text(i,j, "{:.2f}".format(dfCorr.iloc[i,j]), ha="center", va="center", c=color, size="15")
    plt.show()


#Datos históricos
def histoDay(e, fsym, tsym, toTs=None, limit=360, aggregate=1, allData="false"):
    url = "https://min-api.cryptocompare.com/data/v2/histoday"
    
    params = {"api_key" : api_key, "e":e, "fsym":fsym, "tsym":tsym, "allData":allData, 
              "Tots":toTs, "limit":limit, "aggregate":aggregate}
    r = requests.get(url, params=params)
    js = r.json()["Data"]["Data"]
    df=pd.DataFrame(js)
    df.time=pd.to_datetime(df.time, unit="s")
    df = df.set_index("time").drop(["conversionType","conversionSymbol","high","low","open","volumefrom","volumeto"], axis=1)
    return df

#Armado del DataFrame
lista = []
tabla = pd.DataFrame()

for i in monedas:
    lista.append(histoDay("CCCAGG", i, "USD"))
todo = pd.concat(lista, axis=1)
todo.columns=monedas
print(todo)


#Invocamos la función para graficar el DataFrame
graficaCorr(todo.corr())

        
    

