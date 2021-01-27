#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 13:53:36 2021

@author: sebastian
"""

import matplotlib.pyplot as plt
import pandas as pd
from glob import glob
import os
import csv
import chardet


path = os.getcwd()# use your path

def lecture(filename):
    
    # Buscar tipo de encode del archivo
    with open(filename, 'rb') as file:
        enc=chardet.detect(file.read())['encoding']

    
    # Buscar lineas a saltar del header para leer datos del archivo.
    # Tambien busca fecha y hora de lanzamiento del sondeo en el archivo
    with open(filename, 'r', encoding=enc) as file:
        reader = csv.reader(file, delimiter=',')
             
        iline = 0
        for row in reader:
            if row == []:
                pass
            elif row[0] == 'UTCOffset':
                date = next(reader)[1:3]
                fecha = date[0]
                hora = date[1]
                fechahora = date[0] + ' ' + hora
            elif row[0] == '#PROFILE' or row[0] == '#PROFILE ':
                iline += 2
                break
            iline += 1
    
    # Cargar mediciones del sonde en dateframe
    if fecha == '2008-7-5':
        # Excepcion para archivo del 2008-7-5, distinto encode y error en header
        rows = []
        rows.extend(range(iline))
        rows.extend(range(iline+1, iline+3))
        dataframes = pd.read_csv(filename, skiprows=rows, encoding=enc)
    else:
        dataframes = pd.read_csv(filename, skiprows=iline)
    
    # Crear vector de tiempo, con el tiempo de lanzamiento para agregar index
    # a dateframes
    N = dataframes.shape
    time = []
    for i in range(N[0]):
        time.append(fechahora)
    time = pd.to_datetime(time)
        
    dataframes.index = time
    
    
    # Renombrar columnas que estan mal ordenadas
    badfiles = ['2008-1-12', '2008-1-30', '2008-4-4', '2008-5-9', '2008-5-30',
                '2008-7-5', '2008-7-19', '2008-7-25', '2008-9-5', '2008-9-12',
                '2008-10-17', '2008-10-24', '2008-12-29']
    
    if fecha in badfiles:
        dataframes.rename(columns={'WindSpeed' : 'GPHeight', 'WindDirection' : 'RelativeHumidity',
                                  'GPHeight' : 'WindSpeed', 'RelativeHumidity' : 'WindDirection'},
                          inplace=True)
    

    
    # Extraer variables a ocupar
    if 'WindSpeed' in dataframes.keys():
        # Si el archivo tiene datos de viento
        variables = ['GPHeight','Pressure', 'Temperature', 'RelativeHumidity',
                      'O3PartialPressure', 'WindSpeed', 'WindDirection']
    else:
        # Si el archivo no tiene datos de viento
        variables = ['GPHeight','Pressure', 'Temperature', 'RelativeHumidity',
                      'O3PartialPressure']
        
    dataframes = dataframes[variables]
    
    
    return dataframes    

    

# Cargar los nombres de todos los archivos en las carpetas
filenames = []
for year in range(1995, 2020):
    filenames += glob(path + "/"+str(year)+"/"+str(year)+"*.csv")
# Ordena todos los archivos segun sus fechas, archivos con nombres yyyymmdd.*.csv
filenames.sort()

# cargar todos los datos de ozonosondas en mismo dateframe
dfold = pd.DataFrame()
for filename in filenames:
    print(filename)
    df = lecture(filename)
    dfold = pd.concat([dfold, df])

dfold.to_csv(path+'/'+'ozonesondes-1995-2019'+'.csv')
# fig1 = plt.figure(1)
# ax1 = fig1.add_subplot(111)
# ax1.plot(dfold.O3PartialPressure, dfold.GPHeight, ",")    
# ax1.set_xscale('log')
# ax1.plot()
# agrupar datos por dia
#DFList = []
#for group in dfold.groupby(dfold.index):
#    DFList.append(group[1])