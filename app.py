
# coding: utf-8

# In[8]:


# Final Project
# Create a Dashboard taking data from [Eurostat, GDP and main components (output, expenditure and income)](http://ec.europa.eu/eurostat/web/products-datasets/-/nama_10_gdp). 
# The dashboard will have two graphs: 
# * The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data. 
# * The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' [(more here)](https://plot.ly/python/line-charts/) 

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
eurostat = pd.read_csv("nama_10_gdp_1_Data.csv")
available_indicators = eurostat['NA_ITEM'].unique()
available_countries = eurostat['GEO'].unique()
# Creating the Dashboard for Graph 1 & 2:
app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
# Creating the data frame for the units:
eurostat_1 = eurostat[eurostat['UNIT'] == 'Current prices, million euro']
app.layout = html.Div([
#Graph 1    
#I create the layout of the first dropdown and set the default value for my graph - Gross domestic product at market prices
# name of the x-axis is: xaxis-columns, and same for the yaxis = yaxiscolumns 
#first graph name = graph1
    
    html.Div([
        html.Div([
            dcc.Dropdown( 
                id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
        style={'width': '30%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown( 
                id='yaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Wages and salaries'
            )
        ],style={'width': '30%', 'float': 'right', 'display': 'inline-block'})
    ]),
    dcc.Graph(id='graph1'),
    html.Div(dcc.Slider( 
        id='year--slider',
        min=eurostat['TIME'].min(),
        max=eurostat['TIME'].max(),
        value=eurostat['TIME'].max(),
        step=None,
        marks={str(time): str(time) for time in eurostat['TIME'].unique()},
    ), style={'marginRight': 50, 'marginLeft': 110})])

