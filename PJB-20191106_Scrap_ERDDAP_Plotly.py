#!/usr/bin/env python
# coding: utf-8

# In[14]:


import pandas as pd
import numpy as np
import os

import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools

from erddapy import ERDDAP


# In[8]:


e = ERDDAP(
  server="http://erddap.sccoos.org/erddap",
  protocol='tabledap',
)
# http://erddap.sccoos.org/erddap/tabledap/pH-AHL.csv
e.response = 'csv'
e.dataset_id = "pH-AHL"

df_ahl_seaphox = e.to_pandas()
df_ahl_seaphox.head()


# In[20]:


# Create traces
trace1 = go.Scatter(
    x = df_ahl_seaphox['time (UTC)'], 
    y = df_ahl_seaphox['Temp_C'],
    mode = 'lines+markers',
    name = 'Temperature'
)

trace2 = go.Scatter(
    x = df_ahl_seaphox['time (UTC)'], 
    y = df_ahl_seaphox['Pressure_dbar (dbar)'],
    mode = 'lines+markers',
    name = 'Pressure'
)

trace3 = go.Scatter(
    x = df_ahl_seaphox['time (UTC)'], 
    y = df_ahl_seaphox['Sal_PSS'],
    mode = 'lines+markers',
    name = 'Salinity'
)

trace4 = go.Scatter(
    x = df_ahl_seaphox['time (UTC)'], 
    y = df_ahl_seaphox['pH_total'],
    mode = 'lines+markers',
    name = 'pH'
)

trace5 = go.Scatter(
    x = df_ahl_seaphox['time (UTC)'], 
    y = df_ahl_seaphox['O2_umol_per_kg'],
    mode = 'lines+markers',
    name = 'O2'
)

trace6 = go.Scatter(
    x = df_ahl_seaphox['time (UTC)'], 
    y = df_ahl_seaphox['Omega_Ar'],
    mode = 'lines+markers',
    name = 'Ω_Ar'
)

# data = [trace1, trace2]

fig = tools.make_subplots(rows = 6, cols = 1, shared_xaxes=True)

fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 2, 1)
fig.append_trace(trace3, 3, 1)
fig.append_trace(trace4, 4, 1)
fig.append_trace(trace5, 5, 1)
fig.append_trace(trace6, 6, 1)


# Plot and embed here
py.iplot(fig, filename='ahl_subplots.html')
plotly.offline.plot(fig, filename='../ahl_subplots.html')


# In[ ]:




