from numpy import genfromtxt
import plotly.express as px
import numpy as np
import plotly
import string

import plotly.graph_objects as go


my_data = genfromtxt('PowerPattern.csv', delimiter=',')


theta = np.arange(0, 361, 5)


fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=my_data[:,3],
    theta=theta,
    mode='lines',
    name='Measurement',
))
fig.update_layout(
    title='Radiation Pattern',
    showlegend=True,
    # width=650,
    # height=650,
)
fig.write_image("figtest.svg")


