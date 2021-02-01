#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 13:42:02 2021
@author: sebastian
"""

# Import libraries
import numpy as np
import pandas as pd
import os
from scipy.interpolate import interp1d
import warnings




def remov_desc(df):
    """

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

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
    df = df.iloc[i_zasc]
    
    return df


def interp_serie(z_intp, z, serie, type_intp='linear'):
    """

    Parameters
    ----------
    z_intp : TYPE
        DESCRIPTION.
    z : TYPE
        DESCRIPTION.
    serie : TYPE
        DESCRIPTION.
    type_intp : TYPE, optional
        DESCRIPTION. The default is 'linear'.

    Returns
    -------
    serie_intp : TYPE
        DESCRIPTION.

    """
    
    serie_f = interp1d(z, serie, type_intp, bounds_error=False)
    serie_intp = serie_f(z_intp)
    
    return serie_intp



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
yi = 2015
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

        date_str = date.strftime('%Y%m%d')
        
        # Extract data date
        df = dfold.loc[date]
        
        # Check if height is monotonic increasing. If is not monotonic, remove
        # rows associated to those data
        if (df.GPHeight.is_monotonic_increasing and df.GPHeight.is_unique):
            pass
        else:
            df = remov_desc(df)

        
        #Lecture of Data
        GPHeight = df.GPHeight.copy()*10**-3
        Pressure = df.Pressure.copy()
        O3PartialPressure = df.O3PartialPressure.copy()
        Temperature = df.Temperature.copy()
        RelativeHumidity = df.RelativeHumidity.copy()
        Wind_Speed = df.WindSpeed.copy()
        Wind_Direction = df.WindDirection.copy()
        
        # Remove ozone data not valid
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
        Wind_interp = np.sqrt(U_interp**2+V_interp**2)
        Wind_Direction_interp = np.arctan2(V_interp, U_interp) * (180/np.pi)
        Wind_Direction_interp[Wind_Direction_interp<0] = Wind_Direction_interp[Wind_Direction_interp<0] + 360
        Mixing_Ratio_interp = interp_serie(z, GPHeight, Mixing_Ratio)
        
        # Interpolate ozone if profile is valid
        if df_validate.Valid[date]==0:
            O3_ppbv_interp=np.nan*np.zeros(len(z))
            O3PartialPressure_interp = np.nan*np.zeros(len(z))
            Sum_Omega_S = np.nan*np.zeros(len(z))
        else:
            O3_ppbv_interp = interp_serie(z, GPHeight, O3_ppbv)
            O3PartialPressure_interp = interp_serie(z, GPHeight, O3PartialPressure)
            Sum_Omega_S_interp = interp_serie(z, GPHeight, Sum_Omega_S)
        
        # Make dataframe with variables
        df_clear = pd.DataFrame(data={'Pressure':Pressure_interp,'Temp':Temperature_K_interp, 
                                      'RH':RelativeHumidity_interp, 'O3_mba': O3PartialPressure_interp,
                                      'O3_ppbv':O3_ppbv_interp, 'O3_column':Sum_Omega_S_interp,
                                      'U':U_interp, 'V':V_interp, 'Theta':T_potencial_interp,
                                      'Theta_e':T_potencial_e_interp, 'Mixing_Ratio':Mixing_Ratio_interp}, 
                                index=z)
        df_clear.index.rename('Alt', inplace=True)
        
        # Round values in dataframe
        df_clear = df_clear.round(2)
        df_clear.index = np.around(df_clear.index, 1)
        
        # Save individual file per ozonesonde
        df_clear.to_csv(path+'/'+'Data_Interpolate/'+'_RapaNui_'+date_str+'.csv')
        
        
        # Add ozonesonde to dataframe 
        df_clear2 = df_clear.copy()
        
        N = len(z)
        time = []
        for i in range(N):
            time.append(date)
        time = pd.to_datetime(time)
        time.name ='Datetime'
        
        df_clear2.set_index([time, df_clear2.index], inplace=True)
        
        # Add to dataframe complete
        dfold_clear = pd.concat([dfold_clear, df_clear2])
        
        #break        
    
# Save in .csv all ozonesondes interpolated
dfold_clear.to_csv(path+'/'+'RapaNui_all_clear.csv')
