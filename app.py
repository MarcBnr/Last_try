
# coding: utf-8

# In[6]:


#Final Project
#Create a Dashboard taking data from Eurostat, GDP and main components (output, expenditure and income).


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import base64


df = pd.read_csv('nama_10_gdp_1_Data.csv', na_values=':',usecols=["TIME","UNIT","GEO","NA_ITEM","Value"])
df['Value']=df['Value'].str.replace(',','').astype(float)
df=df.dropna()
df=df[~df.GEO.str.contains("Eur") ==True]
df=df[~df.UNIT.str.contains("Current prices, million euro")]
df=df[~df.UNIT.str.contains("Chain linked volumes, index 2010=100")]
df.rename(columns={'NA_ITEM':'Indicator','TIME':'Year','GEO':'Country','UNIT':'Value Type'},inplace=True)

available_indicators = df['Indicator'].unique()
available_countries = df['Country'].unique()


app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
    
app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Markdown('''Final assignment Cloud Computing 2018 - Marc Boner'''),
        ], 
                style={'marginLeft': 47, 'marginRight': 10, 'marginTop': 10, 'marginBottom': 10, 
                       'backgroundColor':'#F7FBFE', 'fontColor': 'blue','fontSize': 25,
                       'border': 'thin lightgrey dashed', 'padding': '6px 0px 0px 8px'},
                className="six columns"
        ),
        html.Div([
            html.Img(src='https://upload.wikimedia.org/wikipedia/commons/c/ce/ESADE_Logo.svg',height="53", width="200")
        ],
            style={'marginLeft': 10, 'marginRight': 10, 'marginTop': 30, 'marginBottom': 10,'textAlign': 'right'},
            className="row"
        ),
    ]),
        

#1. layout
    html.Div([
        html.Div([
        dcc.Markdown('''Relationship between key metrics for 38 countries'''),
    ], 
            style={'marginLeft': 10, 'marginRight': 10, 'marginTop': 10, 'marginBottom': 10,'fontSize': 20,'textAlign': 'center', 
                   'padding': '6px 0px 0px 8px'}),
    
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Exports of goods and services'
            ),
        ],
        style={'marginLeft': 48,'width': '47%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Exports of goods and services'
            )
        ],
        style={'width': '47%', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    html.Div([
        dcc.Slider(
            id='year--slider',
            min=df['Year'].min(),
            max=df['Year'].max(),
            value=df['Year'].max(),

            step=None,
            marks={str(year): str(year) for year in df['Year'].unique()}),
        
        html.Div(id='output-container-range-slider')
    ], style={'width':'92%', 'margin': 50, 'textAlign': 'center'}),
    
    html.Div([
        dcc.Markdown('''____________________________________________________________________________________________'''),
    ], 
            style={'marginLeft': 10, 'marginRight': 10, 'marginTop': 10, 'marginBottom': 10, 
                   'padding': '6px 0px 0px 8px'}),
    html.Div([
        dcc.Markdown('''Key metrics per country from 2008 to 2017'''),
    ], 
            style={'marginLeft': 10, 'marginRight': 10, 'marginTop': 10, 'marginBottom': 10,'fontSize': 20,'textAlign': 'center', 
                   'padding': '6px 0px 0px 8px'}),
    
    

#2 layout
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='Bulgaria'
            ),
        ],
        style={'marginLeft': 48,'width': '47%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Dropdown(
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Exports of goods and services'
            ),
        ],
        style={'width': '47%', 'display': 'inline-block'})
    ]),
    
    dcc.Graph(id='indicator-graphic2')

])

#1. update
@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,year_value):
    dff = df[df['Year'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[(dff['Indicator'] == xaxis_column_name)& (dff['Country']== i)]['Value'],
            y=dff[(dff['Indicator'] == yaxis_column_name)& (dff['Country']== i)]['Value'],
            text=dff[(dff['Indicator'] == yaxis_column_name)& (dff['Country']== i)]['Country'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            },
        name=i[:15]) 
                 for i in dff.Country.unique()
        ],         
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name+ '\n' + '[million euro]',
                'titlefont': dict(size=12),
            },
            yaxis={
                'title': yaxis_column_name+ '\n' + '[million euro]',
                'titlefont': dict(size=12),
            },
            margin={'l': 80, 'b': 40, 't': 30, 'r': 60},
            hovermode='closest'
        )
    }

#slider
@app.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('year--slider', 'value')])
                


#2. update
@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    [dash.dependencies.Input('xaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value')])

def update_graph(xaxis_column_name2, yaxis_column_name2):
    dff = df[(df['Country'] == xaxis_column_name2)]
    
    return {
        'data': [go.Scatter(
            x=dff[(dff['Indicator'] == yaxis_column_name2)& (dff['Country']== i)]['Year'],
            y=dff[(dff['Indicator'] == yaxis_column_name2)& (dff['Country']== i)]['Value'],
            text=dff[(dff['Indicator'] == xaxis_column_name2)& (dff['Country']== i)]['Value'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i[:15]) 
                 for i in df.Country.unique()
        ],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name2,
                'titlefont': dict(size=12),
            },
            yaxis={
                'title': yaxis_column_name2+ '\n' + '[million euro]',
                'titlefont': dict(size=12),
            },
            margin={'l': 80, 'b': 150, 't': 30, 'r': 60},
            hovermode='closest'
        )
    }



if __name__ == '__main__':
    app.run_server(debug=False)

