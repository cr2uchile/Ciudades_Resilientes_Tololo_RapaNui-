#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 11:32:58 2021

@author: sebastian
"""


import pandas as pd              # Data structures
import matplotlib.pyplot as plt  # Plotting
import os as os                  # Directory management



def plot_sonde(df, save=False):
    """

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    save : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    None.

    """
    
    date_str = date.strftime('%Y-%m-%d')
    
    fig, ax = plt.subplots(2, 3, figsize=(16, 11), sharey=True)
    
    var_names = ['O3PartialPressure', 'Temperature', 'RelativeHumidity', 
                 'Pressure', 'WindSpeed', 'WindDirection']
    
    for var in var_names:
        if var == 'O3PartialPressure':
            xlabel = 'Ozone [mPa]'
            Xmin = 0
            Xmax = 28
            n = 0
            m = 0
        elif var == 'Temperature':
            xlabel = 'Temperature [°C]'
            Xmin = -82
            Xmax = 31
            n = 0
            m = 1
        elif var == 'RelativeHumidity':
            xlabel = 'Relative Humidity [%]'
            Xmin = 0
            Xmax = 100
            n = 0
            m = 2
        elif var == 'Pressure':
            xlabel = 'Pressure [hPa]'
            Xmin = 1
            Xmax = 1025
            n = 1
            m = 0
        elif var == 'WindSpeed':
            xlabel = 'Wind Speed [m/s]'
            Xmin = 0
            Xmax = 80
            n = 1
            m = 1
        elif var == 'WindDirection':
            xlabel = 'Wind Direction [°]'
            Xmin = 0
            Xmax = 360
            n = 1
            m = 2
            
        # Height in km
        z = 1e-3 * df.GPHeight.values
        
        # Plot var in subplot
        ax[n,m].plot(df[var], z, color='b', marker='.', markersize=3.5, linewidth=0.3)
        ax[n,m].set_xlabel(xlabel, fontsize=16)
        ax[n,m].set_xlim(xmin=Xmin, xmax=Xmax)
        ax[n,m].set_ylim(ymin=0, ymax=40)
        #add ylabel
        if m==0 and (n==0 or n==1):
            ax[n,m].set_ylabel('Altitude [km]', fontsize=16)

    
    # Add suptitle
    fig.suptitle('Rapa Nui - '+date_str, fontsize=20)
    
    # Save figure
    if save == True:
        fig.savefig(path+"/Graphs_Inspection_Valid/"+'RapaNui_'+date_str+".png", dpi=400)    

    return()




# Get path
path = os.getcwd()

# Read data ozonosondes
dfold = pd.read_csv(path+"/"+"RapaNui_all_ozonesondes.csv", delimiter=',', 
                    index_col=0, parse_dates=True)

# Read dates launch
dates = pd.read_csv(path+"/"+"RapaNui_dates_valid.csv", 
                    delimiter=',', index_col=0, parse_dates=True)
dates = dates.index


# years to be plotted
yi = 2015
yf = 2019

for date in dates:
    if date.year in range(yi, yf+1):
        
        # extract profile per date
        df = dfold.loc[date]
        
        # plot
        plot_sonde(df, save=True)
        
        plt.close('all')
       
        
