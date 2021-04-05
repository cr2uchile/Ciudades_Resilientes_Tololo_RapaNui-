#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 00:03:21 2021

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

def HistENG(DMC_data, EBAS_data, start_date, end_date):
    g =pd.concat([DMC_data,EBAS_data]).loc[start_date:end_date]
    fig = px.histogram(g, x=g.O3_ppbv, histnorm='probability density')
    ylabel = 'Probabity'
    fig.update_layout(
        title_font_family="Times New Roman",
#        title_font_color="red",        
        title_font_size=30,
        title_font_color = 'dimgray',
        plot_bgcolor='#f6f6f6',
        paper_bgcolor='#f6f6f6',
        titlefont=dict(size=14,color='black'),
        yaxis_title=ylabel,
        xaxis_title="O<sub>3</sub> [ppbv]") 
    return fig 

def HistESP(DMC_data, EBAS_data, start_date, end_date):
    g =pd.concat([DMC_data,EBAS_data]).loc[start_date:end_date]
    fig = px.histogram(g, x=g.O3_ppbv, histnorm='probability density')
    ylabel = 'Probabilidad'
    fig.update_layout(
        title_font_family="Times New Roman",
#        title_font_color="red",        
        title_font_size=30,
        title_font_color = 'dimgray',
        plot_bgcolor='#f6f6f6',
        paper_bgcolor='#f6f6f6',
        titlefont=dict(size=14,color='black'),
        yaxis_title=ylabel,
        xaxis_title="O<sub>3</sub> [ppbv]")
    return fig 