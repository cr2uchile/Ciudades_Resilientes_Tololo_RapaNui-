#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 13:42:02 2021

@author: charlie opazo and sebastian villalon

Read file "RapaNui_all_ozonesondes.csv", cleaning and interpolate data.
Remove points that measured altitude is descending.
Remove layers in ozone profiles with anomalous measurements
Interpolate variables to regular altitudes every 100 m between 0 y 35 km-
Save individual files per launch and one file with all sondes data.

Saved variables: 
    Pressure [hPa]
    Temperature [K]
    Relative Humidity [%]
    Ozone partial pressure [mba]
    Ozone [ppbv]
    Column ozone [DU]
    Zonal wind [m/s]
    Meridional wind [m/s]
    Potential temperature [K]
    Equivalent potential temperature [K]
    Water vapor mixing ratio [g/kg]


"""

# Import libraries
import numpy as np
import pandas as pd
import os
from scipy.interpolate import interp1d
import warnings




def remov_desc(df):
    """
    Remove rows with points in sonde data that are descending in altitude 
    during flight time
    
    Parameters
    ----------
    df : DataFrame
        DataFrame with data per launch.

    Returns
    -------
    df_clean : DataFrame
        DataFrame without points that are descending in profile

    """
    
    # Extract altitude
    z = df.GPHeight.values
    
    # Find z decreasing
    i_zasc = []
    zant = z[0]
    for i in range(1,len(z)):
        if z[i] > zant:
            zant = z[i]
            i_zasc.append(i)
        else:
            pass
            
    # remove zdec in dataframe
    df_clean = df.iloc[i_zasc]
    
    return df_clean



def interp_serie(z_intp, z, serie, type_intp='linear'):
    """
    Interpolate vertical profiles to regular altitudes in array z

    Parameters
    ----------
    z_intp : array
        Array with altitudes where interpolate.
    z : array
        Array with altitudes measured altitudes.
    serie : array
        Measured variable to interpolate.
    type_intp : str, optional
        Type of interpolation. The default is 'linear'.

    Returns
    -------
    serie_intp : array
        Variable interpolated to regular altitudes.

    """

    serie_f = interp1d(z, serie, type_intp, bounds_error=False)
    serie_intp = serie_f(z_intp)
    
    return serie_intp



def df_to_csv(df_interp, launch_datetime, z0):
    """
    Save dataFrame with sonde data to file .csv

    Parameters
    ----------
    df_interp : DataFrame
        Sonde data interpolated per launch.
    launch_datetime : datetime
        Sounding launch datetime
    z0: float
        Sounding launch altitude 

    Returns
    -------
    None.

    """
    
    
    # Lauch date and launch time to str
    date_str = date.strftime('%Y%m%d')
    time_str = date.strftime('%H:%M')
    # Launch altitude to str
    z0_str = str(z0)
    
    # Filename and path for csv file
    filename_interp = 'RapaNui_'+date_str+'.csv'
    path_fn = path+'/'+'Data_Interpolate/'+filename_interp
    
    # Headers: variables and units
    hd1 = ['Alt', 'Press', 'Temp', 'RH', 'O3', 'O3', 'O3', 'uwnd', 'vwnd', 
           'Speed', 'Direction', 'Theta', 'Theta_e', 'MixRatio']
    hd2 = ['km', 'hPa', 'K', '%', 'mPa', 'ppbv', 'DU', 'm/s', 'm/s', 'm/s', '°', 'K', 'K', 'g/kg']
    
    
    # Add header with metadata
    with open(path_fn, 'w') as f:
        f.write('STATION                          : Easter Island (Rapa Nui), Chile' + '\n')
        f.write('Data Provider                    : DMC Dirección Meteorológica de Chile, GAW Program' + '\n')
        f.write('Data Compilation                 : 05 April, 2021, by CR2 Center for Climate and Resilience Research, data interpolated every 100m' + '\n')
        f.write('Latitude (deg)                   : -27.17' + '\n')
        f.write('Longitude (deg)                  : -109.42' + '\n')
        f.write('Elevation (m)                    : ' + z0_str + '\n')
        f.write('Launch Date (YYYYMMDD)           : ' + date_str + '\n')
        f.write('Launch Time (UTC)                : ' + time_str + '\n')
        f.write('Sonde Instrument, SN             : SPC 6A' + '\n')
        f.write('Radiosonde, SN                   : Vaisala, CCE64B' + '\n')
        f.write('Solution                         : 1.0% buffered' + '\n')
        f.write('Applied pump corrections         : ' + '\n')
        f.write('Pump flow rate (sec/100ml)       : 9000' + '\n')
        f.write('Background current (uA)          : 9000' + '\n')
        f.write('Missing or bad values            : 9000' + '\n')
        
        
        
    # hd = [['STATION', ':', 'Rapa Nui, Chile'], 
    #       ['Data Provider', ':', 'DMC Dirección Meteorológica de Chile, GAW Program'],
    #       ['Data Compilation', ':', '05 April, 2021, by CR2 Center for Climate and Resilience Research, data interpolated every 100m'],
    #       ['Latitude (deg)', ':', ''],
    #       ['Longitude (deg)', ':', ''],
    #       ['Elevation (m)', ':', ''],
    #       ['Launch Date', ':', ''],
    #       ['Launch Time (UT)', ':', '']
    #      ]
    
    #pd.DataFrame(hd).to_csv(path_fn, mode='w', sep='\t', header=False, index=False)
    # Save headers for variables
    pd.DataFrame([hd1, hd2]).to_csv(path_fn, mode='a', sep='\t', header=False, index=False)
    
    # Save data
    df_clear.to_csv(path_fn, mode='a', sep='\t', header=False)
    
    
    return()





# Read files
# Get path
path = os.getcwd()

# Read data ozonosondes
dfold = pd.read_csv(path+"/"+"RapaNui_all_ozonesondes.csv", delimiter=',', 
                    index_col=0, parse_dates=True)

# Read dates launch
df_validate = pd.read_csv(path+"/"+"RapaNui_dates_valid.csv", 
                          delimiter=',', index_col=0, parse_dates=True)
# dates for ozonesondes
dates = df_validate.index


# Year to interpolate
yi = 1995
yf = 2019

# Constants
R=8.314472; #(J/(mol K))
Cp=29.19; #(J/(mol K))


# Height to interpolate, between 0-35 km every 100 m
z = np.arange(0,35.1, 0.1)


# Make dataframe for data complete
dfold_clear = pd.DataFrame()

for date in dates:
    
    # ignore warnings
    warnings.filterwarnings("ignore")
    
    if date.year in range(yi, yf+1):
        
        # Extract data date
        df = dfold.loc[date]
        
        # Check if height is monotonic increasing. If is not monotonic, remove
        # rows associated to those data
        if (df.GPHeight.is_monotonic_increasing and df.GPHeight.is_unique):
            pass
        else:
            df = remov_desc(df)

        
        #Lecture of Data
        GPHeight = df.GPHeight.values*10**-3
        Pressure = df.Pressure.values
        O3PartialPressure = df.O3PartialPressure.values
        Temperature = df.Temperature.values
        RelativeHumidity = df.RelativeHumidity.values
        Wind_Speed = df.WindSpeed.values
        Wind_Direction = df.WindDirection.values
        
        # Remove ozone profile not valid
        if df_validate.Valid[date]==0:
            O3PartialPressure = np.nan * np.zeros(len(GPHeight))
        
        # Remove layer of ozone profile not valid
        if ~np.isnan(df_validate.loc[date].Height_inf):
            O3PartialPressure[(GPHeight >= df_validate.loc[date].Height_inf) & 
                              (GPHeight <= df_validate.loc[date].Height_sup)] = np.nan
            
        
        #Determination of diferent variables
        
        Temperature_K = Temperature + 273.15
        O3_ppbv = (O3PartialPressure*10**-3)/ (Pressure*10**2)*10**9
        T_potencial = Temperature_K*(1000/Pressure)**(R/Cp)
        U = - Wind_Speed*np.cos((np.pi/180)*Wind_Direction) 
        V = - Wind_Speed*np.sin((np.pi/180)*Wind_Direction)
        Satured_Vapor_Pressure = 6.11*np.exp(5.42*10**3*(1/273-1/Temperature_K))
        Satured_Mixing_Ratio = 0.622*(Satured_Vapor_Pressure/(Pressure-Satured_Vapor_Pressure))
        Mixing_Ratio = 1e3*(RelativeHumidity/100)*Satured_Mixing_Ratio
        T_potencial_e = (Temperature_K*(1+0.061*Mixing_Ratio))*(1000/Pressure)**(R/Cp)
        
        Omega_S = np.zeros(len(GPHeight))
        Sum_Omega_S = np.nan*np.zeros(len(GPHeight))
        if df_validate.Valid[date]==1:
            for i in range(len(GPHeight)-1):
                Omega_S[i] =  3.9449*(O3PartialPressure[i]+O3PartialPressure[i+1])*np.log(Pressure[i]/Pressure[i+1])
                a = np.nansum(Omega_S)
                Sum_Omega_S[i] = a
        #agregar columna de ozono()
        
        
        #Interpolación de distintas variables
        
        Pressure_interp = interp_serie(z, GPHeight, Pressure)
        Temperature_K_interp = interp_serie(z, GPHeight, Temperature_K)
        RelativeHumidity_interp = interp_serie(z, GPHeight, RelativeHumidity)
        T_potencial_interp = interp_serie(z, GPHeight, T_potencial)
        T_potencial_e_interp = interp_serie(z, GPHeight, T_potencial_e)
        U_interp = interp_serie(z, GPHeight, U)
        V_interp = interp_serie(z, GPHeight, V)
        Wind_Speed_interp = np.sqrt(U_interp**2+V_interp**2)
        Wind_Direction_interp = np.arctan2(V_interp, U_interp) * (180/np.pi)
        Wind_Direction_interp[Wind_Direction_interp<0] = Wind_Direction_interp[Wind_Direction_interp<0] + 360
        Mixing_Ratio_interp = interp_serie(z, GPHeight, Mixing_Ratio)
        
        O3PartialPressure_interp = interp_serie(z, GPHeight, O3PartialPressure)
        O3_ppbv_interp = interp_serie(z, GPHeight, O3_ppbv)
        Sum_Omega_S_interp = interp_serie(z, GPHeight, Sum_Omega_S)
        

        
        # Make dataframe with variables
        df_clear = pd.DataFrame(data={'Pressure':Pressure_interp,'Temp':Temperature_K_interp, 
                                      'RH':RelativeHumidity_interp, 'O3_mPa': O3PartialPressure_interp,
                                      'O3_ppbv':O3_ppbv_interp, 'O3_column':Sum_Omega_S_interp,
                                      'U':U_interp, 'V':V_interp, 'WndSpd' : Wind_Speed_interp,
                                      'WndDir' : Wind_Direction_interp, 'Theta':T_potencial_interp,
                                      'Theta_e':T_potencial_e_interp, 'Mixing_Ratio':Mixing_Ratio_interp}, 
                                index=z)
        df_clear.index.rename('Alt', inplace=True)
        
        # Change nan to 9000
        df_clear.fillna(9000, inplace=True)
        
        # Round values in dataframe
        df_clear.index = np.around(df_clear.index, 1)
        df_clear['Pressure'] = df_clear['Pressure'].map('{:.3f}'.format)
        df_clear['Temp'] = df_clear['Temp'].map('{:.3f}'.format)
        df_clear['RH'] = df_clear['RH'].map('{:.3f}'.format)
        df_clear['O3_mPa'] = df_clear['O3_mPa'].map('{:.3f}'.format)
        df_clear['O3_ppbv'] = df_clear['O3_ppbv'].map('{:.3f}'.format)
        df_clear['O3_column'] = df_clear['O3_column'].map('{:.3f}'.format)
        df_clear['U'] = df_clear['U'].map('{:.3f}'.format)
        df_clear['V'] = df_clear['V'].map('{:.3f}'.format)
        df_clear['WndSpd'] = df_clear['WndSpd'].map('{:.3f}'.format)
        df_clear['WndDir'] = df_clear['WndDir'].map('{:.3f}'.format)
        df_clear['Theta'] = df_clear['Theta'].map('{:.3f}'.format)
        df_clear['Theta_e'] = df_clear['Theta_e'].map('{:.3f}'.format)
        df_clear['Mixing_Ratio'] = df_clear['Mixing_Ratio'].map('{:.5f}'.format)
        
        
        
        # Save sounding interpolated
        df_to_csv(df_clear, date, 1e3*GPHeight[0])
        
        
        # Add ozonesonde to dataframe with all soundings
        df_clear2 = df_clear.copy()
        
        # Make index datetime
        N = len(z)
        time = []
        for i in range(N):
            time.append(date)
        time = pd.to_datetime(time)
        time.name ='Datetime'
        
        # Add multi index to dataframe [datetime, altitude]
        df_clear2.set_index([time, df_clear2.index], inplace=True)
        
        # Add to dataframe complete
        dfold_clear = pd.concat([dfold_clear, df_clear2])
                
    
    
# Save in .csv all ozonesondes interpolated
dfold_clear.replace(to_replace=9000, value=np.nan, inplace=True)
dfold_clear.to_csv(path+'/'+'RapaNui_all_clear.csv')
