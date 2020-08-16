import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd
import matplotlib as mpl
import numpy as np

from simulationapp.dataservice import DataServiceClient

COLOR = ['#ff0000', '#0000ff']

client = DataServiceClient()

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='temperature-slider',
        min=0,
        max=1,
        step=0.01,
        value=0.5
    ),
    html.Div(id='updatemode-output-container', style={'margin-top': 20})
])


def transform_value(value):
    max = 8000
    min = 4000
    temperature = int(value*(max-min) + min)
    return temperature


def color_fader(c1, c2, mix=0):
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)


@app.callback(Output('updatemode-output-container', 'children'),
              [Input('temperature-slider', 'value')])
def display_value(value):
    temperature = transform_value(value)
    return f"Temperature: {temperature} K"


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('temperature-slider', 'value')])
def update_figure(value):
    temperature = transform_value(value)
    data = client.get_data('BlackBodySpectrum', Temperature=temperature)
    color = color_fader(COLOR[0], COLOR[1], value)
    data['color'] = color

    fig = px.scatter(data, x="x", y="y", range_y=[0, 140], height=800)
    imax = data['y'].idxmax()
    fig.add_scatter(x=[data['x'].iloc[imax]], y=[data['y'].iloc[imax]], text=f"Max : {data['x'].iloc[imax]:.3f} um")

    fig.data[0].update(mode='lines', line_color=color, line_width=3)
    fig.data[1].update(mode='markers+text', line_color='black', marker_size=5, textposition="top center",textfont=dict(size=18,color=color))
    fig.update_layout(transition_duration=300,
                      plot_bgcolor='white',
                      title_text='Balck body radiation',
                      showlegend=False,
                      shapes=[
                          dict(
                              type="rect",
                              xref="x",
                              yref="y",
                              x0=0.380,
                              y0=0,
                              x1=0.740,
                              y1=140,
                              fillcolor="Black",
                              opacity=0.2,
                              layer="above",
                              line_width=0,
                          )]
                      )

    fig.update_xaxes(title='Wavelenght (um)')
    fig.update_yaxes(title='Intensity (kW sr-1 m-7)')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)