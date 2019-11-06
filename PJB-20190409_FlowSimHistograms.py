#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

### Read in flow simulation data for various endcaps and visualize to see variability in performance
cwd = os.getcwd()

## Printed part
### Read in data
filename = 'V3.2_Flow_Sim_printed.xlsx'
filepath = os.path.join(cwd, 'Data', filename)

df_3p2_3D = pd.read_excel(filepath)

### Format and clean data
df_3p2_3D.drop(index = 0, inplace = True) # bad row
df_3p2_3D.dropna(axis = 0, inplace = True)
df_3p2_3D['Residence time [s]'] = df_3p2_3D['Residence time [s]'].astype('float')

### Plot
fig, axs = plt.subplots()
axs.hist(df_3p2_3D['Residence time [s]'], bins = 100, label = filename)
axs.set_xlabel('Residence Time (s)')
axs.set_ylabel('Count')

## Printed part
### Read in data
filename = 'V3.2_Flow_Sim_printed.xlsx'
filepath = os.path.join(cwd, 'Data', filename)

df_3p2_3D = pd.read_excel(filepath)

### Format and clean data
df_3p2_3D.drop(index = 0, inplace = True) # bad row
df_3p2_3D.dropna(axis = 0, inplace = True)
df_3p2_3D['Residence time [s]'] = df_3p2_3D['Residence time [s]'].astype('float')

### Plot
fig, axs = plt.subplots()
axs.hist(df_3p2_3D['Residence time [s]'], bins = 100, label = filename)
axs.set_xlabel('Residence Time (s)')
axs.set_ylabel('Count')


## Machined part
### Read in data
filename = 'V3.2_Flow_Sim_machined.xlsx'
filepath = os.path.join(cwd, 'Data', filename)

df_3p2_CNC = pd.read_excel(filepath)

### Format and clean data
df_3p2_CNC.drop(index = 0, inplace = True) # bad row
df_3p2_CNC.dropna(axis = 0, inplace = True)
df_3p2_CNC['Residence time [s]'] = df_3p2_CNC['Residence time [s]'].astype('float')

### Plot
axs.hist(df_3p2_CNC['Residence time [s]'], bins = 100, label = filename)
axs.set_xlabel('Residence Time (s)')
axs.set_ylabel('Count')

plt.legend()