#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 23:43:40 2021

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


def MesHora(DMC_data, EBAS_data, start_date, end_date, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA):
    g =pd.concat([DMC_data,EBAS_data]).loc[start_date:end_date]
    a = g.groupby([g.index.month, g.index.hour]).mean()
    O3_mesh = [a.O3_ppbv.values[24*i:24*(i+1)] for i in range (0,13)]

    Months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    xlabel = 'Hora'
    ylabel = 'Mes'

    fig = go.Figure(data=(go.Contour(z=O3_mesh,
                                  #x = [i for i in range(24)],
                                  #y = [i for i in range(1,13)])])
                                  x =["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11" , "12", "13", "14", "15", "16", "17", "18", "19", "20", "21","22","23"],
                                  y = Months, colorscale= 'viridis',
                                  
                                  colorbar=dict(
            title='O<sub>3</sub> [ppbv]', # title here
            titleside='right',
            titlefont=dict(
                size=14,
                family='Arial, sans-serif')), contours=dict(
            coloring ='heatmap',
            showlabels = True, # show labels on contours
            labelfont = dict( # label font properties
                size = 13,
                color = 'black')
            ))))

    fig.update_layout(
        width=540,
        height=540,
        autosize=False,
        margin=dict(t=50, b=10, l=10, r = 10),
        title_font_family="Times New Roman",
#        title_font_color="red",        
        title_font_size=30,
        title_font_color = 'dimgray',
        plot_bgcolor='#f6f6f6',
        paper_bgcolor='#f6f6f6',
        titlefont=dict(size=14,color='black'),
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        )
    # # Update 3D scene options
#     fig.update_scenes(
#         aspectratio=dict(x=1, y=1, z=0.7),
#         aspectmode="manual"
#         )

# Add drowdowns
# button_layer_1_height = 1.08
    fig.update_layout(
            images= [       dict(
                    source='data:image/png;base64,{}'.format(encoded_image_cr2_celeste),
                    xref="paper", yref="paper",
                    x=0.25, y=1.0,
                    sizex=0.2, sizey=0.2,
                    xanchor="right",
                    yanchor="bottom",
                    #sizing="stretch",
                    layer="above")    ,dict(
                    source='data:image/png;base64,{}'.format(encoded_image_DMC),
                    xref="paper", yref="paper",
                    x=0.58, y=1.05,
                    sizex=0.15, sizey=0.15,
                    xanchor="right",
                    yanchor="bottom",
                    #sizing="stretch",
                    layer="above"), dict(
                    source='data:image/png;base64,{}'.format(encoded_image_GWA),
                    xref="paper", yref="paper",
                    x=0.95, y=1.05,
                    sizex=0.17, sizey=0.17,
                    xanchor="right",
                    yanchor="bottom",
                    #sizing="stretch",
                    layer="above")])
    
    # update layout properties
    fig.update_layout(
        autosize=False,
        height=480,
        width=540,
        bargap=0.15,
        bargroupgap=0.1,
        barmode="stack",
        hovermode="x",
        margin=dict(t=100, b=10, l=10, r = 10),
    )


    return fig

def MonthHour(DMC_data, EBAS_data, start_date, end_date, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA):
    
    g =pd.concat([DMC_data,EBAS_data]).loc[start_date:end_date]
    a = g.groupby([g.index.month, g.index.hour]).mean()
    O3_mesh = [a.O3_ppbv.values[24*i:24*(i+1)] for i in range (0,13)]

    Months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    xlabel = 'Hour'
    ylabel = 'Month'

    fig = go.Figure(data=(go.Contour(z=O3_mesh,
                                  #x = [i for i in range(24)],
                                  #y = [i for i in range(1,13)])])
                                  x =["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11" , "12", "13", "14", "15", "16", "17", "18", "19", "20", "21","22","23"],
                                  y = Months, colorscale= 'viridis',
                                  
                                  colorbar=dict(
            title='O<sub>3</sub> [ppbv]', # title here
            titleside='right',
            titlefont=dict(
                size=14,
                family='Arial, sans-serif')), contours=dict(
            coloring ='heatmap',
            showlabels = True, # show labels on contours
            labelfont = dict( # label font properties
                size = 13,
                color = 'black')
            ))))

    fig.update_layout(
        width=540,
        height=400,
        autosize=False,
        margin=dict(t=50, b=10, l=10, r = 10),
        title_font_family="Times New Roman",
#        title_font_color="red",        
        title_font_size=30,
        title_font_color = 'dimgray',
        plot_bgcolor='#f6f6f6',
        paper_bgcolor='#f6f6f6',
        titlefont=dict(size=14,color='black'),
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        )
    fig.update_layout(
            images= [       dict(
                    source='data:image/png;base64,{}'.format(encoded_image_cr2_celeste),
                    xref="paper", yref="paper",
                    x=0.25, y=1.0,
                    sizex=0.2, sizey=0.2,
                    xanchor="right",
                    yanchor="bottom",
                    #sizing="stretch",
                    layer="above")    ,dict(
                    source='data:image/png;base64,{}'.format(encoded_image_DMC),
                    xref="paper", yref="paper",
                    x=0.58, y=1.05,
                    sizex=0.15, sizey=0.15,
                    xanchor="right",
                    yanchor="bottom",
                    #sizing="stretch",
                    layer="above"), dict(
                    source='data:image/png;base64,{}'.format(encoded_image_GWA),
                    xref="paper", yref="paper",
                    x=0.95, y=1.05,
                    sizex=0.17, sizey=0.17,
                    xanchor="right",
                    yanchor="bottom",
                    #sizing="stretch",
                    layer="above")])
    
    # update layout properties
    fig.update_layout(
        autosize=False,
        height=480,
        width=540,
        bargap=0.15,
        bargroupgap=0.1,
        barmode="stack",
        hovermode="x",
        margin=dict(t=100, b=10, l=10, r = 10),
    )

# # Update 3D scene options
#     fig.update_scenes(
#         aspectratio=dict(x=1, y=1, z=0.7),
#         aspectmode="manual"
#         )

# Add drowdowns
# button_layer_1_height = 1.08
    return fig