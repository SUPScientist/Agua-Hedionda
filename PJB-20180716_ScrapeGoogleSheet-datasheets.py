#%% # Google Sheets Scraper
# Goal: scrape the Google Sheet with autofilling data from the Particle Electron at Carlsbad Aquafarm
# [Google Sheet named "SeapHOx_OuterLagoon" is here](https://docs.google.com/spreadsheets/d/19jxQzqJa_B5zZJJmd6LmJDA0utKn0NTWoeNK_HkOse4/edit#gid=0)


import numpy as np
import pandas as pd
# import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datasheets
import os
import pytz

# ### Scrape Google Sheets
# Use datasheets library, following directions from https://datasheets.readthedocs.io/en/latest/index.html
# 


client = datasheets.Client()
workbook = client.fetch_workbook('SeapHOx_midLagoon')
tab = workbook.fetch_tab('Sheet1')
electron_array = tab.fetch_data()
electron_array.head()


# ### Get SeapHOx String, Parse, Remove Bad Transmissions
data_col = electron_array.iloc[:, 1]
data_array = pd.DataFrame(data_col.str.split(',', expand = True)) 

# Get rid of rows that don't start with "20" as in "2018"; this is foolproof until 2100 or 20 shows up elsewhere in a bad row, I guess
good_rows = (data_array.iloc[:, 0]).str.contains('20')
good_rows.fillna(False, inplace = True)
data_array = data_array[good_rows]


# ### Rename and Reindex
data_array.columns = ['Date', 'Time', 'V_batt', 'V_int', 'V_ext', 'P_dbar', 'pH_int', 'O2_uM', 'temp_SBE', 'sal_SBE', 'V_batt_elec', 'charge_status']
data_array.set_index(pd.to_datetime(data_array['Date'] + ' ' + data_array['Time']), inplace = True)
data_array.drop(['Date', 'Time'], axis = 1, inplace = True)
data_array.head()


# ### Filter
# - Filter based on date
# - Cast to type float (for some reason the str.split leaves it as arbitrary object)
# - This was necessary in early notebook as the input data wasn't filtered at all but the Google Sheet should be cleaner to begin with (*i.e.*, no land data)
# - Filtration may come in handy later so keep this here for now

date_filt = data_array.index > '2018-09-06 18:30:00'
data_filt = data_array[date_filt]


pacific = pytz.timezone('US/Pacific')
data_filt.index = data_filt.index.tz_localize(pytz.utc).tz_convert(pacific)

data_filt = data_filt.astype('float')

data_filt.tail()
# data_filt.V_press


#%% Time-Series Plots
fig, axs = plt.subplots(6, 1, figsize = (10, 10), sharex = True)
axs[0].plot(data_filt.index, data_filt.V_batt, 'k')
axs[0].set_ylabel('V_batt')
ax2 = axs[0].twinx()
ax2.plot(data_filt.index, data_filt.V_batt_elec, 'r')
ax2.set_ylabel('V_batt_elec', color='r')
ax2.tick_params('y', colors='r')

axs[1].plot(data_filt.index, data_filt.P_dbar, 'k')
axs[1].set_ylabel('P (dbar)')

axs[2].plot(data_filt.index, data_filt.sal_SBE, 'k')
axs[2].set_ylabel('Salinity')

axs[3].plot(data_filt.index, data_filt.temp_SBE, 'k')
axs[3].set_ylabel('Temp (C)')

axs[4].plot(data_filt.index, data_filt.V_int, 'k')
axs[4].set_ylabel('V_int')
ax2 = axs[4].twinx()
ax2.plot(data_filt.index, data_filt.V_ext, 'r')
ax2.set_ylabel('V_ext', color='r')
ax2.tick_params('y', colors='r')

axs[5].plot(data_filt.index, data_filt.pH_int, 'k')
axs[5].set_ylabel('pH')
ax2 = axs[5].twinx()
ax2.plot(data_filt.index, data_filt.O2_uM, 'r')
ax2.set_ylabel('O2 (uM)', color='r')
ax2.tick_params('y', colors='r')

axs[0].xaxis_date() # make sure it knows that x is a date/time

for axi in axs.flat:
#     axi.xaxis.set_major_locator(plt.MaxNLocator(3))
#     print(axi)
    axi.yaxis.set_major_locator(plt.MaxNLocator(3))
#     axi.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.02f"))

fig.autofmt_xdate() # makes the date labels easier to read.
plt.tight_layout()
plt.savefig('test_dep_01.png')

#%% Property-Property Plot
fig, axs = plt.subplots(1, 1, figsize = (10, 10), sharex = True)
pHOx = axs.scatter(x = data_filt.pH_int, 
                   y = data_filt.O2_uM, 
                   c = data_filt.P_dbar, 
                   s = 100)
axs.set_xlabel('pH (int)')
axs.set_ylabel('O2 (uM)')
plt.colorbar(pHOx, label = 'P (dbar)');

#%% Correlation Plot
cmap = plt.get_cmap('coolwarm')
corr = data_filt.corr()
corr.style.background_gradient(cmap, axis=1)    .set_properties(**{'max-width': '80px', 'font-size': '10pt'})    .set_caption("SeapHOx Correlations")    .set_precision(2)


# In[39]:




