#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 16:40:36 2018

@author: pjb
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

plt.close('all')

# Filename for 60 second flushing (regardless of sample/standard "type")
filename_XSecsFlush = '../Notes -TW/SCS Tank Test/tank1031.txt'

# Import file, index by time
df_XSecsFlush = pd.read_csv(filename_XSecsFlush, header = 24, delimiter='\t', parse_dates=[1])
df_XSecsFlush.set_index('Sample Time', inplace=True)
df_XSecsFlush.head()

# Regroup by sample/standard type
sample_or_standard = df_XSecsFlush.groupby('Type')

# Plot by type
fig, ax = plt.subplots(figsize = (8, 6))

# put dotted line on first
ax.plot(df_XSecsFlush.index, df_XSecsFlush['Vext Ref'], 'k--', label = '') 

# lay points over top
for name, group in sample_or_standard:
    ax.plot(group.index, group['Vext Ref'], marker='o', linestyle='', ms=8, label=name)

ax.xaxis_date() # make sure it knows that x is a date/time
ax.legend()
ax.set_title(filename_XSecsFlush)
ax.set_ylabel('V_int (V)')
fig.autofmt_xdate()
plt.tight_layout()

# Create fig name from orignal filename and save
figname_XSecsFlush = filename_XSecsFlush[:-3]+'png'
plt.savefig(figname_XSecsFlush)