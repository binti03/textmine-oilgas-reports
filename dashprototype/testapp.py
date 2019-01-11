import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd 
import re
import plotly.graph_objs as go

raw_data = pd.read_csv('raw_data.csv',sep = ',', header=0, parse_dates = ['Event_Date'])
def add_datepart(df, fldname):
    fld = df[fldname]
    targ_pre = re.sub('[Dd]ate$','',fldname)
    for n in ('Year','Month','Week','Day','Dayofweek','Is_month_end','Is_month_start','Is_quarter_end','Is_quarter_start','Is_year_end','Is_year_start'):
        df[targ_pre+n] = getattr(fld.dt, n.lower())
        df[targ_pre+'Elapsed'] = (fld - fld.min()).dt.days
        
add_datepart(raw_data, 'Event_Date')

dydg_df = pd.DataFrame(raw_data.Event_Date.dt.day_name())
dydg_df['Degree'] = raw_data.Degree
dydg_df = pd.DataFrame(dydg_df.groupby(['Event_Date','Degree']).size().reset_index(name='count'))
dydg_df = dydg_df.pivot(index='Event_Date', columns='Degree', values='count')
dydg_df.reset_index(inplace=True)
cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
from pandas.api.types import CategoricalDtype
cat_type = CategoricalDtype(categories=cats, ordered=True)
dydg_df.Event_Date = dydg_df.Event_Date.astype(cat_type)
dydg_df.sort_values('Event_Date', inplace=True)

mdg = pd.DataFrame(raw_data.Event_Date.dt.month_name())
mdg['Degree'] = raw_data.Degree
mdg = pd.DataFrame(mdg.groupby(['Event_Date','Degree']).size().reset_index(name='count'))
mdg = mdg.pivot(index='Event_Date', columns='Degree', values='count')
mdg.reset_index(inplace=True)
cats = ['January', 'February', 'March', 'April','May','June', 'July', 'August','September', 'October', 'November', 'December']
from pandas.api.types import CategoricalDtype
cat_type = CategoricalDtype(categories=cats, ordered=True)
mdg.Event_Date = mdg.Event_Date.astype(cat_type)
mdg.sort_values('Event_Date', inplace=True)

hdg = pd.DataFrame({'Time':raw_data.Time, 'Degree':raw_data.Degree})
hdg = pd.DataFrame(hdg.groupby(['Time','Degree']).size().reset_index(name='count'))
hdg = hdg.pivot(index='Time', columns='Degree', values='count')
hdg.reset_index(inplace=True)



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1('Oil and Gas Industry Accident Analysis', 
           style={
            'textAlign': 'center'
        }),


    html.Div([
        html.H4('NAICS 213111, 213112, 237120  |  Fatality and Catastrophe Investigation Summaries  |  Timeline 2001-2017',
            style={
            'textAlign': 'center',
            'color': '#A9A9A9'
        })
    ]),

    html.Div([
        dcc.Textarea(id='input-box', 
            placeholder='Please enter your summary report text here..', 
            style={'width':'50%'}),
        ], style={'align-items':'center'}),

    html.Div([html.Button('Submit', id='button')],style={'align-items': 'center','justify-content': 'center'}),
        html.Div(id='output-container-button',
             children='Enter a value and press submit'),

    html.Div(
        className='row1',
        children=[
            html.Div([
                    dcc.Graph(
                        id='timeline-graph',
                        figure={
                            'data': [dict(
                                          x = raw_data['Event_Date'],
                                          autobinx = False,
                                          autobiny = True,
                                          #marker = dict(color = 'rgb(68, 68, 68)'),
                                          name = 'date',
                                          type = 'histogram',
                                          xbins = dict(
                                            end = '2017-12-31',
                                            size = 'M1',
                                            start = '2001-01-01'
                                          )
                                        )],
                            'layout': dict(
                                          # paper_bgcolor = 'rgb(240, 240, 240)',
                                          # plot_bgcolor = 'rgb(240, 240, 240)',
                                          title = '<b>Oil & Gas Industry Accidents</b>',
                                          xaxis = dict(
                                            title = 'Years',
                                            tickangle=-90,
                                            type = 'date',
                                            nticks = 25
                                          ),
                                          yaxis = dict(
                                            title = 'Accident Count',
                                            type = 'linear'
                                          ),
                                          updatemenus = [dict(
                                                x = 0.1,
                                                y = 1.15,
                                                xref = 'paper',
                                                yref = 'paper',
                                                yanchor = 'top',
                                                active = 1,
                                                showactive = True,
                                                buttons = [
                                                dict(
                                                    args = ['xbins.size', 'D1'],
                                                    label = 'Day',
                                                    method = 'restyle',
                                                ), dict(
                                                    args = ['xbins.size', 'M1'],
                                                    label = 'Month',
                                                    method = 'restyle',
                                                ), dict(
                                                    args = ['xbins.size', 'M3'],
                                                    label = 'Quater',
                                                    method = 'restyle',
                                                ), dict(
                                                    args = ['xbins.size', 'M6'],
                                                    label = 'Half Year',
                                                    method = 'restyle',
                                                ), dict(
                                                    args = ['xbins.size', 'M12'],
                                                    label = 'Year',
                                                    method = 'restyle',
                                                )]
                                          )]
                                        )
                        }
                    )
                ], 
                style={
                "height" : "25%", 
                "width" : "55%", 
                'border-width': '1px', 
                'border-color':'#ababab', 
                'display': 'inline-block', 
                'border-style': 'solid'
                }),


                html.Div([
                    dcc.Graph(
                        id = 'dayofweek',
                        
                        figure={
                                'data' : [
                                    go.Bar(
                                    x=dydg_df.Event_Date,
                                    y=dydg_df.Fatality,
                                    name='Fatality'
                                    ),
                                    go.Bar(
                                    x=dydg_df.Event_Date,
                                    y=dydg_df['Hospitalized injury'],
                                    name='Hospitalized Injury'
                                    ),
                                    go.Bar(
                                    x=dydg_df.Event_Date,
                                    y=dydg_df['Non Hospitalized injury'],
                                    name='Non Hospitalized Injury'
                                    ),
                                ],
                                'layout' : go.Layout(
                                    # paper_bgcolor = 'rgb(240, 240, 240)',
                                    # plot_bgcolor = 'rgb(240, 240, 240)',
                                    barmode='group',
                                    title = '<b>Day of Week vs Degree</b>',
                                    yaxis = dict(
                                    title = 'Accident Count (2013-2017)',
                                    type = 'linear'
                                    ),
                                    xaxis = dict(
                                    title = 'Days of Week'), 
                                    legend=dict(x=0, y=1.1, orientation='h')
                                )
                        }
                    )

                ], 
                style={
                "height" : "25%", 
                "width" : "40%", 
                'border-width': '1px', 
                'border-color':'#ababab', 
                'display': 'inline-block', 
                'border-style': 'solid'
                })
        ]),

    
    html.Div(
        className='row2',
        children=[

            html.Div([
                dcc.Graph(
                    id='month-degree',
                    figure={
                        'data' : [
                            go.Bar(
                            x=mdg.Event_Date,
                            y=mdg.Fatality,
                            name='Fatality'
                            ),
                            go.Bar(
                            x=mdg.Event_Date,
                            y=mdg['Hospitalized injury'],
                            name='Hospitalized Injury'
                            ),
                            go.Bar(
                            x=mdg.Event_Date,
                            y=mdg['Non Hospitalized injury'],
                            name='Non Hospitalized Injury'
                            )],
                        'layout' : go.Layout(
                                    barmode='group',
                                    title = '<b>Month vs Degree</b>',
                                    xaxis=dict(
                                    tickangle=-45,
                                    title = 'Months'),
                                    yaxis = dict(
                                    title = 'Accident Count (2013-2017)',
                                    type = 'linear'
                                    ),
                                    legend=dict(x=0, y=1.1, orientation='h')
                                )
                    }
                )
            ], 
            style={
            "height" : "25%", 
            "width" : "45%", 
            'border-width': '1px', 
            'border-color':'#ababab', 
            'display': 'inline-block', 
            'border-style': 'solid'
            }),

            html.Div([
                dcc.Graph(
                    id='hour-degree',
                    figure={
                        'data' : [
                            go.Bar(
                            x=hdg.Time,
                            y=hdg.Fatality,
                            name='Fatality'
                            ),
                            go.Bar(
                            x=hdg.Time,
                            y=hdg['Hospitalized injury'],
                            name='Hospitalized Injury'
                            ),
                            go.Bar(
                            x=hdg.Time,
                            y=hdg['Non Hospitalized injury'],
                            name='Non Hospitalized Injury'
                            )
                        ],
                        'layout' : go.Layout(
                                    barmode='group',
                                    title = '<b>Hour of Day vs Degree</b>',
                                    xaxis = dict(
                                    title = 'Hours of Day (24 hour format)',
                                    nticks = 24
                                    ),
                                    yaxis = dict(
                                    title = 'Accident Count',
                                    type = 'linear'
                                    ),
                                    legend=dict(x=0, y=1.1, orientation='h')
                                )
                    }
                )
            ], 
            style={
            "height" : "25%", 
            "width" : "50%", 
            'border-width': '1px', 
            'border-color':'#ababab', 
            'display': 'inline-block', 
            'border-style': 'solid'
            })
    ])
    

])

@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, value):
    return 'The input value was "{}" '.format(
        value
    )

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)