# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 18:29:03 2020

@author: laura Gallardo, Camilo Menares and Charlie Opazo

Reading and saving Tololo ozone data. Except for removing negative values, and strange values,
no cleansing or resampling is applied to the data.

Data for the period 2013-2020 was downloaded from http://ebas.nilu.no/
This set corresponds to hourly averaged values

Data for the period 1995-2013 was obtained from the Chilean Meteorological Office
thanks to Dr. Carmen Vega (carmen.vega@dgac.gob.cl) and colleagues

Last updated jan 4 2021, LGK
"""


#Importing libraries

import pandas as pd              # Data structures
import matplotlib.pyplot as plt  # Plotting 
import os as os                  # Directory management    
import numpy as np               # Numerics   
import datetime
from pathlib import Path

#Reading data downloaded from  http://ebas.nilu.no/
#Hourly averages


def leer_ebas(inicio,fin):
    """    
    Parameters
    ----------
    inicio : string
        Start date of file '20130101'
    fin : TYPE
        End date of file'20140101'
    spec: string
          Reads ozone 1 hour average and standard deviation
    Returns
    -------
    df : Dataframe containing O3 in ppbv and its standard deviation (hourly values)
       Data downloaded from
        http://ebas.nilu.no/Pages/DataSetList.aspx?key=A4C1704036474C47AED6FA75E2A99882.
        The data format is described in (NASA Ames 1001).: 
        https://cloud1.arc.nasa.gov/solve/archiv/archive.tutorial.html
            

    """
    
    #Data to be read
    #From the accompanying information file
    # Data structure
    #[8760 rows x 7 columns]>
    #starttime     endtime        O3    O3.1     O3.2   O3.3   flag
    #where
    # O3 is ozone, ug/m3, Statistics=arithmetic mean, 
    # O3.1 ozone, nmol/mol, Statistics=arithmetic mean, 
    # O3.2 ozone, ug/m3, Statistics=stddev, 
    # O3.3 ozone, nmol/mol, Statistics=stddev, 
    #
    
    orig = os.getcwd() #Says where the current file is
    datadir=orig+'\\DATA\\DB-EBAS\\' 
    
    if inicio=='20190101':
        name_data = 'CL0001R.'+inicio+'000000.20200630060000.uv_abs.ozone.air.1y.1h.CL01L_TEI49C_no72417371.CL01L_uv_abs.lev2.nas' # Define el nombre de los archivos a leer
    else:
        name_data = 'CL0001R.'+inicio+'000000.20201102112043.uv_abs.ozone.air.1y.1h.CL01L_TEI49C_no72417371.CL01L_uv_abs.lev2.nas'
   
    tiempo = pd.date_range(inicio,fin, freq= 'H')                                   
    input_data = pd.read_csv(datadir+ name_data,decimal=".", delimiter=r"\s+", header =76);  # lectura de datos
  
    
    input_data = input_data.rename(columns={input_data.keys()[2]: "O3_ug/m3", input_data.keys()[3]: "O3_ppbv",
                               input_data.keys()[4]: "O3_ug/m3_std" , input_data.keys()[5]: "O3_ppbv_std", 
                               input_data.keys()[6]: "flag"})                        # Redefine las columnas del dataframe
    

    # Replacing non values by NaN
    
               
    input_data["O3_ppbv"].replace(999.99, np.nan, inplace=True)
    input_data["O3_ppbv_std"].replace(99.99, np.nan, inplace=True)
    input_data["O3_ppbv_std"].replace(999.99, np.nan, inplace=True)

    # Generating indexed time series
    
          
    O3_ppbv = pd.Series(input_data["O3_ppbv"].values, index=tiempo[0:-1])
    O3_ppbv_2 = pd.Series(input_data["O3_ppbv_std"].values, index=tiempo[0:-1])

    
    df = pd.DataFrame({ "O3_ppbv" : O3_ppbv, "O3_ppbv_std" : O3_ppbv_2 })

    #There are repeated dates in this data set
    
    # Finding and removing dates (index) repeated 
    df = df.iloc[~df.index.duplicated(keep='first')]


    return df                   



#Reading data provided by DMC 
#15 min averages on yearly files


def leer_dmc(inicio,fin,tipo):
    """    
    Parameters
    ----------
    inicio : string
        Start date of file, e.g., '20130101'
    fin : TYPE
        End date of file, e.g., '20140101'
    tipo: indicates type of data structure either 118 or 119
    
    118 is organized as 24 columns indicating:
    1) Array Identifier; 
    2) Julian Day; 
    3) Standard Time; 
    4) Station ID; 
    5) Battery Voltage; 
    6) Wind speed (m/s); 
    7) Wind Direction (0-360°);
    8) Average internal temperature (C); 
    9) Average ambient temperature(C);
    10) Average relative humidity(%); 
    11) Average solar radiation licor (W/m2);
    12) Average solar radiation diffuse Kipp-Zonen(W/m2);
    13) Average solar radiation incident Kipp-Zonen(W/m2);
    14) Average net radiation Shenk (W/m2);
    15) Average UV-B radiation Yankee-Erythermal (mW/m2)
    16) Average UV-B radiation Yankee Total UV-B (mW/m2)
    17) Average pressure (mb); 
    18) Average ozone (ppb)[possibly v]
    19) Total precipitation (mm)); 
    20) Standard deviation of wind speed (m/s))
    21) Average wind speed (m/s); 
    22) Average wind vector magnitude; 
    23) Average wind vector direction; 
    24) Standard deviation of wind direction
    
    119 is organized as 31 columns indicating:
    1) Array Identifier; 
    2) Year; 
    3) Julian Day; 
    4) Standard Time; 
    5) Station ID;
    6) Signature;
    7) Battery Voltage; 
    8) Instantaneous solar radiation licor (W/m2);
    9) Instantaneous solar radiation diffuse Kipp-Zonen(W/m2);
    10) Instantaneous solar radiation incident Kipp-Zonen(W/m2);
    11) Instantaneous net radiation Shenk (W/m2);
    12) Instantaneous UV-B radiation Yankee-Erythermal (mW/m2)
    13) Instantaneous UV-B radiation Yankee Total UV-B (mW/m2)
    14) Average internal temperature (C); 
    15) Average ambient temperature(C);
    16) Average relative humidity(%);
    17) Average solar radiation diffuse Kipp-Zonen(W/m2);
    18) Average solar radiation incident Kipp-Zonen(W/m2);
    19) Average net radiation Shenk (W/m2);
    20) Average UV-B radiation Yankee-Erythermal (mW/m2)
    21) Average UV-B radiation Yankee Total UV-B (mW/m2)
    22) Average pressure (mb); 18) Average ozone (ppb)[possibly v]
    23) Average pressure (mb)    
    24) Average ozone (ppb) 
    25) Total precipitation (mm)); 
    26) Standard deviation of wind speed (m/s))
    27) Standard deviation of ozone (ppb)
    28) Average wind speed (m/s))
    29) Average wind vector magnitude; 
    30) Average wind vector direction; 
    31) Standard deviation of wind direction
     
    Returns
    -------
    df : Dataframe containing ozone in ppbv and relative humidity (15 min average)
    
    Data for the period 1995-2013 was obtained from the Chilean Meteorological Office
    thanks to Dr. Carmen Vega (carmen.vega@dgac.gob.cl) and colleagues
        

    """
    
        #Data to be read
    #From the accompanying information file
    # Data structure
    # Accordin to "tipo" 118 or 119

    orig = os.getcwd() #Says where the file is
    datadir=orig +'\\DATA\\DB-DMC\\'
    #datadir=orig +'/Data/'

    if inicio=='1997': 
        if tipo==118:
            name_data='ET'+inicio+'_1'+'.csv'
        elif tipo==119:
            name_data='ET'+inicio+'_2'+'.csv'
    else:
        name_data='ET'+inicio+'.csv'
        
    
        
#The file contains strange characters    

    if tipo==118:
        input_data = pd.read_csv(datadir+ name_data,decimal=",", delimiter=r";", header =0, na_values= ['?' , 'c '])  # lectura de datos
    elif tipo==119:
        input_data = pd.read_csv(datadir+ name_data,decimal=",", delimiter=r";", header =0, na_values= '?')
        # In year 2013 the columns don't have labels
        if inicio=='2013':
            input_data = pd.read_csv(orig+'\\DATA\\DB-DMC\\'+'ET2013.csv', decimal=",", delimiter=r";", na_values= '?',header = None)
            for i in range(31):
                input_data = input_data.rename(columns={input_data.keys()[i]: str(i+1)})
    #Renaming column names
    if tipo==118:
        input_data = input_data.rename(columns={input_data.keys()[9]: "RH_perc",input_data.keys()[17]: "O3_ppbv"})                            
    elif tipo==119:
        input_data = input_data.rename(columns={input_data.keys()[15]: "RH_perc",input_data.keys()[23]: "O3_ppbv"})
        
    #Changing dates
        
    if tipo==118:
        j = input_data['2']  # Julian Day
        h_aux = input_data['3']
    elif tipo==119:
        j = input_data['3']  # Julian Day
        h_aux = input_data['4']
        
        
    # Make date string 
    fecha_str = [inicio +'-'+ str(d) for d in j]
    fecha = pd.to_datetime(fecha_str, format='%Y-%j')
    
    dhora_str = [str(hi // 100).zfill(2) + ':' + str(hi % 100).zfill(2) 
                 + ':00' for hi in h_aux]
    dhora = pd.to_timedelta(dhora_str)
    
    tiempo = fecha + dhora
    

    # tiempo=pd.DatetimeIndex(vector_t)
    
    # Generating time indexed series
    
    O3_ppbv = pd.Series(input_data["O3_ppbv"].values, index=tiempo)
    RH_perc = pd.Series(input_data["RH_perc"].values, index=tiempo)

        
    # Forma estructura dataframe final
        
   
    df = pd.DataFrame({ "O3_ppbv" : O3_ppbv, "RH_perc" : RH_perc })
   
    return df

############################READING AND SAVING##############
#Reading DMC data 1995-2012
dfold = pd.DataFrame()

#From 1995 to 1996
for i in range(1995,1997):
    var=leer_dmc(str(i),str(i+1),118) 
    dfold = pd.concat([dfold,var])
    
# 1997 tewo sections
var=leer_dmc('1997','1998',118)
dfold = pd.concat([dfold,var])

var=leer_dmc('1997','1998',119)
dfold = pd.concat([dfold,var])
#1998 on
for i in range(1998,2013):
    var=leer_dmc(str(i),str(i+1),119)
    dfold = pd.concat([dfold,var])

#
var = leer_dmc('2013','2013',119).astype(float)
dfold = pd.concat([dfold,var])

# Finding and removing dates (index) repeated
data_old = len(dfold)
dfold = dfold.iloc[~dfold.index.duplicated(keep='first')]
data_new = len(dfold)
clear_data = data_old - data_new
#Removing negative values
dfold[dfold < 0] = np.nan
#Removing values over 1000
dfold[dfold>1000] = np.nan
data_new_no_negative = len(dfold)
clear_data_no_negative = data_new - data_new_no_negative
all_clear_data = clear_data_no_negative + clear_data
#Se re-indexan datos cada 15 minutos
dfdmc_O3_RH_15m = dfold.resample('15min').mean()

#Reading EBAS data 2013-2020
df_2013 = leer_ebas('20130101','20140101')
df_2014 = leer_ebas('20140101','20150101')
df_2015 = leer_ebas('20150101','20160101')
df_2016 = leer_ebas('20160101','20170101')
df_2017 = leer_ebas('20170101','20180101')
df_2018 = leer_ebas('20180101','20190101')
df_2019 = leer_ebas('20190101','20200101')
# Concatena datos
dfebas_O3H = pd.concat([ df_2013 ,  df_2014, df_2015 , df_2016 , df_2017, df_2018, df_2019])


#Saving data frames
    
orig = os.getcwd() #Says where the file is 
ruta=orig+'\\DATA\\'
dfebas_O3H.to_csv(ruta+'EBAS-O3H-2013-2019'+'.csv')
dfdmc_O3_RH_15m.to_csv(ruta+'DMC-O3_RH_15m_dmc-1995-2013'+'.csv')



