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


# In[16]:


# Create traces
trace1 = go.Scatter(
    x = df_ahl_seaphox['time (UTC)'], 
    y = df_ahl_seaphox['pH_total'],
    mode = 'lines+markers',
    name = 'pH'
)

trace2 = go.Scatter(
    x = df_ahl_seaphox['time (UTC)'], 
    y = df_ahl_seaphox['O2_umol_per_kg'],
    mode = 'lines+markers',
    name = 'O2'
)

# trace3 = go.Scatter(
#     x = df_ahl_seaphox['time (UTC)'], 
#     y = az_m_s2,
#     mode = 'lines+markers',
#     name = 'Az (m/s2)'
# )

# trace4 = go.Scatter(
#     x = df_ahl_seaphox['time (UTC)'], 
#     y = df_ahl_seaphox['vel (m/s)'],
#     mode = 'lines+markers', 
#     name = 'Vel (m/s)'
# )

# trace5 = go.Scatter(
#     x = df_ahl_seaphox['time (UTC)'], 
#     y = df_ahl_seaphox['displacement (m)'],
#     mode = 'lines+markers',
#     name = 'Disp (m)'
# )

# trace6 = go.Scatter(
#     x = df_ahl_seaphox['time (UTC)'], 
#     y = df_ahl_seaphox['temp'],
#     mode = 'lines+markers',
#     name = 'Temp (oC)'
# )

# data = [trace1, trace2]

fig = tools.make_subplots(rows = 4, cols = 1, shared_xaxes=True)

fig.append_trace(trace1, 1, 1)
fig.append_trace(trace2, 2, 1)
# fig.append_trace(trace3, 1, 1)
# fig.append_trace(trace4, 2, 1)
# fig.append_trace(trace5, 3, 1)
# fig.append_trace(trace6, 4, 1)


# Plot and embed here
py.iplot(fig, filename='ahl_subplots.html')
plotly.offline.plot(fig, filename='ahl_subplots.html')


# In[ ]:




