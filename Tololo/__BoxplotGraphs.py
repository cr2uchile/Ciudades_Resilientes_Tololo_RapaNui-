#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 23:50:05 2021

@author: Sebastián Villalón
"""
import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import geopandas as gpd
from dash.dependencies import Input, Output
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os as os
import numpy as np
import datetime
import base64
from datetime import date
from datetime import timedelta
from textwrap import dedent
from datetime import datetime as dt
from scipy.optimize import leastsq

def BoxENG(DMC_data, EBAS_data, start_date, end_date, radio_boxplot_eng):
    g =pd.concat([DMC_data,EBAS_data]).loc[start_date:end_date]
    if radio_boxplot_eng =='Hourly':           
        mat_h = g.set_index(g.index.hour, append=False).unstack()['O3_ppbv']    
        fig = px.box(mat_h,x=mat_h.index, y=mat_h.values,points=False)
        aux1 = [i for i in range(0,24)]
        aux2 = None       
        xlabel = 'Hour'    
    elif radio_boxplot_eng=='Monthly':
        mat_h = g.set_index(g.index.month, append=False).unstack()['O3_ppbv']
        fig = px.box(mat_h, x=mat_h.index, y=mat_h.values, points=False)
        aux1 = ["Jan", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dec"]
        xlabel = 'Mes' 
        aux2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 , 12]

    
    fig.update_layout(
    #    autosize=False,
    #    width=500,
    #    height=500,
        #title = zaxis6_name,
        title_font_family="Times New Roman",
#        title_font_color="red",        
        title_font_size=30,
        title_font_color = 'dimgray',
        plot_bgcolor='#f6f6f6',
        paper_bgcolor='#f6f6f6',
        width=540,
        height=400,
        margin=dict(t=50, b=10, l=10, r = 10),
        yaxis=dict(
            #title_text= '<b>' + yaxis6_name + '</b>', 
        titlefont=dict(size=14,color='black')),
        xaxis=dict(
            #title_text="<b>"+ radio2_name + "</b> ",
            ticktext=aux1,
            tickvals=aux2,
    #        tickmode="array",
        titlefont=dict(size=14,color='black'),
      ),xaxis_title=xlabel,
        yaxis_title="O<sub>3</sub> [ppbv]")
    fig.update_xaxes(
        tickangle = 90
        )
# # Update 3D scene options
#     fig.update_scenes(
#         aspectratio=dict(x=1, y=1, z=0.7),
#         aspectmode="manual"
#         )

# Add drowdowns
# button_layer_1_height = 1.08
    return fig

def BoxESP(DMC_data, EBAS_data, start_date, end_date, radio_boxplot_esp):
    g =pd.concat([DMC_data,EBAS_data]).loc[start_date:end_date]
    if radio_boxplot_esp =='Horario':           
        mat_h = g.set_index(g.index.hour, append=False).unstack()['O3_ppbv']    
        fig = px.box(mat_h,x=mat_h.index, y=mat_h.values,points=False)
        aux1 = [i for i in range(0,24)]
        aux2 = None       
        xlabel = 'Hora'    
    elif radio_boxplot_esp=='Mensual':
        mat_h = g.set_index(g.index.month, append=False).unstack()['O3_ppbv']
        fig = px.box(mat_h, x=mat_h.index, y=mat_h.values, points=False)
        aux1 = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        xlabel = 'Mes' 
        aux2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 , 12]

    
    fig.update_layout(
    #    autosize=False,
    #    width=500,
    #    height=500,
        #title = zaxis6_name,
        title_font_family="Times New Roman",
#        title_font_color="red",        
        title_font_size=30,
        title_font_color = 'dimgray',
        plot_bgcolor='#f6f6f6',
        paper_bgcolor='#f6f6f6',
        width=540,
        height=400,
        margin=dict(t=50, b=10, l=10, r = 10),
        yaxis=dict(
            #title_text= '<b>' + yaxis6_name + '</b>', 
        titlefont=dict(size=14,color='black')),
        xaxis=dict(
            #title_text="<b>"+ radio2_name + "</b> ",
            ticktext=aux1,
            tickvals=aux2,
    #        tickmode="array",
        titlefont=dict(size=14,color='black'),
      ),xaxis_title=xlabel,
        yaxis_title="O<sub>3</sub> [ppbv]")
    fig.update_xaxes(
        tickangle = 90
        )
# # Update 3D scene options
#     fig.update_scenes(
#         aspectratio=dict(x=1, y=1, z=0.7),
#         aspectmode="manual"
#         )

# Add drowdowns
# button_layer_1_height = 1.08
    return fig

