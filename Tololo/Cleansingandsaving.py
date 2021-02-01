# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 13:01:43 2020

@author: laura Gallardo & Camilo Menares

Reads, cleans and samples TOLOLO data 
Data --ozone only--for the period 2013-2020 were downloaded from http://ebas.nilu.no/
This set corresponds to hourly averaged values

Data (ozone, water vapor, radiation, wind, etc)for the period 1995-2013
were obtained from the Chilean Meteorological Office
thanks to Dr. Carmen Vega (carmen.vega@dgac.gob.cl) and colleagues
"""



#Importing libraries

import pandas as pd              # Data structures
import matplotlib.pyplot as plt  # Plotting
import os as os                  # Directory management
import numpy as np               # Numerics
import datetime
from datetime import date
from datetime import timedelta
from datetime import datetime as dt
import info_Plotting  #Import key settings for the following graphs and data
# Libreria creada para definir las rutas y los string de los Modelos
from info_Plotting import FHIST
from info_Plotting import FHIST2
from info_Plotting import FSERIES
from pathlib import Path



#Exploring EBAS data
# The following file was read using Readingandsaving.py
# It consists of a dataframe containg hourly values of ozone and the corresponding 
# standard deviation

# The ozone sensor is a refur-bished ozone photometer (Thermo Scientific, TE49c) since 2013
# see Anet et al, 2017 doi:10.5194/acp-17-6477-2017 for details, including
# https://acp.copernicus.org/articles/17/6477/2017/acp-17-6477-2017-supplement.pdf
# See https://assets.thermofisher.com/TFS-Assets/EPM/manuals/EPM-manual-Model%2049i.pdf
# 
#Thus 
# Response time: 20s with 10s lag
# Precision: 1ppbv
# Selectable Full Scale Range: 0.05--200 ppm or 0.1--400 mg/m^3
# Lower limit of detection: 1.0ppb (zero noise 0.5 ppb RMS)


orig = os.getcwd() #Says where the file is
fn = orig+'\\DATA\\'+'EBAS-O3H-2013-2019.csv'
df = pd.read_csv(fn, parse_dates=True, index_col=0)
df.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)

df_orig_ebas = df #Original EBAS data set

# # Plotting time series
FSERIES('O3', 'EBAS', df, 1) #PENDING TIME AXES

# #Creating histograms of data
# #FHIST(spec,dbname,df,Nbins, ext=None)
FHIST('O3', 'EBAS', df, 50) #PENDING Anchored text


# #These data ave been subject to evaluation we do not "clean"

# dfH_ebas=df

############################
#Exploring DMC data
# The following file was read using Readingandsaving.py
# It consists of a dataframe containg hourly values of ozone and the corresponding 
# standard deviation
orig = os.getcwd() #Says where the file is
#fn=orig+'/Data/'+'DMC-O3_RH_15m_dmc-1995-2012'  # cambiar fn linea inferior
fn = orig+'\\DATA\\'+'DMC-O3_RH_15m_dmc-1995-2013.csv'

df = pd.read_csv(fn,index_col=0,parse_dates=True) 
#df.rename(columns = {'Unnamed: 0':'Date'}, inplace = True)
df_orig_dmc = df  #Original time series, before cleansing


#Plotting time series

FSERIES('O3', 'DMC', df, 1) #PENDING TIME AXES
#FHIST('O3', 'DMC', df, 50)
def clean_series_demo(Min, Max, df):
    """
    Parameters
    ----------
    Min : float
        Minimum value of ozone to filter.
    Max : float
        Maximum value of ozone to filter.
    df : DataFrame
        Contains the data of ozone measurements in Tololo station.

    Returns
    -------
    The function lets try some values to filter the time series of ozone in
    Tololo station and compare with the instrument limit detection, M.Schultz
    filter and J.Anet filter.
    The function returns the mean and std of time series.
    """
    a = df.copy()
# The ozone sensor was a TECO  49-003  analyzer, between 1995-2013
# see Anet et al, 2017 doi:10.5194/acp-17-6477-2017 for details
# https://www.eol.ucar.edu/instruments/thermo-environmental-instruments-model-49-ozone-analyzer
#Thus 
# Response time: 20s with 10s lag
# Precision: 1ppbv
# Selectable Full Scale Range: 0.05--200 ppm or 0.1--400 mg/m^3
# Lower limit of detection: 1.0ppb (zero noise 0.5 ppb RMS)
# Other measurement characteristics (comments on signal/noise, bias limits, etc)

#Removing values below detection limit or the assumed range of calibration, i.e. 5 ppbv

    a.O3_ppbv[a.O3_ppbv < Min] = np.nan

# # WARNING
# See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
#   df.O3_ppbv[df.O3_ppbv <5] = np.nan
# C:\Users\laura\Desktop\DataVis\TOLOLO\Cleansingandsaving.py:100: SettingWithCopyWarning: 
# A value is trying to be set on a copy of a slice from a DataFrame

#The time series evidences calibration spikes. In lack of the record of dates of calibration, 
# we remove values above 65 ppbv, considering the data distribution of EBAS hourly values

    a.O3_ppbv[a.O3_ppbv > Max] = np.nan
    FSERIES('O3', 'DMC', a, 1)
    FHIST2('O3', 'DMC', a, 50)
    series = a.O3_ppbv
    mean = series.mean()
    std = series.std()
    return mean, std
def clean_series(Min, Max, df):
    """
    Parameters
    ----------
    Min : float
        Minimum value of ozone to filter.
    Max : float
        Maximum value of ozone to filter.
    df : DataFrame
        Contains the data of ozone measurements in Tololo station.
    Returns
    -------
    TYPE
        The function apply a filter to the time series for values less than Min
        and higher values than Max. The function returns the number of
        filtered data.

    """
    inf = df.O3_ppbv < Min
    df.O3_ppbv[inf] = np.nan
    sup = df.O3_ppbv > Max
    df.O3_ppbv[sup] = np.nan
    return inf.sum() + sup.sum()
#clean_series(min_filter, max_filter, df)
#sum_first_filter = clean_series(5, 65, df)


def clean_near(df, n, c):
    """

    Parameters
    ----------
    df : Dataframe
        DESCRIPTION.
    n : int
        DESCRIPTION.
    c : float
        DESCRIPTION.
    d : float
        DESCRIPTION.

    Returns
    -------
    list
        DESCRIPTION.

    """

    df_2 = df.copy()
    df_movil = df.rolling(window=n).mean()
    first_hour = dt.strptime(str(df_movil.index[0]), '%Y-%m-%d %H:%M:%S')
    last_hour = dt.strptime(str(df_movil.index[-1]), '%Y-%m-%d %H:%M:%S')
    first_hour_des = first_hour + datetime.timedelta(minutes=15)
    last_hour_des = last_hour + datetime.timedelta(minutes=15)
    hour_mod = pd.date_range(str(first_hour_des), str(last_hour_des),
                             freq='15min')
    df_mod = pd.DataFrame({'O3_ppbv': df_movil.O3_ppbv.values}, index=hour_mod)
    index_sup = (c*df_mod) - df < 0
    df_2[index_sup] = np.nan
    supr_date_1 = index_sup.sum()
    index_sup = ((c-1)*df_mod) - df > 0
    df_2[index_sup] = np.nan
    supr_date_2 = index_sup.sum()

    return [df_2, supr_date_1, supr_date_2]
df = clean_near(df, 3 , 1.5)[0]
#Removing values under 5 ppbv
df[df <5] = np.nan
#Removing values over 100 ppbv
df[df >100] = np.nan
# función que permite calcular las medias horarias para un intervalo con
# una cierta cantidad de datos
def completitud(df, n, frec):
    """
    Parameters
    ----------
    df : DataFrame, contiene la información de las mediciones.
    n : int, número de datos mínimo que debe contener el intervalo de tiempo 
        para calcular la media.
    frec : str, indica la frecuencia de los datos a promediar.

    Returns
    -------
    list
        Entrega una lista con un DataFrame con los datos promediados en el 
        intervalo de tiempo sugerido y un conteo de los datos no considerados.
    """
    bad_mean = np.isnan(df.O3_ppbv).astype(int).resample(frec).sum()
    m = np.isnan(df.O3_ppbv).astype(int).resample(frec).sum().max()
    good_mean = bad_mean > m-n
    count_bad = good_mean.sum()
    df_hourly = df.resample(frec).mean()
    df_hourly[good_mean] = np.nan
    return [df_hourly, count_bad]
# Data frame que permite ver los cambios para el cálculo de promedios horarios
# con 3 o mas mediciones en una hora     
df2 = completitud(df,3,'H')[0] 
FSERIES('O3', 'DMC', df, 1)
#grafico del dataframe mencionado anteriormente
FSERIES('O3', 'DMC', df2, 1)

#PENDING TIME AXES

orig = os.getcwd()

fn=orig+'\\DATA\\'+'DMC-O3_RH_1H_dmc-1995-2013_clear.csv'
#fn=orig+'/Data/DMC-O3_RH_15m_dmc-1995-2012_clear'
df2.to_csv(fn)


#Creating histograms of data
#FHIST(spec,dbname,df,Nbins, ext=None)
#FHIST('O3', 'DMC', df, 50) #PENDING Anchored text




#Resamplig to hourly values and calculating the corresponding standard deviation

# dfH=df.resample('H').mean()
# dfstd=df.resample('H').std()
#ERROR: COMPLAINS
# C:\Users\laura\Desktop\DataVis\TOLOLO\Cleansingandsaving.py:100: SettingWithCopyWarning: 
# A value is trying to be set on a copy of a slice from a DataFrame

# See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
#   df.O3_ppbv[df.O3_ppbv > 68] = np.nan
# C:\Users\laura\anaconda3\lib\site-packages\numpy\lib\histograms.py:839: RuntimeWarning: invalid value encountered in greater_equal
#   keep = (tmp_a >= first_edge)
# C:\Users\laura\anaconda3\lib\site-packages\numpy\lib\histograms.py:840: RuntimeWarning: invalid value encountered in less_equal
#   keep &= (tmp_a <= last_edge)
# Traceback (most recent call last):

#   File "C:\Users\laura\Desktop\DataVis\TOLOLO\Cleansingandsaving.py", line 112, in <module>
#     dfH=df.resample('H').mean()

#   File "C:\Users\laura\anaconda3\lib\site-packages\pandas\core\generic.py", line 8115, in resample
#     level=level,

#   File "C:\Users\laura\anaconda3\lib\site-packages\pandas\core\resample.py", line 1270, in resample
#     return tg._get_resampler(obj, kind=kind)

#   File "C:\Users\laura\anaconda3\lib\site-packages\pandas\core\resample.py", line 1404, in _get_resampler
#     "Only valid with DatetimeIndex, "

# TypeError: Only valid with DatetimeIndex, TimedeltaIndex or PeriodIndex, but got an instance of 'RangeIndex'

#Creating data series of hourly ozone and corresponding standard deviation

# Edite una prueba
#df.resample('15min').mean()
#horas_aux=pd.date_range('1995-11-09 18:15:00','2013-04-24 15:15:00',freq = '15min') hora desfasada promedio movil en 15 min