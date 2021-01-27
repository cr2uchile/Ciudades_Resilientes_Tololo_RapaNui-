# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 14:51:56 2021

@author: Sebastián
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os as os
from datetime import date
from datetime import timedelta
from datetime import datetime as dt
import pandas as pd

orig_ebas = os.getcwd()
fn_ebas = orig_ebas+'\\DATA\\'+'EBAS-O3H-2013-2019.csv'
#leer la primera columna como datetime
df_ebas = pd.read_csv(fn_ebas, parse_dates=True, index_col=0)
df_ebas.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
df_orig_ebas = df_ebas

orig_dmc = os.getcwd()
fn_dmc = orig_dmc+'\\DATA\\'+'DMC-O3_RH_15m_dmc-1995-2013.csv'
df_dmc = pd.read_csv(fn_dmc, index_col=0, parse_dates=True)
df_orig_dmc = df_dmc

#extracción de datos utiles DMC
Fecha_dmc_2013 = df_orig_dmc['2013']
O3_dmc_2013 = Fecha_dmc_2013.O3_ppbv
#Promedio horario de mediciones
O3_dmc_2013_horario = O3_dmc_2013.resample("H").mean()
#Se aplica un filtro preliminar
O3_dmc_2013_horario[O3_dmc_2013_horario < 5] = np.nan
O3_dmc_2013_horario[O3_dmc_2013_horario > 65] = np.nan
#extracción de datos utiles EBAS
Fecha_dmc_2013 = df_orig_ebas['2013']
O3_ebas_2013 = Fecha_dmc_2013.O3_ppbv

fig1 = plt.figure(1)
fig1.clf()
ax1 = fig1.add_subplot(111)
ax1.plot(O3_dmc_2013_horario.index, O3_dmc_2013_horario, color='b',
         label='DMC Time Series')
ax1.set_ylabel('Mixing Ratio $O_{3}$ [ppbv]', fontsize=18)
ax1.set_xlabel('Date', fontsize=18)
ax1.set_title('Hourly Average of $O_{3}$ Mixing Ratio', fontsize=18)
ax1.legend()
fig1.show()

fig2 = plt.figure(2)
fig2.clf()
ax3 = fig2.add_subplot(111)
ax3.plot(O3_dmc_2013_horario.index, O3_dmc_2013_horario,
         label='DMC Time Series')
ax3.plot(O3_ebas_2013.index, O3_ebas_2013,
         label='EBAS Time Series')
ax3.set_ylabel('Mixing Ratio $O_{3}$ [ppbv]', fontsize=18)
ax3.set_xlabel('Date', fontsize=18)
ax3.set_title('Hourly Average of $O_{3}$ Mixing Ratio', fontsize=18)
ax3.legend()
fig2.show()

fig3 = plt.figure(3)
fig3.clf()
ax4 = fig3.add_subplot(111)
ax4.plot(O3_dmc_2013.index, O3_dmc_2013, label='DMC Time Series')
ax4.set_xlabel('Date', fontsize=18)
ax4.set_ylabel('Mixing Ratio $O_{3}$ [ppbv]', fontsize=18)
ax4.legend()
fig3.show()
O3_dmc_2013[O3_dmc_2013 < 5] = np.nan
O3_dmc_2013[O3_dmc_2013 > 65] = np.nan
fig4 = plt.figure(4)
fig4.clf()
ax5 = fig4.add_subplot(111)
ax5.plot(O3_dmc_2013.index, O3_dmc_2013, label='DMC Time Series')
ax5.set_xlabel('Date', fontsize=18)
ax5.set_ylabel('Mixing Ratio $O_{3}$ [ppbv]', fontsize=18)
ax5.legend(loc='upper right')
ax5.set_title('DMC Time Series After 5-65[ppbv] Filter', fontsize=18)
fig4.show()
fig5 = plt.figure(5)
fig5.clf()
ax6 = fig5.add_subplot(111)
ax6.plot(O3_ebas_2013.index, O3_ebas_2013, label='EBAS Time Series',
         color='orange')
ax6.set_xlabel('Date', fontsize=18)
ax6.set_ylabel('Mixing Ratio $O_{3}$ [ppbv]', fontsize=18)
ax6.legend(loc='upper right')
ax6.set_title('Hourly Average of $O_{3}$ Mixing Ratio', fontsize=18)
fig5.show()
