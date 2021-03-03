#!/usr/bin/env python
# coding: utf-8

# # Download data from ERDDAP and plot with Plotly

# In[8]:


import pandas as pd
import numpy as np
import os

# from _plotly_future_ import v4_subplots
import plotly
# import chart_studio.plotly as py
import plotly.graph_objs as go
from plotly import tools
import datetime

from erddapy import ERDDAP


# ### Step 1: access data on ERDDAP
# - from this URL: http://erddap.sccoos.org/erddap/tabledap/pH-AHL.csv
# - put into DataFrame

# In[12]:


e = ERDDAP(
  server="http://erddap.sccoos.org/erddap",
  protocol='tabledap',
)
e.response = 'csv'
e.dataset_id = "pH-AHL"

df_ahl_seaphox = e.to_pandas()

# Trim a bit for plotting speed
# df_ahl_seaphox = df_ahl_seaphox.iloc[::2, :]
df_ahl_seaphox.head()


# ### Make Plotly subplots; save HTML output

# In[15]:


# Create traces
trace1 = go.Scatter(
    x = df_ahl_seaphox['time (UTC)'], 
    y = df_ahl_seaphox['Temp_C'],
    mode = 'lines',
    name = 'Temperature'
)

trace2 = go.Scatter(
    x = df_ahl_seaphox['time (UTC)'], 
    y = df_ahl_seaphox['Pressure_dbar (dbar)'],
    mode = 'lines',
    name = 'Pressure'
)

trace3 = go.Scatter(
    x = df_ahl_seaphox['time (UTC)'], 
    y = df_ahl_seaphox['Sal_PSS'],
    mode = 'lines',
    name = 'Salinity'
)

trace4 = go.Scatter(
    x = df_ahl_seaphox['time (UTC)'], 
    y = df_ahl_seaphox['pH_total'],
    mode = 'lines',
    name = 'pH'
)

trace5 = go.Scatter(
    x = df_ahl_seaphox['time (UTC)'], 
    y = df_ahl_seaphox['O2_umol_per_kg'],
    mode = 'lines',
    name = 'O2'
)

trace6 = go.Scatter(
    x = df_ahl_seaphox['time (UTC)'], 
    y = df_ahl_seaphox['Omega_Ar'],
    mode = 'lines',
    name = 'Ω_Ar'
)

# data = [trace1, trace2]

fig = plotly.subplots.make_subplots(rows = 6, cols = 1, shared_xaxes=True)

fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 2, 1)
fig.append_trace(trace3, 3, 1)
fig.append_trace(trace4, 4, 1)
fig.append_trace(trace5, 5, 1)
fig.append_trace(trace6, 6, 1)

# Update yaxis properties
fig.update_yaxes(title_text="Temp (ºC)", row=1, col=1, range=[10, 27])
fig.update_yaxes(title_text="P (dbar)", row=2, col=1, range=[3.5, 6.5])
fig.update_yaxes(title_text="Sal (PSU)", row=3, col=1, range=[33.3, 34.5])
fig.update_yaxes(title_text="pH", row=4, col=1, range=[7.8, 8.1])
fig.update_yaxes(title_text="O2 (µmol/kg)", row=5, col=1, range=[175, 300])
fig.update_yaxes(title_text="Ω_ar", row=6, col=1, range=[1, 3.5])

fig.update_xaxes(title_text="Time (UTC)", row=6, col=1, range=[datetime.datetime(2019, 8, 22),
                                                       max(df_ahl_seaphox['time (UTC)'])])

# Plot and embed here
# py.iplot(fig, filename='ahl_subplots.html')
plotly.offline.plot(fig, filename='../ahl_subplots.html')


# In[ ]:





# In[ ]:




