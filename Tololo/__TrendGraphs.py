#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 23:26:57 2021

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
from __toolsTrend import *

def tendencia(DMC_data, EBAS_data, radio_trends, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA):
    df_d =  pd.concat([DMC_data,EBAS_data]).loc['1997':'2020']
    
    #aux_a , aux_b = info_data('2015-01-01 01','2020-08-09 23',df,'D')

    df_m = df_d.resample('M').mean().loc['1997':'2020']
    df_m.O3_ppbv[df_m.O3_ppbv<20] = np.nan
    df_m = df_m.fillna(df_m.mean()) 
    s    = df_m.O3_ppbv.values 
    s_df = df_m.O3_ppbv
    ###################

    if radio_trends == 'Lamsal':        
        model_trend =  lamsal_trend(s)
    elif radio_trends == 'Linear':
        model_trend = linear_trend(s)
    elif radio_trends == 'EMD':
        model_trend = emd_trend(s)    
    elif radio_trends == 'STL':
        model_trend = stl_trend(s_df)    
    elif radio_trends == 'ThielSen':
        model_trend = TheillSen_trend(s) 
        



    fig = go.Figure()       
    fig.add_trace(go.Scatter(
            x=df_m.index,
            y=df_m["O3_ppbv"],
            mode='markers',
            #text = aux_a    ,  
            marker={
                'size': 6,
                #'color': aux_b,
                'opacity': 0.5,
                'line': {'width': 0.9, 'color': 'black'}
            }
        ))
    fig.add_trace(go.Scatter( 
                x=df_m.index, 
                y=model_trend[0],
                mode='markers', 
                marker=dict(size= 6, color='black')
                ))

    fig.add_trace(go.Scatter( 
                    x=df_m.index[0:1], 
                    y= [57 , 57] , #df_m[0:1]*2.0
                    mode='text', 
                    marker=dict(size= 6, color='black'),
                    text=["Tendencia Decadal= " + str(round(model_trend[1]*10*12,1)) + ' +/- ' + str(round(tiao(model_trend[0], s)*10,2)) +'[ppbv]  <br>Promedio= '+ str(round(df_m["O3_ppbv"].mean(),1)) + " [ppbv]"],
                    textposition="top right",
                    textfont=dict(
                    family="Times New Roman",
                    size=14,
                    color="black")  #
                    ))
    fig.update_layout(
            showlegend = True,
            title_font_family="Times New Roman",
    #        title_font_color="red",        
            title_font_size=30,
            yaxis=dict(
                range=[0, 65]),
            margin=dict(t=50, b=10, l=10, r = 10),
            title_font_color = 'dimgray',
            plot_bgcolor='#f6f6f6',
            paper_bgcolor='#f6f6f6',
            titlefont=dict(size=14,color='black'),
            xaxis_title='Fecha',
            yaxis_title="O<sub>3</sub> [ppbv]") 
    fig.update_layout(
images= [       dict(
                    source='data:image/png;base64,{}'.format(encoded_image_cr2_celeste),
                    xref="paper", yref="paper",
                    x=0.6, y=1,
                    sizex=0.2, sizey=0.2,
                    xanchor="right",
                    yanchor="top",
                    #sizing="stretch",
                    layer="above")    ,dict(
                    source='data:image/png;base64,{}'.format(encoded_image_DMC),
                    xref="paper", yref="paper",
                    x=0.7, y=1,
                    sizex=0.15, sizey=0.15,
                    xanchor="right",
                    yanchor="top",
                    #sizing="stretch",
                    layer="above"), dict(
                    source='data:image/png;base64,{}'.format(encoded_image_GWA),
                    xref="paper", yref="paper",
                    x=0.8, y=1,
                    sizex=0.15, sizey=0.15,
                    xanchor="right",
                    yanchor="top",
                    #sizing="stretch",
                    layer="above")])
    return fig

def trend(DMC_data, EBAS_data, radio_trends, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA):
    df_d =  pd.concat([DMC_data,EBAS_data]).loc['2012':'2020']
    
    #aux_a , aux_b = info_data('2015-01-01 01','2020-08-09 23',df,'D')

    df_m = df_d.resample('M').mean().loc['2012':'2020']
    df_m.O3_ppbv[df_m.O3_ppbv<20] = np.nan
    df_m = df_m.fillna(df_m.mean()) 
    s    = df_m.O3_ppbv.values 
    s_df = df_m.O3_ppbv
    ###################

    if radio_trends == 'Lamsal':        
        model_trend =  lamsal_trend(s)
    elif radio_trends == 'Linear':
        model_trend = linear_trend(s)
    elif radio_trends == 'EMD':
        model_trend = emd_trend(s)    
    elif radio_trends == 'STL':
        model_trend = stl_trend(s_df)    
    elif radio_trends == 'ThielSen':
        model_trend = TheillSen_trend(s) 

    fig = go.Figure()       
    fig.add_trace(go.Scatter(
            x=df_m.index,
            y=df_m["O3_ppbv"],
            name='medicion',
            mode='markers',
            #text = aux_a    ,  
            marker={
                'size': 6,
                #'color': aux_b,
                'opacity': 0.5,
                'line': {'width': 0.9, 'color': 'black'}
            }
        ))
    fig.add_trace(go.Scatter( 
                x=df_m.index, 
                y=model_trend[0],
                name='tendencia',
                mode='markers', 
                marker=dict(size= 6, color='black')
                ))

    fig.add_trace(go.Scatter( 
                    x=df_m.index[0:1], 
                    y= [57 , 57],
                    mode='text', 
                    marker=dict(size= 6, color='black'),
                    text=["Decadal Trend = " + str(round(model_trend[1]*10*12,1)) + ' +/- xx [ppbv]  <br>Mean= '+ str(round(df_m["O3_ppbv"].mean(),1)) + " [ppbv]"],
                    textposition="top right",
                    textfont=dict(
                    family="Times New Roman",
                    size=14,
                    color="black")  #
                    ))
    fig.update_layout(
            showlegend = False,
            title_font_family="Times New Roman",
    #        title_font_color="red",        
            title_font_size=30,
            yaxis=dict(
                range=[0, 65]),
            margin=dict(t=0, b=0, l=0, r = 0),
            title_font_color = 'dimgray',
            plot_bgcolor='#f6f6f6',
            paper_bgcolor='#f6f6f6',
            titlefont=dict(size=14,color='black'),
            xaxis_title='Fecha',
            yaxis_title="O<sub>3</sub> [ppbv]")
    fig.update_layout(
    images= [       dict(
                        source='data:image/png;base64,{}'.format(encoded_image_cr2_celeste),
                        xref="paper", yref="paper",
                        x=0.6, y=1,
                        sizex=0.2, sizey=0.2,
                        xanchor="right",
                        yanchor="top",
                        #sizing="stretch",
                        layer="above")    ,dict(
                        source='data:image/png;base64,{}'.format(encoded_image_DMC),
                        xref="paper", yref="paper",
                        x=0.7, y=1,
                        sizex=0.15, sizey=0.15,
                        xanchor="right",
                        yanchor="top",
                        #sizing="stretch",
                        layer="above"), dict(
                        source='data:image/png;base64,{}'.format(encoded_image_GWA),
                        xref="paper", yref="paper",
                        x=0.8, y=1,
                        sizex=0.15, sizey=0.15,
                        xanchor="right",
                        yanchor="top",
                        #sizing="stretch",
                        layer="above")])
    return fig                             