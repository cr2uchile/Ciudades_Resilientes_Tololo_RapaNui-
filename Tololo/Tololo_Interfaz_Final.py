#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 11:50:56 2021

@author: sebastian
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
from __TrendGraphs import *
from __MonthHourGraphs import *
from __BoxplotGraphs import *
from __HistGraphs import *


orig = os.getcwd()
fn_dmc = os.path.join(orig,'DATA','DMC-O3_RH_1H_dmc-1995-2013_clear.csv')
DMC_data = pd.read_csv(fn_dmc, index_col=0, parse_dates=True)
fn_ebas = os.path.join(orig,'DATA','EBAS-O3H-2013-2019.csv')
EBAS_data = pd.read_csv(fn_ebas, parse_dates=True, index_col=0)
EBAS_data.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)

image_filename_cr2 = 'logo_footer110.png'
encoded_image_cr2 = base64.b64encode(open(image_filename_cr2, 'rb').read()).decode('ascii')
image_filename_cr2_celeste = 'cr2_celeste.png'
encoded_image_cr2_celeste = base64.b64encode(open(image_filename_cr2_celeste, 'rb').read()).decode('ascii')
image_filename_DMC = 'logoDMC_140x154.png'
encoded_image_DMC = base64.b64encode(open(image_filename_DMC, 'rb').read()).decode('ascii')
image_filename_tololo = 'Tololo.png'
encoded_image_tololo = base64.b64encode(open(image_filename_tololo, 'rb').read()).decode('ascii')
image_filename_tololo_download = 'Tololo_Download.png'
encoded_image_tololo_download = base64.b64encode(open(image_filename_tololo_download, 'rb').read()).decode('ascii')
image_filename_GWA = 'gaw_logo.png'
encoded_image_GWA = base64.b64encode(open(image_filename_GWA, 'rb').read()).decode('ascii')
image_filename_lamsal = 'grafico_aero.png'
encoded_image_lamsal = base64.b64encode(open(image_filename_lamsal, 'rb').read()).decode('ascii')


##############cosas del mapa
fig = go.Figure(go.Scattergeo(lat=[-30.169], lon=[-70.804]))
fig.update_geos(projection_type="orthographic",
                projection_rotation=dict(lon=-70, lat=-30), bgcolor='#f6f6f6',
                lataxis_showgrid=True, lonaxis_showgrid=True
                
                  )
fig.update_layout(height=200, margin={"r":0,"t":0,"l":0,"b":0}, 
                  paper_bgcolor='#f6f6f6',
                  plot_bgcolor='#f6f6f6')


#######################
### -tabs prperties
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'color': '#0668a1',
}

tab_selected_style = {
    'borderTop': '#1766a0',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#1766a0',
    'color': 'white',
    'padding': '6px'
}
###
colors = {
    'background': 'white',
    'text': '#7FDBFF',
    'background_2': 'white',
    'background_3': 'cyan'

}
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
################################### Configuración Encabezado Página Web##############    
    html.Div([
        html.Div([html.H2("Tololo Ozone Measurements", style={'font-size':'18pt','color': 'white','font-family': 'Abel', 'font-weight': '200 !important', 'margin-top': '28px', 'margin-left':'10px'})], style={'position':'absolute','display': 'inline-block'}),
             html.A([       
             html.Img(src='data:image/png;base64,{}'.format(encoded_image_cr2), style={'height':'80px'})],href = 'http://www.cr2.cl/', style={'margin-left': '400px', 'position':'absolute'}),
             html.A([     
             html.Img(src='data:image/png;base64,{}'.format(encoded_image_DMC),style = {'height':'80px'})], href='http://www.meteochile.gob.cl/PortalDMC-web', style={'margin-left': '700px', 'position':'absolute'}),
             html.A([     
             html.Img(src='data:image/png;base64,{}'.format(encoded_image_GWA),style = {'height':'80px'})], href='https://www.wmo.int/gaw/', style={'margin-left': '900px', 'position':'absolute'}),
             html.Div([
                 html.H2("Language:" , style={'font-size':'15pt','color': 'white', 'margin-top': '30px'})], style={'margin-left': '1050px','display': 'inline-block', 'position':'absolute'}
                 ),
            html.Div([
                daq.ToggleSwitch(
                    id='Switch_Lang',
                    className='SwicthLang',
                    value=True,
                    )], style={'backgroundColor':'#1766a0','margin-top':'30px','margin-left': '1150px','display': 'inline-block', 'position':'absolute'}) 
    ],
    style={'backgroundColor':'#1766a0', 'height':'80px'}),
#####################################################################################    
    html.Div(id='tabs-content', style={'backgroundcolor':'#f6f6f6'})
])
########################################Contenido Página Web#########################
@app.callback(Output('tabs-content', 'children'),
              Input('Switch_Lang', 'value'))
def Web_Language(Switch_Lang):
#####################################Versión en Ingles###############################    
    if Switch_Lang==False:
        return [html.Div([
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-1',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Information',
                value='tab-1',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Graphs',
                value='tab-2',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Download Data',
                value='tab-3', className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Methods',
                value='tab-4',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
        ]),
    html.Div(id='tabs-content-classes', style={'backgroundColor':'#f6f6f6'})
])]
#######################################Version en Español ##########################      
    if Switch_Lang==True:
        return [html.Div([
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-1',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Presentación',
                value='tab-1',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Gráficos',
                value='tab-2',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Descargar Datos',
                value='tab-3', className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Métodos',
                value='tab-4',
                className='custom-tab',style=tab_style, selected_style=tab_selected_style,
                selected_className='custom-tab--selected'
            ),
        ]),
    html.Div(id='tabs-content-classes', style={'backgroundColor':'#f6f6f6'})
])]
    
@app.callback(Output('tabs-content-classes', 'children'),
              Input('tabs-with-classes', 'value'),
              Input('Switch_Lang', 'value'))
def render_content(tab, Switch_Lang):
################################################Tab 1###################################  
    if tab == 'tab-1':
        if Switch_Lang==False:
################################################ Informacion en Ingles##################            
            return [html.Div([html.Div([html.H1("Tololo (30.169 S, 70.804 W, 81m)", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'})
                ,dcc.Markdown(dedent(f'''
                As a part of the Global Atmospheric Watch (GAW) program, a monitoring station of radiation and surface ozone was installed by the World Meteorological Organization on the premises of the Cerro Tololo Inter-American Observatory, which is located near La Serena, Chile. Moreover, it is the objective of the “QHAWAYRA” (Quechua for “air survey”) program to make this site a fully equipped GAW station (Gallardo et al. 2000). The GAW measurements describe long-term changes in the atmospheric conditions. This goal requires measuring sites at which the anthropogenic impact of sources in the area is either avoided or is identified such that the data can be stratified accordingly. For this reason, the locations of these stations are sometimes chosen on summits of high mountains such as Cerro Tololo. Cerro Tololo (2200 m above mean sea level (MSL)) is situated about 50 km east of the Chilean coast at 30°S, where the cities of La Serena and Coquimbo are located. The topography of the area can be described as very complex. The valleys around these mountains are deep, down to 500 m MSL, and the Andes mountain range is only 30 km east of Cerro Tololo with heights of up to 6 km MSL.                     
                                     

                Principal Investigators: Laura Gallardo, Carmen Vega        
                Emails: [lgallard@u.uchile.cl](mailto:lgallard@u.uchile.cl), [carmen.vega@dgac.gob.cl](mailto:carmen.vega@dgac.gob.cl)
    
                
                Data Site Manager: Francisca Muñoz, CR2 – Center for Climate and Resilience Research.            
                Email: [fmunoz@dgf.uchile.cl](mailto:fmunoz@dgf.uchile.cl)
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Data scientist: Camilo Menares, CR2 - Center for Climate and Resilence Research.          
                Email: [cmenares@dgf.uchile.cl](mailto:cmenares@dgf.uchile.cl)
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Data scientist: Sebastian Villalón, CR2 - Center for Climate and Resilence Research.             
                Email: [sebastian.villalon@ug.uchile.cl](mailto:sebastian.villalon@ug.uchile.cl)
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Data Disclaimer: These data have been collected at Rapa Nui by the Chilean Weather Office (DMC) under the auspices of the Global Atmospheric Watch (GAW) Programme of the World Meteorological Organization (WMO).
    
                The data on this website are subject to revision and reprocessing. Check dates of creation to download the most current version.
    
                Contact the station principal investigator(s) for questions concerning data techniques and quality.
                
                
                
                '''), style={'margin-left':'60px'})] ,  
                style={'color': 'black', 'width':'50%',
                                                    'backgroundColor': '#f6f6f6', 'display': 'inline-block', 'margin-top':'50px', 'border-right': '2px solid #0668a1'}), 
                html.Div([
                                          html.Img(src='data:image/png;base64,{}'.format(encoded_image_tololo), 
                                   style={'height':'45%', 'width':'450px','margin-right':'75px' ,'margin-left':'75px', 'margin-top':'75px', 'border': '0px solid #0668a1', 'border-radius': '10px'}), dcc.Markdown('Credits: NOAO/NSF/AURA', style={'margin-left':'75px'}),
                                    html.H1("Map", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}), 
                                    dcc.Graph(figure=fig)
                                    ], 
                                    
                                     style={'display': 'inline-block', 'float':'right', 'width': '50%', 'backgroundColor': '#f6f6f6'})
                              ], style={'backgroundColor': '#f6f6f6', 'height':'780px'})
                              ]
#################################################Informacion en Español#####################################                              
        elif Switch_Lang==True:
            return[
                html.Div([
                html.Div([html.H1("Tololo (30.169 S, 70.804 W, 81m)", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                             dcc.Markdown(dedent(f'''
                As a part of the Global Atmospheric Watch (GAW) program, a monitoring station of radiation and surface ozone was installed by the World Meteorological Organization on the premises of the Cerro Tololo Inter-American Observatory, which is located near La Serena, Chile. Moreover, it is the objective of the “QHAWAYRA” (Quechua for “air survey”) program to make this site a fully equipped GAW station (Gallardo et al. 2000). The GAW measurements describe long-term changes in the atmospheric conditions. This goal requires measuring sites at which the anthropogenic impact of sources in the area is either avoided or is identified such that the data can be stratified accordingly. For this reason, the locations of these stations are sometimes chosen on summits of high mountains such as Cerro Tololo. Cerro Tololo (2200 m above mean sea level (MSL)) is situated about 50 km east of the Chilean coast at 30°S, where the cities of La Serena and Coquimbo are located. The topography of the area can be described as very complex. The valleys around these mountains are deep, down to 500 m MSL, and the Andes mountain range is only 30 km east of Cerro Tololo with heights of up to 6 km MSL.                                 
                                                 
                Investigadoras Principales: Laura Gallardo, Carmen Vega        
                Emails: [lgallard@u.uchile.cl](mailto:lgallard@u.uchile.cl), [carmen.vega@dgac.gob.cl](mailto:carmen.vega@dgac.gob.cl)
         
                
                Data Site Manager: Francisca Muñoz, CR2 – Center for Climate and Resilience Research.            
                Email: [fmunoz@dgf.uchile.cl](mailto:fmunoz@dgf.uchile.cl)
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Data scientist: Camilo Menares, CR2 - Center for Climate and Resilence Research.          
                Email: [cmenares@dgf.uchile.cl](mailto:cmenares@dgf.uchile.cl)
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Data scientist: Sebastian Villalón, CR2 - Center for Climate and Resilence Research.             
                Email: [sebastian.villalon@ug.uchile.cl](mailto:sebastian.villalon@ug.uchile.cl)
                Av. Blanco Encalada 2002, Santiago, Chile
                
                Data Disclaimer: These data have been collected at Rapa Nui by the Chilean Weather Office (DMC) under the auspices of the Global Atmospheric Watch (GAW) Programme of the World Meteorological Organization (WMO).

                The data on this website are subject to revision and reprocessing. Check dates of creation to download the most current version.
    
                Contact the station principal investigator(s) for questions concerning data techniques and quality.
                
                '''), style={'margin-left':'60px'})] ,  
                style={'color': 'black', 'width':'50%','backgroundColor': '#f6f6f6', 'display': 'inline-block', 'margin-top':'50px', 'border-right': '2px solid #0668a1'}), 
                html.Div([
                                          html.Img(src='data:image/png;base64,{}'.format(encoded_image_tololo), 
                                   style={'height':'45%', 'width':'450px','margin-right':'75px' ,'margin-left':'75px','margin-top':'75px', 'border': '0px solid #0668a1', 'border-radius': '10px'}), dcc.Markdown('Créditos: NOAO/NSF/AURA', style={'margin-left':'75px'}),
                                    html.H1("Mapa", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}), 
                                    dcc.Graph(figure=fig)], 
                                    
                                     style={'display': 'inline-block', 'float':'right', 'width': '50%', 'backgroundColor': '#f6f6f6'})
                ], style={'backgroundColor': '#f6f6f6', 'height':'780px'})
                                          ]
#####################################################################################
    elif tab == 'tab-2':
        if Switch_Lang==False:
                return [html.Div([
                    html.Div([
                    
                html.H1("Trends", style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}),
        html.Div([html.Label('Trends: ', style={'color':'#0668a1','display': 'inline-block'}),
                  html.Div([dbc.Container(
    [
        dbc.RadioItems(
            options=[
                {"label": "Lamsal", "value": "Lamsal"},
                {"label": "EMD", "value": "EMD"},
                {"label": "Linear", "value": "Linear"},
                {"label": "ThielSen", "value":"ThielSen"},
                {"label": "STL", "value":"STL"}
            ],
            id="radio_trends",
            labelClassName="date-group-labels",
            labelCheckedClassName="date-group-labels-checked",
            className="date-group-items",
            inline=True,
            value="Lamsal"
        ),
    ],
    className="p-3",
)
    ], style={'display':'inline-block'})
                 ,
                  
        html.Label('Period: ', style={'color':'#0668a1','display': 'inline-block'}),
                  html.Div([dbc.Container(
    [
        dbc.RadioItems(
            options=[
                {"label": "Daily", "value": "Daily"},
                {"label": "Monthly", "value": "Monthly"}
            ],
            id="radio_trends_period",
            labelClassName="date-group-labels",
            labelCheckedClassName="date-group-labels-checked",
            className="date-group-items",
            inline=True,
            value="Daily"
        ),
    ],
    className="p-3",
)
    ], style={'display':'inline-block'})
                 
                  ])
        ,
        dcc.Graph(id='Trend_graph', figure={"layout":{"height":400, "width":1080}})], style={'margin':'auto','width':'1080px', 'height':'500px'}),
        html.Div([
            html.Div([
    html.H1("Month-Hour Diagram", style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}),
    html.Div([ html.Label('Date Range:', style={'color':'#0668a1','font-size':'18px', 'backgroundColor':'#f6f6f6'}),
            dcc.DatePickerRange(
                id='calendar_1',
                start_date=date(1997, 5, 3),
                end_date=date(1998,5,3)
                )], style={'margin-left':'50px'}),
        dcc.Graph(id="MonthHourDiagram", style={'backgroundColor':'#f6f6f6'})], style={'margin-left':'100px','margin-top':'20px','width':'525px','height':'400px', 'display': 'inline-block'})
        ], style={'display':'inline-block'}),
        html.Div([
                daq.ToggleSwitch(
                    className='SwitchHBENG',
                    id='Switch_ENG',
                    value=False,
                    )   
                    , html.Div(id='switch-content')], style={'margin-left':'5px','margin-top':'20px','width':'525px','height':'400px', 'display': 'inline-block', 'backgroundColor':'#f6f6f6'})
        ,
        
    ], style={'backgroundColor': '#f6f6f6', 'height':'1100px'})
                    ]
        
        if Switch_Lang==True:
            return [
################################################GRafico Tendencia################
                html.Div([                
                html.Div([html.H1("Tendencia", style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}),
                              html.Div([
    html.Div([html.Label("Tendencia:", style={'font-size':'18px', 'color':'#0668a1'})],style={'display':'inline-block'}), html.Div([dbc.Container(
    [
        dbc.RadioItems(
            options=[
                {"label": "Lamsal", "value": "Lamsal"},
                {"label": "EMD", "value": "EMD"},
                {"label": "Linear", "value": "Linear"},
                {"label": "ThielSen", "value":"ThielSen"},
                {"label": "STL", "value":"STL"}
            ],
            id="radio_trends_esp",
            labelClassName="date-group-labels",
            labelCheckedClassName="date-group-labels-checked",
            className="date-group-items",
            inline=True,
            value="Lamsal"
        ),
    ],
    className="p-3",
)
    ], style={'display':'inline-block'}), 
    html.Label('Periodo: ', style={'color':'#0668a1','display': 'inline-block'}),
                  html.Div([dbc.Container(
    [
        dbc.RadioItems(
            options=[
                {"label": "Diario", "value": "Diario"},
                {"label": "Mensual", "value": "Mensual"}
            ],
            id="radio_trends_period_esp",
            labelClassName="date-group-labels",
            labelCheckedClassName="date-group-labels-checked",
            className="date-group-items",
            inline=True,
            value="Diario"
        ),
    ],
    className="p-3",
)
    ], style={'display':'inline-block'})
    
    
    ]),
            
            dcc.Graph(id='Tendencia_graf', figure={"layout":{"height":400, "width":1080}})], style={'margin':'auto','width':'1080px', 'height':'500px'}),
                
            html.Div([
                html.Div([
                html.H1("Diagrama Mes-Hora", style={'font-size':'24px','text-align': 'center', 'color': '#0668a1','backgroundColor':'#f6f6f6'}), 
                html.Div([ html.Label('Intervalo de Tiempo:', style={'color':'#0668a1','font-size':'18px', 'backgroundColor':'#f6f6f6'}),
            dcc.DatePickerRange(
                id='calendario_1',
                start_date=date(1997, 5, 3),
                end_date=date(1998,5,3)
                )], style={'margin-left':'50px'}),dcc.Graph(id="DiagramaMesHora", style={'backgroundColor':'#f6f6f6'})], style={'margin-left':'100px','margin-top':'20px','width':'525px','height':'400px', 'display': 'inline-block', 'backgroundColor':'#f6f6f6'}
                ),
                html.Div([
                daq.ToggleSwitch(
                    id='Switch',
                    className='SwitchHBESP',
                    value=False,
                    )   
                    , html.Div(id='switch-contenido')], style={'margin-left':'5px','margin-top':'20px','width':'525px','height':'400px', 'display': 'inline-block'})
                ])
        ], style={'backgroundColor': '#f6f6f6', 'height':'1100px'})    
        ]
    elif tab == 'tab-3':
        if Switch_Lang==False:
            return html.Div([
                html.Div([html.H1("Download", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),dcc.Markdown(dedent(f''' A continuación usted podrá descargar las mediciones realizadas en la estación Tololo.                                      
                                          En caso de necesitar un intervalo de tiempo específico, 
                                          debe seleccionar las fechas   
                                          en el calendario y a continuación presionar el botón de descargas:
                '''), style={'margin-left':'60px'}),dcc.DatePickerRange(
                id='calendario_descarga',
                start_date=min(DMC_data.index),
                end_date=max(EBAS_data.index)
                , style={'margin-left':'60px'}) ,dbc.Button("Descargar ", id="btn_descarga_2", n_clicks=0, style={'margin-left':'5px','display':'inline-block', 'backgroundColor':'#0668a1'}),Download(id="download_2")
                ,dcc.Markdown(dedent(f''' CITATION – If you use this dataset please acknowledge the Chilean Weather Office, and cite Anet, G. J., Steinbacher, M., Gallardo, L., Velásquez Álvarez, A. P., Emmenegger, L., and Buchmann, B. (2017). Surface ozone in the Southern Hemisphere: 20 years of data from a site with a unique setting in El Tololo, Chile. Atmos. Chem. Phys. 17, 6477–6492. doi:10.5194/acp-17-6477-2017.'''
                    ), style = {'margin-top':'50px', 'margin-left':'60px'}) 
                
                ],style={'color': 'black', 'width':'50%', 'margin-left':'0px'
                                                    ,'backgroundColor': '#f6f6f6', 'display': 'inline-block', 'margin-top':'50px', 'border-right': '2px solid #0668a1'}),
                html.Div([
                html.Img(src='data:image/png;base64,{}'.format(encoded_image_tololo_download), 
                                   style={'width':'350px' ,'margin-left':'70px','margin-top':'75px', 'border': '0px solid #0668a1', 'border-radius': '10px'})    
                    ], style={'display':'inline-block','float':'right' ,'width':'50%'})
                               
                               ], style={'backgroundColor': '#f6f6f6','height': '650px'})
                
            
        elif Switch_Lang==True:
            return html.Div([
        html.Div([html.H1("Descarga", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),dcc.Markdown(dedent(f''' A continuación usted podrá descargar las mediciones realizadas en la estación Tololo.                                      
                                          En caso de necesitar un intervalo de tiempo específico, 
                                          debe seleccionar las fechas   
                                          en el calendario y a continuación presionar el botón de descargas:
                '''), style={'margin-left':'60px'}),dcc.DatePickerRange(
                id='calendario_descarga',
                start_date=min(DMC_data.index),
                end_date=max(EBAS_data.index)
                , style={'margin-left':'60px'}) ,dbc.Button("Descargar ", id="btn_descarga_2", n_clicks=0, style={'margin-left':'5px','display':'inline-block', 'backgroundColor':'#0668a1'}),Download(id="download_2")
                ,dcc.Markdown(dedent(f''' CITATION – If you use this dataset please acknowledge the Chilean Weather Office, and cite Anet, G. J., Steinbacher, M., Gallardo, L., Velásquez Álvarez, A. P., Emmenegger, L., and Buchmann, B. (2017). Surface ozone in the Southern Hemisphere: 20 years of data from a site with a unique setting in El Tololo, Chile. Atmos. Chem. Phys. 17, 6477–6492. doi:10.5194/acp-17-6477-2017.'''
                    ), style = {'margin-top':'50px', 'margin-left':'60px'}) 
                
                ],style={'color': 'black', 'width':'50%', 'margin-left':'0px'
                                                    ,'backgroundColor': '#f6f6f6', 'display': 'inline-block', 'margin-top':'50px', 'border-right': '2px solid #0668a1'}),
                html.Div([
                html.Img(src='data:image/png;base64,{}'.format(encoded_image_tololo_download), 
                                   style={'width':'350px' ,'margin-left':'70px','margin-top':'75px', 'border': '0px solid #0668a1', 'border-radius': '10px'})    
                    ], style={'display':'inline-block','float':'right' ,'width':'50%'})
                               
                               ], style={'backgroundColor': '#f6f6f6','height': '650px'})
    elif tab == 'tab-4':
        if Switch_Lang==False:
            return [html.Div([html.H1("Lamsal", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                              
                dcc.Markdown(dedent(f'''
                Las tendencias lineales en estos compuestos se calcularon utilizando un modelo de regresión de Fourier según (Lamsal et al., 2015; Tiao et al., 1990) 
                para estimar las componentes estacionales y lineales en las observaciones de Ozono . 
                De acuerdo a (Lamsal et al., 2015), al suponer que la serie temporal de los valores medios mensuales en las observaciones de ozono en Tololo esta 
                compuesta por tres sub-componentes aditivos, podemos descomponer nuestra regresión como:
                    <p> &Omega; =  &alpha; (t) + bt + R(t)  </p>
                Donde (\u03A9) es la componente estacional dependiente del tiempo (t), (b) una componente de tendencia lineal y (R) un residuo o ruido. 
                Así se puede estimar la mayoría de las curvas para los contaminantes atmosféricos al definir \u03B1(t) como una serie de Fourier con 
                coeficientes n<sub>j<sub> y m<sub>j<sub> para una cantidad de datos j, como:  
                    
                Entonces dichas magnitudes representadas por la componente en la tendencia lineal (b) permitirán cuantificar la evolución en la concentraciones 
                de los contaminantes analizados. El error en la regresión es calculado según (Tiao et al., 1990), al cual es obtenido mediante una función 
                no lineal dependiente de la autocorrelación y el número total de datos.    
                
                '''), style={'margin-left':'60px'})
            ], style={'width':'50%', 'display':'inline-block', 'margin-top':'50px'}), 
                                    html.Div([
                html.H1("Artículos", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                dcc.Markdown(dedent(f'''
               Anet, G. J., Steinbacher, M., Gallardo, L., Velásquez Álvarez, A. P., Emmenegger, L., and Buchmann, B. (2017). Surface ozone in the Southern Hemisphere: 20 years of data from a site with a unique setting in El Tololo, Chile. Atmos. Chem. Phys. 17, 6477–6492. doi:10.5194/acp-17-6477-2017.
                '''), style={'margin-left':'60px'})
                ], style={'margin-top':'50px','display':'inline-block','float':'right' ,'width':'50%'})
                                    ]
        if Switch_Lang==True:        
            return [html.Div([
                html.H1("Lamsal", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                dcc.Markdown(dedent(f'''
                Las tendencias lineales en estos compuestos se calcularon utilizando un modelo de regresión de Fourier según (Lamsal et al., 2015; Tiao et al., 1990) 
                para estimar las componentes estacionales y lineales en las observaciones de Ozono . 
                De acuerdo a (Lamsal et al., 2015), al suponer que la serie temporal de los valores medios mensuales en las observaciones de ozono en Tololo esta 
                compuesta por tres sub-componentes aditivos, podemos descomponer nuestra regresión como:
                    <p> &Omega; =  &alpha; (t) + bt + R(t)  </p>
                Donde (\u03A9) es la componente estacional dependiente del tiempo (t), (b) una componente de tendencia lineal y (R) un residuo o ruido. 
                Así se puede estimar la mayoría de las curvas para los contaminantes atmosféricos al definir \u03B1(t) como una serie de Fourier con 
                coeficientes n<sub>j<sub> y m<sub>j<sub> para una cantidad de datos j, como:  
                    
                Entonces dichas magnitudes representadas por la componente en la tendencia lineal (b) permitirán cuantificar la evolución en la concentraciones 
                de los contaminantes analizados. El error en la regresión es calculado según (Tiao et al., 1990), al cual es obtenido mediante una función 
                no lineal dependiente de la autocorrelación y el número total de datos.    
                
                '''), style={'margin-left':'60px'})
            ], style={'width':'50%', 'display':'inline-block', 'margin-top':'50px'}), html.Div([
                html.H1("Artículos", style={'text-align': 'center','font-family': 'Abel','font-size': '28px','color': '#0668a1','backgroundColor': '#f6f6f6'}),
                dcc.Markdown(dedent(f'''
               Anet, G. J., Steinbacher, M., Gallardo, L., Velásquez Álvarez, A. P., Emmenegger, L., and Buchmann, B. (2017). Surface ozone in the Southern Hemisphere: 20 years of data from a site with a unique setting in El Tololo, Chile. Atmos. Chem. Phys. 17, 6477–6492. doi:10.5194/acp-17-6477-2017.
                '''), style={'margin-left':'60px'})
                ], style={'margin-top':'50px','display':'inline-block','float':'right' ,'width':'50%'})]                    
#################################### Trend Graph ###################    
@app.callback(Output('Trend_graph', 'figure'),
              Input('radio_trends', 'value'),
              Input('radio_trends_period', 'value')
              )
def update_graph(radio_trends,radio_trends_period):
    
    fig = trend(DMC_data, EBAS_data, radio_trends,radio_trends_period, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA)  

    return fig
########################################Grafico de Tendencia###################
@app.callback(Output('Tendencia_graf', 'figure'),
              Input('radio_trends_esp', 'value'),
              Input('radio_trends_period_esp', 'value')
              )
def update_graph(radio_trends_esp, radio_trends_period_esp):
    
    fig = tendencia(DMC_data, EBAS_data, radio_trends_esp,radio_trends_period_esp,encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA)

    return fig

#################################Slider- Español##############################
@app.callback(Output('switch-contenido', 'children'),
              Input('Switch', 'value'))
def render_content(Switch):
    if Switch == False:
        return [html.Div([
    html.H1("Histograma", style={'font-size':'24px','text-align': 'center','color': '#0668a1','backgroundColor':'#f6f6f6'}),
    html.Div([html.Label('Intervalo de tiempo:', style={'color':'#0668a1','font-size':'15px'}),
            dcc.DatePickerRange(
                id='calendario_3',
                start_date=date(1997, 5, 3),
                end_date=date(1998,5,3)
                )], style={'backgroundColor':'#f6f6f6'}),
    dcc.Graph(id="Histograma", style={'backgroundColor':'#f6f6f6'})], style={'width':'525px','height':'400px', 'display': 'inline-block', 'backgroundColor':'#f6f6f6'})]
    elif Switch == True:
        return [html.Div([    
        html.H1("Boxplot", style={'font-size':'24px','text-align': 'center','color': '#0668a1','backgroundColor':'#f6f6f6'}),   
    html.Div([
        html.Label('Fechas:', style={'color':'#0668a1','font-size':'15px'}),       
            dcc.DatePickerRange(
                id='calendario_2',
                start_date=date(1997, 5, 3),
                end_date=date(1998,5,3),
                )
     ], style={'display':'inline-block'})
        
    ,html.Div([html.Label("Promedio:", style={'color':'#0668a1','font-size':'18px'}), 
    html.Div([dbc.Container(
    [
        dbc.RadioItems(
            options=[
                {"label": "Horario", "value": "Horario"},
                {"label": "Mensual", "value": "Mensual"},
            ],
            id="radio_boxplot_esp",
            labelClassName="date-group-labels",
            labelCheckedClassName="date-group-labels-checked",
            className="date-group-items",
            inline=True,
            value="Horario"
        ),
    ],
    className="p-3",
    )
    ], style={'display':'inline-block'})
    ], style={'display':'inline-block'})
            ,
    dcc.Graph(id="Boxplot_esp", style={'backgroundColor':'#f6f6f6'})],style={'width':'525px','height':'400px'} )]
#################################Slider-English##############################
@app.callback(Output('switch-content', 'children'),
              Input('Switch_ENG', 'value'))
def render_content(Switch_ENG):
    if Switch_ENG == False:
        return [html.Div([
    html.H1("Histogram", style={'font-size':'24px','text-align': 'center','color': '#0668a1','backgroundColor':'#f6f6f6'}),
    html.Div([html.Label('Dates:', style={'color':'#0668a1','font-size':'15px'}),
            dcc.DatePickerRange(
                id='calendar_3',
                start_date=date(1997, 5, 3),
                end_date=date(1998,5,3)
                )], style={'backgroundColor':'#f6f6f6'}),
    dcc.Graph(id="Histogram", style={'backgroundColor':'#f6f6f6'})], style={'width':'525px','height':'400px', 'display': 'inline-block'})]
    elif Switch_ENG == True:
        return [html.Div([    
        html.H1("Boxplot", style={'font-size':'24px','text-align': 'center','color': '#0668a1','backgroundColor':'#f6f6f6'}),   
    html.Div([
        html.Label('Dates:', style={'color':'#0668a1','font-size':'15px'}),       
            dcc.DatePickerRange(
                id='calendar_2',
                start_date=date(1997, 5, 3),
                end_date=date(1998,5,3),
                )
     ], style={'display':'inline-block'})
        
    ,html.Div([html.Label("Mean:", style={'color':'#0668a1','font-size':'18px'}), 
    html.Div([dbc.Container(
    [
        dbc.RadioItems(
            options=[
                {"label": "Hourly", "value": "Hourly"},
                {"label": "Monthly", "value": "Monthly"},
            ],
            id="radio_boxplot_eng",
            labelClassName="date-group-labels",
            labelCheckedClassName="date-group-labels-checked",
            className="date-group-items",
            inline=True,
            value="Hourly"
        ),
    ],
    className="p-3",
    )
    ], style={'display':'inline-block'})
    ], style={'display':'inline-block'})
            ,
    dcc.Graph(id="Boxplot_Eng", style={'backgroundColor':'#f6f6f6'})],style={'width':'525px','height':'400px'} )]    
########################################## Month Hour Diagram#################
@app.callback(
    Output('MonthHourDiagram', 'figure'),
      [Input('calendar_1', 'start_date'),
      Input('calendar_1', 'end_date')])
def update_graph(start_date, end_date):
 
    fig = MonthHour(DMC_data, EBAS_data, start_date, end_date, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA)
    return fig
#######################################Diagrama Mes Hora###################### 
@app.callback(
    Output('DiagramaMesHora', 'figure'),
      [Input('calendario_1', 'start_date'),
      Input('calendario_1', 'end_date')])
def update_graph(start_date, end_date):
 
    fig = MesHora(DMC_data, EBAS_data, start_date, end_date, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA)
    return fig
#######################################Boxplot#################################
@app.callback(
    Output('Boxplot_Eng', 'figure'),
      [Input('calendar_2', 'start_date'),
      Input('calendar_2', 'end_date'), 
      Input('radio_boxplot_eng', 'value')])
def update_graph(start_date, end_date, radio_boxplot_eng):
    fig = BoxENG(DMC_data, EBAS_data, start_date, end_date, radio_boxplot_eng, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA)
    return fig  

###################################Diagrama cajas y bigotes ###################
@app.callback(
    Output('Boxplot_esp', 'figure'),
      [Input('calendario_2', 'start_date'),
      Input('calendario_2', 'end_date'), 
      Input('radio_boxplot_esp', 'value')])
def update_graph(start_date, end_date, radio_boxplot_esp):
    fig = BoxESP(DMC_data, EBAS_data, start_date, end_date, radio_boxplot_esp, encoded_image_cr2_celeste, encoded_image_DMC, encoded_image_GWA)
    return fig  
#####################################Histogram#################################
@app.callback(
    Output('Histogram', 'figure'),
      [Input('calendar_3', 'start_date'),
      Input('calendar_3', 'end_date')])
def update_graph(start_date, end_date):
    fig = HistENG(DMC_data, EBAS_data, start_date, end_date)    
    return fig  

#####################################Histograma###############################
@app.callback(
    Output('Histograma', 'figure'),
      [Input('calendario_3', 'start_date'),
      Input('calendario_3', 'end_date')])
def update_graph(start_date, end_date):
    fig = HistESP(DMC_data, EBAS_data, start_date, end_date)    
    return fig  
############### DEscarga de datos#############################################

@app.callback(Output("download_2", "data"), [Input("btn_descarga_2", "n_clicks"),Input('calendario_descarga', 'start_date'),
      Input('calendario_descarga', 'end_date')])
def generate_csv(n_clicks, start_date, end_date):
    if n_clicks==0:
        return None
    else:
        df_all = pd.concat([DMC_data,EBAS_data]).loc[start_date:end_date]
        return send_data_frame(df_all.to_csv, filename="Tololo_Time_Series_Dates_Selected.csv")    
if __name__ == '__main__':
    app.run_server(debug=True, port = 8050)


                                                              