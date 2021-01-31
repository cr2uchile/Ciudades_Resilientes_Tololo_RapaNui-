#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 13:42:02 2021

@author: sebastian
"""
from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
from glob import glob
import os
import csv
import chardet
path = os.getcwd()
dfold = pd.read_csv(path+'/'+'ozonesondes-1995-2019'+'.csv', parse_dates=True, index_col=0)
df_2 = pd.read_csv(path+'/'+'Validacion_Rapa_nui.csv', parse_dates=True, index_col=0)
df_validate= pd.read_csv(path+'/'+'dates_valid_ozonesondes-1995-2019'+'.csv',  parse_dates=True, index_col=0) 
R=8.314472; #(J/(mol K))
Cp=29.19; #(J/(mol K))
yi = 2015
yf = 2019
dates = df_validate.index
def monotomic(series):
    for i in range(1, len(series)-1):
        output = series[:i]<series[i+1]
    return output     
for date in dates:
    
    if date.year in range(yi, yf+1):
        date = dates[-1]
        date_str = date.strftime('%Y-%m-%d')
        df = dfold[dfold.index==date]
        
        #Lecture of Data
        Pressure = df.Pressure.values
        O3PartialPressure = df.O3PartialPressure.values
        Temperature = df.Temperature.values
        RelativeHumidity = df.RelativeHumidity.values
        Wind_Speed = df.WindSpeed.values
        Wind_Direction = df.WindDirection.values
        Temperature_K = Temperature + 273.15
        #Determination of diferent'
        GPHeight = df.GPHeight*10**-3
        O3_ppbv = (O3PartialPressure*10**-3)/ (Pressure*10**2)*10**9
        T_potencial = (Temperature+273.15)*(1000/Pressure)**(R/Cp)
        U = - Wind_Speed*np.cos((np.pi/180)*Wind_Direction) 
        V = - Wind_Speed*np.sin((np.pi/180)*Wind_Direction)
        Satured_Vapor_Pressure = 6.11*np.exp(5.42*10**3*(1/273-1/(Temperature+273.15)))
        Satured_Mixing_Ratio = 0.622*(Satured_Vapor_Pressure/(Pressure-Satured_Vapor_Pressure))
        Mixing_Ratio = (RelativeHumidity/100)*Satured_Mixing_Ratio
        T_potencial_e = ((Temperature+273.15)*(1+0.061*Mixing_Ratio))*(1000/Pressure)**(R/Cp)
        Omega_S = np.zeros(len(GPHeight))
        #Omega_R = 7.8899* Pressure[-1]
        Sum_Omega_S = np.nan*np.zeros(len(GPHeight))
        for i in range(len(GPHeight)-1):
            Omega_S[i] =  3.9449*(O3PartialPressure[i]+O3PartialPressure[i+1])*np.log(Pressure[i]/Pressure[i+1])
            a = np.nansum(Omega_S)
            Sum_Omega_S[i] = a
        #agregar columna de ozono()
        #Interpolación de distintas variables
        z = np.arange(0,35, 0.1)
        Pressure_interp = np.interp(z, GPHeight, Pressure)
        Temperature_interp = np.interp(z, GPHeight, Temperature)
        Temperature_K_interp = np.interp(z, GPHeight, Temperature_K)
        RelativeHumidity_interp = np.interp(z, GPHeight, RelativeHumidity)
        T_potencial_interp = np.interp(z, GPHeight, T_potencial)
        T_potencial_e_interp = np.interp(z, GPHeight, T_potencial_e)
        U_interp = np.interp(z, GPHeight, U)
        V_interp = np.interp(z, GPHeight, V)
        Wind_interp = np.sqrt(U_interp**2+V_interp**2)
        Mixing_Ratio_interp = np.interp(z, GPHeight, T_potencial_e)
        
    
        if df_validate.Valid[date]==0:
            O3_ppbv_interp=np.nan*np.zeros(len(z))
            O3PartialPressure_interp = np.nan*np.zeros(len(z))
            Sum_Omega_S = np.nan*np.zeros(len(z))
        else:
            O3_ppbv_interp = np.interp(z, GPHeight, O3_ppbv)
            O3PartialPressure_interp = np.interp(z, GPHeight, O3PartialPressure)
            Sum_Omega_S_interp = np.interp(z, GPHeight, Sum_Omega_S)
        #Wind_Direction_interp = np.arctan2(V_interp/U_interp)*(180/np.pi)
        #Wind_Direction_interp[Wind_Direction_interp<0] +=360
        df_clear = pd.DataFrame(data={'Pressure':Pressure_interp,'Temp':Temperature_K_interp, 
                                      'RH':RelativeHumidity_interp, 'O3_mba': O3PartialPressure_interp,
                                      'O3_ppbv':O3_ppbv_interp, 'O3_column':Sum_Omega_S_interp,
                                      'U':U_interp, 'V':V_interp, 'Theta':T_potencial_interp,
                                      'Theta_e':T_potencial_e_interp, 'Mixing_Ratio':Mixing_Ratio_interp}, index=z)
        df_round= df_clear.round(2)
        df_round[df_round.index<min(GPHeight)]=np.nan
        df_round[df_round.index>max(GPHeight)]=np.nan
        df_round.to_csv(path+'/'+date_str+'_Rapa_Nui_interp'+'.csv')
        break        
        
# df_clear = pd.DataFrame()

# df_clear = pd.DataFrame(data={'Pressure':Pressure_interp}, 
#                         index=dates)
# Pressure = df[i].Pressure 
        # O3PartialPressure = df[i].O3PartialPressure
        # Temperature = df[i].Temperature
        # RelativeHumidity = df[i].RelativeHumidity
        # GPHeight = df[i].GPHeight*10**-3
        # z = np.arange(0,35, 0.1)
        # Pressure_interp = np.interp(z, GPHeight, Pressure)
        # O3PartialPressure_interp = np.interp(z, GPHeight, O3PartialPressure)
        # Temperature_interp = np.interp(z, GPHeight, Temperature)
        # RelativeHumidity_interp = np.interp(z, GPHeight, RelativeHumidity)
        # O3_ppbv = (O3PartialPressure_interp*10**-3)/ (Pressure_interp*10**2)*10**9


# #quitar horas minutos y segundos 
# df.index = df.index.normalize()
# df_validate.index = df_validate.index.normalize()
# for i in df_validate.index:
#     if df_validate.Validado[i]==0:
#         df[df.index==i]=np.nan

