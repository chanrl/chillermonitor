import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
from datetime import datetime

import pandas as pd

### REPLACE THIS WITH API CALL ###
df = pd.read_csv('SampleData.csv')
df = df[df['kW/Ton']>0.001].reset_index(drop=True)

def generate_sample():
    row_num = random.randint(0,len(df))
    lift = df.Lift[row_num]
    load = df['Load(%)'][row_num]
    kW = df['kW/Ton'][row_num]
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return lift, load, kW, time

lift, load, kW, time = generate_sample() 
### API CALL SHOULD RETURN VARS lift, load, kW as shown ###

X = deque([], maxlen=None) # to show only recent data points, set maxlen to # of recent data points displayed. animate would need to be toggled off as well
Y = deque([], maxlen=None)
Z = deque([], maxlen=None)
hovertextdisplay = deque([], maxlen=None)

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=5000,
            n_intervals = 0
        ),
    ]
)

@app.callback(Output('live-graph', 'figure'),
        [Input('graph-update', 'n_intervals')])


def update_graph_scatter(n):
    lift, load, kW, time = generate_sample()
    X.append(load)
    Y.append(lift)
    Z.append(kW)
    x_ann = X[-1]
    y_ann = Y[-1]
    z_ann = Z[-1]
    hovertextdisplay.append(f"{time} <br> % Load: {x_ann:.2f} <br> Lift (°F): {y_ann:.2f} <br> kW/ton: {z_ann:.2f}")

    data = go.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'markers',
            hovertext=list(hovertextdisplay),
            hoverinfo='text',
            marker=dict(color = list(Z), cmax=1, cmin=0.3, showscale=True, reversescale=True,
            colorscale='RdYlGn', size=8, colorbar=dict(title='kW/Ton', thickness=20) )
            )

    return {'data': [data], 'layout': go.Layout(title=dict(text='Chiller Status', x=.01, y=.98, xanchor='left'),
                                                xaxis=dict(title='% Load', range=[0,120]),
                                                yaxis=dict(title='Lift (°F)', range=[0,80], scaleratio=1),
                                                annotations=[dict(x=x_ann, y=y_ann, text=f'Latest {time}', showarrow=True, arrowhead=0, arrowcolor='white', ax=0, ay=40)],
                                                paper_bgcolor='black',
                                                plot_bgcolor='black',
                                                width=650,
                                                height=300,
                                                margin=dict(l=35,r=35,b=35,t=35),
                                                font=dict(color='white', size=12)
                                                )}





if __name__ == "__main__":
    app.run_server(debug=True)

