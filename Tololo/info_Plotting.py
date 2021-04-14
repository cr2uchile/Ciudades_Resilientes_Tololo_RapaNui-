# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 13:28:52 2020

@author: laura Gallardo

Plotting tool
"""

import pandas as pd  
# Libreria para Serie de datos indexa fechas, genera estadisticos rapidos .. etc
import numpy as np  
# Libreria para matrices y operaciones matematicas modo Matlab incluye Nans .. etc
import scipy.io
# Libreria para lectura de datos formato h5 h4 mat etc
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText


def FHIST(spec,dbname,df,Nbins, ext=None):
    '''
    
    
    Parameters
    ----------
    spec : String indicating species, e.g., O3
    dbname : string indicating data base, e.g., EBAS, or DMC
    df: dataframe with time, value, std of value
    ext: figure format, default is png
    Returns
    Figure :histogram of data, indicating period
    -------
    None.

    '''
    from matplotlib.offsetbox import AnchoredText
    from pylab import rcParams
    rcParams['figure.figsize'] = 10, 5

    plt.figure()
    plt.rcParams["font.family"] = "Times New Roman"                      
    plt.rcParams['xtick.labelsize'] = 16
    plt.rcParams['ytick.labelsize'] = 16
    
    if spec=='O3':
        series=df.O3_ppbv   #[df.O3_ppbv.between(df.O3_ppbv.quantile(.01), df.O3_ppbv.quantile(.99))]
    elif spec=='RH':
        series=df.RH_perc
        
    #Period of data
    fechas=df.index
    ini=fechas[0]
    fin=fechas[len(fechas)-1]

    mino=0
    maxo=np.nanmax(series)
        
    kwargs = dict(histtype='stepfilled', alpha=0.3, density=True, bins=Nbins)
        
    plt.hist(series, **kwargs)
    plt.xlim([mino, maxo])
    plt.ylim(0, 0.10)

    
    if spec=='O3':
        tit='Ozone (ppbv)'
        titu='Tololo (30°S, 70°W, 2151 m a.s.l.)'+' DB-'+dbname
    elif spec=='RH':
        tit='Relative Humidity (%)'
        titu='Tololo (30°S, 70°W, 2151 m a.s.l.)'+' DB-'+dbname
    
    titulo=titu+': '+'\n' +'from '+str(ini)+' to '+str(fin)
    plt.xlabel(tit,fontsize=18)
    plt.ylabel('Density',fontsize=18)
    plt.title(titulo, fontsize=20)
    
    ene=len(series)-np.sum(np.isnan(series))
       
    ax=plt.subplot(111)
    at = AnchoredText("N of bins "+str(Nbins)+"\n N of data points "+str(ene) + 
                      "\n N of missing data points "+str(np.sum(np.isnan(series))) +
                      "\n Mean: " + str(round(series.mean(),2)) + 
                      "\n Std: " + str(round(series.std(),2)), prop=dict(size=12), loc=1) 
    ax.add_artist(at)
    
    if ext ==None:
        ext='png'
                                           
#    plt.tight_layout(rect=[0, 0.03,1,0.95]) 
    plt.show()   
     
#    plt.savefig('COMPARISON/FIG_HIST_CO//'+stnname +'.'+ext, dpi=600)    
    
    return()


def FHIST2(spec,dbname,df,Nbins, ext=None):
    '''
    
    
    Parameters
    ----------
    spec : String indicating species, e.g., O3
    dbname : string indicating data base, e.g., EBAS, or DMC
    df: dataframe with time, value, std of value
    ext: figure format, default is png
    Returns
    Figure :histogram of data, indicating period
    -------
    None.

    '''
    from matplotlib.offsetbox import AnchoredText
    from pylab import rcParams
    rcParams['figure.figsize'] = 10, 5

    fig1 = plt.figure()
    fig1.clf()
    ax1 = fig1.add_subplot(111)
   # ax1.set_rcParams["font.family"] = "Times New Roman"                      
    #ax1.set_rcParams['xtick.labelsize'] = 16
    #ax1.set_rcParams['ytick.labelsize'] = 16
    
    if spec=='O3':
        series=df.O3_ppbv   #[df.O3_ppbv.between(df.O3_ppbv.quantile(.01), df.O3_ppbv.quantile(.99))]
    elif spec=='RH':
        series=df.RH_perc
        
    #Period of data
    fechas=df.index
    ini=fechas[0]
    fin=fechas[len(fechas)-1]

    mino=0
    maxo=np.nanmax(series)
        
    kwargs = dict(histtype='stepfilled', alpha=0.3, density=True, bins=Nbins)
        
    ax1.hist(series, **kwargs)
    ax1.axvline(5, color='r', label='Instrument Limit Detection')
    ax1.axvline(65, color='blue', label='L.Gallardo Filter')
    ax1.axvline(series.mean() + 4*series.std(), color='teal', label='M.Schultz Filter')
    ax1.axvline(series.mean() - 4*series.std(), color='teal')
    ax1.axvline(10, color='yellow', label='J.Anet Filter')
    ax1.axvline(55, color='yellow')
    ax1.axvline(series.mean(), color='k', label='Mean')
    ax1.set_xlim([mino, maxo + 15])
    ax1.set_ylim(0, 0.10)
    ax1.legend(loc='lower right')

    
    if spec=='O3':
        tit='Ozone (ppbv)'
        titu='Tololo (30°S, 70°W, 2151 m a.s.l.)'+' DB-'+dbname
    elif spec=='RH':
        tit='Relative Humidity (%)'
        titu='Tololo (30°S, 70°W, 2151 m a.s.l.)'+' DB-'+dbname
    
    titulo=titu+': '+'\n' +'from '+str(ini)+' to '+str(fin)
    ax1.set_xlabel(tit,fontsize=18)
    ax1.set_ylabel('Density',fontsize=18)
    ax1.set_title(titulo, fontsize=20)
    
    ene=len(series)-np.sum(np.isnan(series))
       
    ax=plt.subplot(111)
    at = AnchoredText("N of bins "+str(Nbins)+"\n N of data points "+str(ene) + 
                      "\n N of missing data points "+str(np.sum(np.isnan(series))) +
                      "\n Mean: " + str(round(series.mean(),2)) + 
                      "\n Std: " + str(round(series.std(),2)), prop=dict(size=12), loc=1) 
    ax.add_artist(at)
    
    if ext ==None:
        ext='png'
                                           
#    plt.tight_layout(rect=[0, 0.03,1,0.95]) 
    fig1.show()   
     
#    plt.savefig('COMPARISON/FIG_HIST_CO//'+stnname +'.'+ext, dpi=600)    
    
    return()

########Time series plot
    

def FSERIES(spec,dbname,df,tipo, ext=None):
    '''
  
    Parameters
    ----------
    spec : String indicating species, e.g., O3
    dbname : string indicating data base, e.g., EBAS, or DMC
    df: dataframe with time, value, std of value
    tipo: 1 indicates plain time series, 2 time series+std
    ext: figure format, default is png
    Returns
    Figure Time series plots
    -------
    None.

    '''
    from matplotlib.offsetbox import AnchoredText
    from pylab import rcParams
    rcParams['figure.figsize'] = 10, 5

    plt.figure()
    plt.rcParams["font.family"] = "Times New Roman"                      
    plt.rcParams['xtick.labelsize'] = 16
    plt.rcParams['ytick.labelsize'] = 16
    
    if spec=='O3':
        series=df.O3_ppbv
    elif spec=='RH':
        series=df.RH_perc
        
    #Period of data
    fechas=df.index
    ini=fechas[0]
    fin=fechas[len(fechas)-1]
    
    mino=0
    maxo=np.nanmax(series)
    
    plt.plot(series)
    plt.ylim([mino,maxo+10])
#    plt.ylim(0,0.10)

    
    if spec=='O3':
        tit='Ozone (ppbv)'
        titu='Tololo (30°S, 70°W, 2151 m a.s.l.)'+' DB-'+dbname
    elif spec=='RH':
        tit='Relative Humidity (%)'
        titu='Tololo (30°S, 70°W, 2151 m a.s.l.)'+' DB-'+dbname
    
    
    titulo=titu+': '+'\n' +'from '+str(ini)+' to '+str(fin)
    plt.title(titulo)
    plt.xlabel('Date',fontsize=18)
    plt.ylabel(tit,fontsize=18)
    
    ax=plt.subplot(111)
    at = AnchoredText("Mean: " + str(round(series.mean(),2)) + 
                      "\n Std: " + str(round(series.std(),2)) +
                      "\n Trend 1: " + 'XX +/- YY ppbv/decada'+
                      "\n Trend 2: " + 'XX +/- YY ppbv/decada' 
                      , prop=dict(size=12), loc=1) 
    ax.add_artist(at)
    
    #plt.title(titulo, fontsize=20) 
    #    plt.tight_layout(rect=[0, 0.03,1,0.95]) 
    plt.show()   
     
#    plt.savefig('COMPARISON/FIG_HIST_CO//'+stnname +'.'+ext, dpi=600)    
    
    return()
    