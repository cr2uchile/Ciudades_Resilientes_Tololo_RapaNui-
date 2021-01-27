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
    
    date_str = date.strftime('%Y-%m-%d')
    
    fig, ax = plt.subplots(3, 2, figsize=(12, 18), sharey=True)
    #plt.cla()
    
    var_names = ['O3PartialPressure', 'Temperature', 'RelativeHumidity', 
                 'Pressure', 'WindSpeed', 'WindDirection']
    
    for var in var_names:
        if var == 'O3PartialPressure':
            xlabel = 'Ozone [mPa]'
            Xmin = -2
            Xmax = 20
            n = 0
            m = 0
        elif var == 'Temperature':
            xlabel = 'Temperature [°C]'
            Xmin = -70
            Xmax = 20
            n = 0
            m = 1
        elif var == 'RelativeHumidity':
            xlabel = 'Relative Humidity [%]'
            Xmin = 0
            Xmax = 100
            n = 1
            m = 0
        elif var == 'Pressure':
            xlabel = 'Pressure [hPa]'
            Xmin = 1
            Xmax = 1040
            n = 1
            m = 1
        elif var == 'WindSpeed':
            xlabel = 'Wind Speed [°]'
            Xmin = 0
            Xmax = 100
            n = 2
            m = 0
        elif var == 'WindDirection':
            xlabel = 'Wind Speed [m/s]'
            Xmin = 0
            Xmax = 360
            n = 2
            m = 1
            
        # Height in km
        z = 1e-3 * df.GPHeight.values
        
        # Plot var in subplot
        ax[n,m].plot(df[var], z, marker='.')
        ax[n,m].set_xlabel(xlabel)
        ax[n,m].set_xlim(xmin=Xmin, xmax=Xmax)
        ax[n,m].set_ylim(ymin=0, ymax=40)
    
    # Add suptitle
    fig.suptitle('Rapa Nui - '+date_str)
    
    # Save figure
    if save == True:
        fig.savefig(path+"/Graphs_Inspection_Valid/"+date_str+".png", dpi=400)    

    return()




# Get path
path = os.getcwd()

# Read data ozonosondes
dfold = pd.read_csv(path+"/"+"ozonesondes-1995-2019.csv", delimiter=',', 
                    index_col=0, parse_dates=True)

# Read dates launch
dates = pd.read_csv(path+"/"+"dates_valid_ozonesondes-1995-2019.csv", 
                    delimiter=',', index_col=0, parse_dates=True)
dates = dates.index


# years to be plotted
yi = 2019
yf = 2019

for date in dates:
    if date.year in range(yi, yf+1):
        date = dates[-1]
        df = dfold[dfold.index==date]
        
        plot_sonde(df, save=True)
        
        break
        
        

#from scipy interpolate import interp1d
#ocupar oop como el caso de tololo
#from scipy.interpolate import interp1d 
#interp1d(z, serie, type_intp, bounds_error=False)
#serie_f(z_intp)
#U = - |V| cos(angulo) 
#V = -|V| sin(angulo) 
# def grafica(year, n):
    
#     filenames = glob(path + "/"+str(year)+"/"+str(year)+"*.csv")
#     dir_2019 = path + '/2019/20190427.ECC.6a.na.EIMO.csv'
#     if year==2019:
#         df = []
#         for i in range(len(filenames)):
#             if filenames[i] == dir_2019:
#                 df.append(pd.read_csv(dir_2019, skiprows = 26))
#             else:
#                 df.append(pd.read_csv(filenames[i], skiprows = n))            
#     else:            
#         df = [pd.read_csv(f, skiprows = n) for f in filenames]
#     for i in range(len(df)):       
#         # Pressure = df[i].Pressure 
#         # O3PartialPressure = df[i].O3PartialPressure
#         # Temperature = df[i].Temperature
#         # RelativeHumidity = df[i].RelativeHumidity
#         # GPHeight = df[i].GPHeight*10**-3
#         # z = np.arange(0,35, 0.1)
#         # Pressure_interp = np.interp(z, GPHeight, Pressure)
#         # O3PartialPressure_interp = np.interp(z, GPHeight, O3PartialPressure)
#         # Temperature_interp = np.interp(z, GPHeight, Temperature)
#         # RelativeHumidity_interp = np.interp(z, GPHeight, RelativeHumidity)
#         # O3_ppbv = (O3PartialPressure_interp*10**-3)/ (Pressure_interp*10**2)*10**9
        
#         Pressure = df[i].Pressure 
#         O3PartialPressure = df[i].O3PartialPressure
#         Temperature = df[i].Temperature
#         RelativeHumidity = df[i].RelativeHumidity
#         GPHeight = df[i].GPHeight*10**-3
#         z = GPHeight
#         Pressure_interp = Pressure = df[i].Pressure
#         O3PartialPressure_interp = df[i].O3PartialPressure
#         Temperature_interp = df[i].Temperature
#         RelativeHumidity_interp = df[i].RelativeHumidity
#         O3_ppbv = O3PartialPressure
#         if year ==2018 or year==2019:
#             fig, ax = plt.subplots(3, 2, figsize=(6, 18), sharey=True)
#             plt.cla()    
#             ax[0,0].plot(O3_ppbv, z, label='Vertical structure of $O_{3}$', marker='.')
#             #ax[0,0].set_xscale('log')
#             ax[0,0].set_xlabel('$O_{3}$ [mpa]')
#             ax[0,0].set_ylabel('Height [km]')
#             ax[0,0].set_xlim(xmin=-3, xmax=20)
#             ax[0,0].set_ylim(ymin=0, ymax=40)
#             ax[0,0].legend()
            
#             ax[0,1].plot(Temperature_interp, z, label='Vertical structure of Temperature', marker='.')
#             ax[0,1].set_xlabel('T [°C]')
#             ax[0,1].set_ylabel('Height [km]')
#             ax[0,1].legend()
            
#             ax[1,0].plot(Pressure_interp, z, label='Vertical structure of Pressure', marker='.')
#             ax[1,0].set_xlabel('P [hpa]')
#             ax[1,0].set_ylabel('Height [km]')
#             ax[1,0].legend()
            
#             ax[1,1].plot(RelativeHumidity_interp, z, label='Vertical structure of HR', marker='.')
#             ax[1,1].set_xlabel('HR ')
#             ax[1,1].set_ylabel('Height [km]')
#             ax[1,1].legend()
        
#             WindDirection = df[i].WindDirection
#             WindSpeed = df[i].WindSpeed
#             WindDirection_interp = df[i].WindDirection
#             WindSpeed_interp =  WindSpeed = df[i].WindSpeed
#             ax[2,0].plot(WindDirection_interp, z, label='Vertical structure of Wind Direction', marker='.')
#             ax[2,0].set_xlabel('Wind Direction')
#             ax[2,0].set_ylabel('Height [km]')
#             ax[2,0].legend()            

#             ax[2,1].plot(WindSpeed_interp, z, label='Vertical structure of speed', marker='.')
#             ax[2,1].set_xlabel('Velociy [m/s]')
#             ax[2,1].set_ylabel('Height [km]')
#             ax[2,1].legend()
#             fig.savefig(path+"/"+str(year)+'/graphs/All/'+str(filenames[i][64:72])+'Allprofiles.png', dpi=400)
#             plt.cla() 
#         else:
#             fig, ax = plt.subplots(2, 2, figsize=(6, 12), sharey=True)
#             plt.cla()    
#             ax[0,0].plot(O3_ppbv, z, label='Vertical structure of $O_{3}$', marker='.')
#             #ax[0,0].set_xscale('log')
#             ax[0,0].set_xlabel('$O_{3}$ [mpa]')
#             ax[0,0].set_ylabel('Height [km]')
#             ax[0,0].set_xlim(xmin=0, xmax=20)
#             ax[0,0].set_ylim(ymin=0, ymax=40)
#             ax[0,0].legend()
            
#             ax[0,1].plot(Temperature_interp, z, label='Vertical structure of Temperature', marker='.')
#             ax[0,1].set_xlabel('T [°C]')
#             ax[0,1].set_ylabel('Height [km]')
#             ax[0,1].legend()
            
#             ax[1,0].plot(Pressure_interp, z, label='Vertical structure of Pressure', marker='.')
#             ax[1,0].set_xlabel('P [hpa]')
#             ax[1,0].set_ylabel('Height [km]')
#             ax[1,0].legend()
            
#             ax[1,1].plot(RelativeHumidity_interp, z, label='Vertical structure of HR', marker='.')
#             ax[1,1].set_xlabel('HR ')
#             ax[1,1].set_ylabel('Height [km]')
#             ax[1,1].legend()
#             fig.savefig(path+"/"+str(year)+'/graphs/All/'+str(filenames[i][64:72])+'Allprofiles.png', dpi=400)
#             plt.cla() 
        
# def calc_ind_desc(z):

#     ind = []

#     zant = z[0]
#     for i in range(1,len(z)):
#         if z[i] > zant:
#             zant = z[i]
#         else:
#             ind.append(i)

# return ind 

# ides = calc_ind_desc(z)
# z = np.delete(z, ides) 
