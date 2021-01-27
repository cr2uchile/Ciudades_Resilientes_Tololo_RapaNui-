#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 13:53:36 2021

@author: sebastian
"""


import pandas as pd
from glob import glob
import os
# año 1995 n = 56
# año 1996 n = 54
# año 1997 n = 54
# año 1998 n = 44
# archivo 2004  05 22 viene con error el nombre del archivo, corrección a mano 
# año 2004 n = 42
# año 2005 n = 44
# año 2006 n = 44
# año 2007 n = 44
# año 20080705 viene con presión,etc. caso especial
#año  2008 n = 44
# año 2009 n = 25
# año 2010 n = 25
# año 2011 n = 25
# año 2012 n = 25
# año 2013 n = 25
# año 2014 n = 25
# año 2015 n = 25
# año 2016 n = 25
# año 2018 n = 25
# año 2019 n = 25
path = os.getcwd()# use your path
#archivos con desfase
dir_2004 = path + '/2004/20040313.ECC.na.na.EIMO.csv'
#archivos con desfase
dir_2008 = path + '20080705.ECC.na.na.EIMO.csv_datefix.csv'
dir_2019 = path + '/2019/20190427.ECC.6a.na.EIMO.csv'
def lecture(year, n):
    filenames = glob(path + "/"+str(year)+"/"+str(year)+"*.csv")
    filenames.sort()
    if year==2004:
        dataframes = []
        for i in range(len(filenames)):
            if filenames[i] == dir_2004:
                dataframes.append(pd.read_csv(dir_2004, skiprows = 44))
            else:
                dataframes.append(pd.read_csv(filenames[i], skiprows = n))   
    if year==2008:
        dataframes = []
        for i in range(len(filenames)):
            if filenames[i] ==dir_2008:
                dataframes.append(pd.read_csv(dir_2008, skiprows = [46]))
            else:
                dataframes.append(pd.read_csv(filenames[i], skiprows = n))  
    else:            
        dataframes = [pd.read_csv(f, skiprows = n) for f in filenames]
    for i in range(len(filenames)):
        #nombre a fecha 
        f = filenames[i][64:68] + '-'+ filenames[i][68:70] + '-'+ filenames[i][70:72]
        #se agregan estas dos horas provisorias
        f1 = f + ' ' + '17:00:00'
        f2 = f + ' ' + '20:00:00'
        #tener la misma fecha n-veces veces
        dates = pd.date_range(f1,f2, len(dataframes[i]))
        dataframes[i].index = dates
    return dataframes    

dfold = pd.DataFrame()
#Reading data 1995
df = pd.concat(lecture(1995,56))
dfold = pd.concat([dfold,df])
#Reading data 1996-1997
for i in range(1996,1998):
    df = pd.concat(lecture(i,54))
    dfold = pd.concat([dfold,df])
#Reading data 1998
df = pd.concat(lecture(1998,44))
dfold = pd.concat([dfold,df])   
#Reading data 2004
df = pd.concat(lecture(2004,42))
dfold = pd.concat([dfold,df]) 
#Reading data 2005-2008
for i in range(2005,2008):
    df = pd.concat(lecture(i,44))
    dfold = pd.concat([dfold,df]) 

#Reading data 2009-2016
for i in range(2009,2017):
    df = pd.concat(lecture(i,25))
    dfold = pd.concat([dfold,df])     
#Reading data 2018    
df = pd.concat(lecture(2018,25))
dfold = pd.concat([dfold,df])     

#dfold contiene todos los datos 