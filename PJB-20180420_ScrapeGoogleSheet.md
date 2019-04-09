
# Google Sheets Scraper
Goal: scrape the Google Sheet with autofilling data from the Particle Electron at Carlsbad Aquafarm
[Google Sheet named "SeapHOx_OuterLagoon" is here](https://docs.google.com/spreadsheets/d/19jxQzqJa_B5zZJJmd6LmJDA0utKn0NTWoeNK_HkOse4/edit#gid=0)


```python
import numpy as np
import pandas as pd
# import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

# %matplotlib inline
```

### Scrape Google Sheets
Run python script from https://developers.google.com/sheets/api/quickstart/python which needs to run separately as it interacts with the web browser (in other words, don't copy and paste script into here.


```python
%run ./quickstart.py
type(values)
print(values[-5:])
```

    [['4/25/2018', '2018/04/25,18:33:37,17.900,0.08970,-0.82115,4.61300,8.21260,324.13400,17.61180,33.61750,3.92,68.17'], ['4/25/2018', '2018/04/25,19:30:25,17.900,0.08984,-0.82095,4.39200,8.21485,325.94699,17.53390,33.63030,3.92,67.88'], ['4/25/2018', '2018/04/25,20:00:25,17.900,0.09020,-0.82050,4.31700,8.21950,328.78201,17.82600,33.61960,3.92,67.88'], ['4/25/2018', '2018/04/25,20:30:25,17.900,0.08992,-0.82070,4.22800,8.21406,328.10199,17.77370,33.57290,3.92,67.88'], ['4/25/2018', '2018/04/25,21:30:25,17.900,0.08955,-0.82108,4.24400,8.20803,321.25500,17.72110,33.61730,3.92,67.88']]


### Grab Useful Data from Sheet


```python
electron_array = pd.DataFrame(values) # includes timestamp
data_col = electron_array.iloc[:, 1]
data_array = pd.DataFrame(data_col.str.split(',', expand = True)) 
data_array.columns = ['Date', 'Time', 'V_batt', 'V_int', 'V_ext', 'P_dbar', 'pH_int', 'O2_umolkg', 'temp_SBE', 'sal_SBE', 'V_batt_elec', 'charge_status']
data_array.set_index(pd.to_datetime(data_array['Date'] + ' ' + data_array['Time']), inplace = True)
data_array.drop(['Date', 'Time'], axis = 1, inplace = True)
data_array.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>V_batt</th>
      <th>V_int</th>
      <th>V_ext</th>
      <th>P_dbar</th>
      <th>pH_int</th>
      <th>O2_umolkg</th>
      <th>temp_SBE</th>
      <th>sal_SBE</th>
      <th>V_batt_elec</th>
      <th>charge_status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2018-04-17 18:30:25</th>
      <td>18.860</td>
      <td>0.07985</td>
      <td>-0.83308</td>
      <td>5.33600</td>
      <td>8.05349</td>
      <td>328.51599</td>
      <td>13.43740</td>
      <td>33.55860</td>
      <td>4.05</td>
      <td>84.77</td>
    </tr>
    <tr>
      <th>2018-04-17 19:00:25</th>
      <td>18.870</td>
      <td>0.08055</td>
      <td>-0.83331</td>
      <td>5.41600</td>
      <td>8.08004</td>
      <td>328.32300</td>
      <td>13.48790</td>
      <td>33.56140</td>
      <td>4.05</td>
      <td>84.62</td>
    </tr>
    <tr>
      <th>2018-04-17 19:30:25</th>
      <td>18.860</td>
      <td>0.08002</td>
      <td>-0.83326</td>
      <td>5.38800</td>
      <td>8.07537</td>
      <td>325.82300</td>
      <td>13.53800</td>
      <td>33.55890</td>
      <td>4.05</td>
      <td>84.62</td>
    </tr>
    <tr>
      <th>2018-04-17 20:02:20</th>
      <td>18.860</td>
      <td>0.07946</td>
      <td>-0.83334</td>
      <td>5.35400</td>
      <td>8.06744</td>
      <td>324.28900</td>
      <td>13.54920</td>
      <td>33.56210</td>
      <td>4.05</td>
      <td>84.48</td>
    </tr>
    <tr>
      <th>2018-04-17 20:32:51</th>
      <td>18.850</td>
      <td>0.07959</td>
      <td>-0.83293</td>
      <td>5.21900</td>
      <td>8.06995</td>
      <td>326.27499</td>
      <td>13.65300</td>
      <td>33.56350</td>
      <td>4.05</td>
      <td>84.48</td>
    </tr>
  </tbody>
</table>
</div>



### Filter
- Filter based on date
- Cast to type float (for some reason the str.split leaves it as arbitrary object)
- This was necessary in early notebook as the input data wasn't filtered at all but the Google Sheet should be cleaner to begin with (*i.e.*, no land data)
- Filtration may come in handy later so keep this here for now


```python
date_filt = data_array.index > '2018-04-17 18:30:00'
data_filt = data_array[date_filt]

import pytz
pacific = pytz.timezone('US/Pacific')
data_filt.index = data_filt.index.tz_localize(pytz.utc).tz_convert(pacific)

data_filt = data_filt.astype('float')

data_filt.tail()
# data_filt.V_press
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>V_batt</th>
      <th>V_int</th>
      <th>V_ext</th>
      <th>P_dbar</th>
      <th>pH_int</th>
      <th>O2_umolkg</th>
      <th>temp_SBE</th>
      <th>sal_SBE</th>
      <th>V_batt_elec</th>
      <th>charge_status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2018-04-25 11:33:37-07:00</th>
      <td>17.9</td>
      <td>0.08970</td>
      <td>-0.82115</td>
      <td>4.613</td>
      <td>8.21260</td>
      <td>324.13400</td>
      <td>17.6118</td>
      <td>33.6175</td>
      <td>3.92</td>
      <td>68.17</td>
    </tr>
    <tr>
      <th>2018-04-25 12:30:25-07:00</th>
      <td>17.9</td>
      <td>0.08984</td>
      <td>-0.82095</td>
      <td>4.392</td>
      <td>8.21485</td>
      <td>325.94699</td>
      <td>17.5339</td>
      <td>33.6303</td>
      <td>3.92</td>
      <td>67.88</td>
    </tr>
    <tr>
      <th>2018-04-25 13:00:25-07:00</th>
      <td>17.9</td>
      <td>0.09020</td>
      <td>-0.82050</td>
      <td>4.317</td>
      <td>8.21950</td>
      <td>328.78201</td>
      <td>17.8260</td>
      <td>33.6196</td>
      <td>3.92</td>
      <td>67.88</td>
    </tr>
    <tr>
      <th>2018-04-25 13:30:25-07:00</th>
      <td>17.9</td>
      <td>0.08992</td>
      <td>-0.82070</td>
      <td>4.228</td>
      <td>8.21406</td>
      <td>328.10199</td>
      <td>17.7737</td>
      <td>33.5729</td>
      <td>3.92</td>
      <td>67.88</td>
    </tr>
    <tr>
      <th>2018-04-25 14:30:25-07:00</th>
      <td>17.9</td>
      <td>0.08955</td>
      <td>-0.82108</td>
      <td>4.244</td>
      <td>8.20803</td>
      <td>321.25500</td>
      <td>17.7211</td>
      <td>33.6173</td>
      <td>3.92</td>
      <td>67.88</td>
    </tr>
  </tbody>
</table>
</div>



### Plot


```python
fig, axs = plt.subplots(6, 1, figsize = (10, 10), sharex = True)
axs[0].plot(data_filt.index, data_filt.V_batt)
axs[0].set_ylabel('V_batt')
ax2 = axs[0].twinx()
ax2.plot(data_filt.index, data_filt.V_batt_elec, 'r')
ax2.set_ylabel('V_batt_elec', color='r')
ax2.tick_params('y', colors='r')

axs[1].plot(data_filt.index, data_filt.P_dbar)
axs[1].set_ylabel('P_dbar')

axs[2].plot(data_filt.index, data_filt.sal_SBE)
axs[2].set_ylabel('sal_SBE')

axs[3].plot(data_filt.index, data_filt.temp_SBE)
axs[3].set_ylabel('Temp')

axs[4].plot(data_filt.index, data_filt.V_int)
axs[4].set_ylabel('V_int')
ax2 = axs[4].twinx()
ax2.plot(data_filt.index, data_filt.V_ext, 'r')
ax2.set_ylabel('V_ext', color='r')
ax2.tick_params('y', colors='r')

axs[5].plot(data_filt.index, data_filt.pH_int)
axs[5].set_ylabel('pH')
ax2 = axs[5].twinx()
ax2.plot(data_filt.index, data_filt.O2_umolkg, 'r')
ax2.set_ylabel('O2', color='r')
ax2.tick_params('y', colors='r')

axs[0].xaxis_date() # make sure it knows that x is a date/time

for axi in axs.flat:
#     axi.xaxis.set_major_locator(plt.MaxNLocator(3))
#     print(axi)
    axi.yaxis.set_major_locator(plt.MaxNLocator(3))
#     axi.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.02f"))

fig.autofmt_xdate() # makes the date labels easier to read.
```


```python
fig, axs = plt.subplots(1, 1, figsize = (10, 10), sharex = True)
pHOx = axs.scatter(x = data_filt.pH_int, 
                   y = data_filt.O2_umolkg, 
                   c = data_filt.P_dbar, 
                   s = 100)
axs.set_xlabel('pH (int)')
axs.set_ylabel('O2 (umol per something)')
plt.colorbar(pHOx, label = 'P (dbar)');
```


```python
cmap = plt.get_cmap('coolwarm')
corr = data_filt.corr()
corr.style.background_gradient(cmap, axis=1)\
    .set_properties(**{'max-width': '80px', 'font-size': '10pt'})\
    .set_caption("SeapHOx Correlations")\
    .set_precision(2)
```





        <style  type="text/css" >
        
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row0_col0 {
            
                background-color:  #b40426;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row0_col1 {
            
                background-color:  #3b4cc0;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row0_col2 {
            
                background-color:  #3b4cc0;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row0_col3 {
            
                background-color:  #e9d5cb;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row0_col4 {
            
                background-color:  #3d50c3;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row0_col5 {
            
                background-color:  #9ebeff;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row0_col6 {
            
                background-color:  #4358cb;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row0_col7 {
            
                background-color:  #b7cff9;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row0_col8 {
            
                background-color:  #d55042;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row0_col9 {
            
                background-color:  #d24b40;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row1_col0 {
            
                background-color:  #3b4cc0;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row1_col1 {
            
                background-color:  #b40426;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row1_col2 {
            
                background-color:  #b40426;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row1_col3 {
            
                background-color:  #cad8ef;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row1_col4 {
            
                background-color:  #b40426;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row1_col5 {
            
                background-color:  #ec7f63;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row1_col6 {
            
                background-color:  #d24b40;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row1_col7 {
            
                background-color:  #edd1c2;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row1_col8 {
            
                background-color:  #6282ea;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row1_col9 {
            
                background-color:  #5e7de7;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row2_col0 {
            
                background-color:  #3b4cc0;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row2_col1 {
            
                background-color:  #b40426;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row2_col2 {
            
                background-color:  #b40426;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row2_col3 {
            
                background-color:  #c1d4f4;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row2_col4 {
            
                background-color:  #b50927;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row2_col5 {
            
                background-color:  #ed8366;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row2_col6 {
            
                background-color:  #cd423b;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row2_col7 {
            
                background-color:  #ebd3c6;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row2_col8 {
            
                background-color:  #6282ea;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row2_col9 {
            
                background-color:  #5e7de7;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row3_col0 {
            
                background-color:  #b7cff9;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row3_col1 {
            
                background-color:  #7ea1fa;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row3_col2 {
            
                background-color:  #7093f3;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row3_col3 {
            
                background-color:  #b40426;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row3_col4 {
            
                background-color:  #89acfd;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row3_col5 {
            
                background-color:  #bad0f8;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row3_col6 {
            
                background-color:  #3b4cc0;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row3_col7 {
            
                background-color:  #ccd9ed;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row3_col8 {
            
                background-color:  #b1cbfc;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row3_col9 {
            
                background-color:  #b1cbfc;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row4_col0 {
            
                background-color:  #3b4cc0;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row4_col1 {
            
                background-color:  #b40426;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row4_col2 {
            
                background-color:  #b50927;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row4_col3 {
            
                background-color:  #cfdaea;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row4_col4 {
            
                background-color:  #b40426;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row4_col5 {
            
                background-color:  #e9785d;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row4_col6 {
            
                background-color:  #da5a49;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row4_col7 {
            
                background-color:  #edd1c2;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row4_col8 {
            
                background-color:  #6788ee;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row4_col9 {
            
                background-color:  #6282ea;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row5_col0 {
            
                background-color:  #3b4cc0;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row5_col1 {
            
                background-color:  #f6a283;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row5_col2 {
            
                background-color:  #f7a688;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row5_col3 {
            
                background-color:  #b5cdfa;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row5_col4 {
            
                background-color:  #f39778;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row5_col5 {
            
                background-color:  #b40426;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row5_col6 {
            
                background-color:  #d3dbe7;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row5_col7 {
            
                background-color:  #86a9fc;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row5_col8 {
            
                background-color:  #6f92f3;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row5_col9 {
            
                background-color:  #6a8bef;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row6_col0 {
            
                background-color:  #3b4cc0;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row6_col1 {
            
                background-color:  #d44e41;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row6_col2 {
            
                background-color:  #cf453c;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row6_col3 {
            
                background-color:  #90b2fe;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row6_col4 {
            
                background-color:  #da5a49;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row6_col5 {
            
                background-color:  #f3c8b2;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row6_col6 {
            
                background-color:  #b40426;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row6_col7 {
            
                background-color:  #e0dbd8;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row6_col8 {
            
                background-color:  #4055c8;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row6_col9 {
            
                background-color:  #3f53c6;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row7_col0 {
            
                background-color:  #5f7fe8;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row7_col1 {
            
                background-color:  #c0d4f5;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row7_col2 {
            
                background-color:  #bad0f8;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row7_col3 {
            
                background-color:  #cbd8ee;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row7_col4 {
            
                background-color:  #c0d4f5;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row7_col5 {
            
                background-color:  #8badfd;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row7_col6 {
            
                background-color:  #abc8fd;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row7_col7 {
            
                background-color:  #b40426;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row7_col8 {
            
                background-color:  #3b4cc0;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row7_col9 {
            
                background-color:  #3b4cc0;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row8_col0 {
            
                background-color:  #d75445;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row8_col1 {
            
                background-color:  #516ddb;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row8_col2 {
            
                background-color:  #536edd;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row8_col3 {
            
                background-color:  #dfdbd9;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row8_col4 {
            
                background-color:  #5a78e4;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row8_col5 {
            
                background-color:  #bbd1f8;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row8_col6 {
            
                background-color:  #3b4cc0;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row8_col7 {
            
                background-color:  #8caffe;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row8_col8 {
            
                background-color:  #b40426;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row8_col9 {
            
                background-color:  #b50927;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row9_col0 {
            
                background-color:  #d44e41;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row9_col1 {
            
                background-color:  #506bda;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row9_col2 {
            
                background-color:  #506bda;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row9_col3 {
            
                background-color:  #e0dbd8;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row9_col4 {
            
                background-color:  #5875e1;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row9_col5 {
            
                background-color:  #b7cff9;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row9_col6 {
            
                background-color:  #3b4cc0;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row9_col7 {
            
                background-color:  #8fb1fe;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row9_col8 {
            
                background-color:  #b50927;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
            #T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row9_col9 {
            
                background-color:  #b40426;
            
                max-width:  80px;
            
                font-size:  10pt;
            
            }
        
        </style>

        <table id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530" None>
        
            <caption>SeapHOx Correlations</caption>
        

        <thead>
            
            <tr>
                
                
                <th class="blank level0" >
                  
                
                
                
                <th class="col_heading level0 col0" colspan=1>
                  V_batt
                
                
                
                <th class="col_heading level0 col1" colspan=1>
                  V_int
                
                
                
                <th class="col_heading level0 col2" colspan=1>
                  V_ext
                
                
                
                <th class="col_heading level0 col3" colspan=1>
                  P_dbar
                
                
                
                <th class="col_heading level0 col4" colspan=1>
                  pH_int
                
                
                
                <th class="col_heading level0 col5" colspan=1>
                  O2_umolkg
                
                
                
                <th class="col_heading level0 col6" colspan=1>
                  temp_SBE
                
                
                
                <th class="col_heading level0 col7" colspan=1>
                  sal_SBE
                
                
                
                <th class="col_heading level0 col8" colspan=1>
                  V_batt_elec
                
                
                
                <th class="col_heading level0 col9" colspan=1>
                  charge_status
                
                
            </tr>
            
        </thead>
        <tbody>
            
            <tr>
                
                
                <th id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530"
                 class="row_heading level0 row0" rowspan=1>
                    V_batt
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row0_col0"
                 class="data row0 col0" >
                    1
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row0_col1"
                 class="data row0 col1" >
                    -0.92
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row0_col2"
                 class="data row0 col2" >
                    -0.92
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row0_col3"
                 class="data row0 col3" >
                    0.13
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row0_col4"
                 class="data row0 col4" >
                    -0.9
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row0_col5"
                 class="data row0 col5" >
                    -0.35
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row0_col6"
                 class="data row0 col6" >
                    -0.86
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row0_col7"
                 class="data row0 col7" >
                    -0.2
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row0_col8"
                 class="data row0 col8" >
                    0.81
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row0_col9"
                 class="data row0 col9" >
                    0.83
                
                
            </tr>
            
            <tr>
                
                
                <th id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530"
                 class="row_heading level0 row1" rowspan=1>
                    V_int
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row1_col0"
                 class="data row1 col0" >
                    -0.92
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row1_col1"
                 class="data row1 col1" >
                    1
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row1_col2"
                 class="data row1 col2" >
                    1
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row1_col3"
                 class="data row1 col3" >
                    -0.091
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row1_col4"
                 class="data row1 col4" >
                    1
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row1_col5"
                 class="data row1 col5" >
                    0.64
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row1_col6"
                 class="data row1 col6" >
                    0.83
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row1_col7"
                 class="data row1 col7" >
                    0.18
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row1_col8"
                 class="data row1 col8" >
                    -0.68
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row1_col9"
                 class="data row1 col9" >
                    -0.7
                
                
            </tr>
            
            <tr>
                
                
                <th id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530"
                 class="row_heading level0 row2" rowspan=1>
                    V_ext
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row2_col0"
                 class="data row2 col0" >
                    -0.92
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row2_col1"
                 class="data row2 col1" >
                    1
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row2_col2"
                 class="data row2 col2" >
                    1
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row2_col3"
                 class="data row2 col3" >
                    -0.14
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row2_col4"
                 class="data row2 col4" >
                    0.99
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row2_col5"
                 class="data row2 col5" >
                    0.62
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row2_col6"
                 class="data row2 col6" >
                    0.86
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row2_col7"
                 class="data row2 col7" >
                    0.15
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row2_col8"
                 class="data row2 col8" >
                    -0.68
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row2_col9"
                 class="data row2 col9" >
                    -0.7
                
                
            </tr>
            
            <tr>
                
                
                <th id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530"
                 class="row_heading level0 row3" rowspan=1>
                    P_dbar
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row3_col0"
                 class="data row3 col0" >
                    0.13
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row3_col1"
                 class="data row3 col1" >
                    -0.091
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row3_col2"
                 class="data row3 col2" >
                    -0.14
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row3_col3"
                 class="data row3 col3" >
                    1
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row3_col4"
                 class="data row3 col4" >
                    -0.048
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row3_col5"
                 class="data row3 col5" >
                    0.15
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row3_col6"
                 class="data row3 col6" >
                    -0.38
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row3_col7"
                 class="data row3 col7" >
                    0.23
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row3_col8"
                 class="data row3 col8" >
                    0.11
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row3_col9"
                 class="data row3 col9" >
                    0.11
                
                
            </tr>
            
            <tr>
                
                
                <th id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530"
                 class="row_heading level0 row4" rowspan=1>
                    pH_int
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row4_col0"
                 class="data row4 col0" >
                    -0.9
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row4_col1"
                 class="data row4 col1" >
                    1
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row4_col2"
                 class="data row4 col2" >
                    0.99
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row4_col3"
                 class="data row4 col3" >
                    -0.048
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row4_col4"
                 class="data row4 col4" >
                    1
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row4_col5"
                 class="data row4 col5" >
                    0.67
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row4_col6"
                 class="data row4 col6" >
                    0.78
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row4_col7"
                 class="data row4 col7" >
                    0.18
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row4_col8"
                 class="data row4 col8" >
                    -0.64
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row4_col9"
                 class="data row4 col9" >
                    -0.66
                
                
            </tr>
            
            <tr>
                
                
                <th id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530"
                 class="row_heading level0 row5" rowspan=1>
                    O2_umolkg
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row5_col0"
                 class="data row5 col0" >
                    -0.35
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row5_col1"
                 class="data row5 col1" >
                    0.64
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row5_col2"
                 class="data row5 col2" >
                    0.62
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row5_col3"
                 class="data row5 col3" >
                    0.15
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row5_col4"
                 class="data row5 col4" >
                    0.67
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row5_col5"
                 class="data row5 col5" >
                    1
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row5_col6"
                 class="data row5 col6" >
                    0.28
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row5_col7"
                 class="data row5 col7" >
                    -0.03
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row5_col8"
                 class="data row5 col8" >
                    -0.12
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row5_col9"
                 class="data row5 col9" >
                    -0.15
                
                
            </tr>
            
            <tr>
                
                
                <th id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530"
                 class="row_heading level0 row6" rowspan=1>
                    temp_SBE
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row6_col0"
                 class="data row6 col0" >
                    -0.86
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row6_col1"
                 class="data row6 col1" >
                    0.83
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row6_col2"
                 class="data row6 col2" >
                    0.86
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row6_col3"
                 class="data row6 col3" >
                    -0.38
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row6_col4"
                 class="data row6 col4" >
                    0.78
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row6_col5"
                 class="data row6 col5" >
                    0.28
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row6_col6"
                 class="data row6 col6" >
                    1
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row6_col7"
                 class="data row6 col7" >
                    0.097
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row6_col8"
                 class="data row6 col8" >
                    -0.82
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row6_col9"
                 class="data row6 col9" >
                    -0.83
                
                
            </tr>
            
            <tr>
                
                
                <th id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530"
                 class="row_heading level0 row7" rowspan=1>
                    sal_SBE
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row7_col0"
                 class="data row7 col0" >
                    -0.2
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row7_col1"
                 class="data row7 col1" >
                    0.18
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row7_col2"
                 class="data row7 col2" >
                    0.15
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row7_col3"
                 class="data row7 col3" >
                    0.23
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row7_col4"
                 class="data row7 col4" >
                    0.18
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row7_col5"
                 class="data row7 col5" >
                    -0.03
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row7_col6"
                 class="data row7 col6" >
                    0.097
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row7_col7"
                 class="data row7 col7" >
                    1
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row7_col8"
                 class="data row7 col8" >
                    -0.37
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row7_col9"
                 class="data row7 col9" >
                    -0.37
                
                
            </tr>
            
            <tr>
                
                
                <th id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530"
                 class="row_heading level0 row8" rowspan=1>
                    V_batt_elec
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row8_col0"
                 class="data row8 col0" >
                    0.81
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row8_col1"
                 class="data row8 col1" >
                    -0.68
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row8_col2"
                 class="data row8 col2" >
                    -0.68
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row8_col3"
                 class="data row8 col3" >
                    0.11
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row8_col4"
                 class="data row8 col4" >
                    -0.64
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row8_col5"
                 class="data row8 col5" >
                    -0.12
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row8_col6"
                 class="data row8 col6" >
                    -0.82
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row8_col7"
                 class="data row8 col7" >
                    -0.37
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row8_col8"
                 class="data row8 col8" >
                    1
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row8_col9"
                 class="data row8 col9" >
                    0.99
                
                
            </tr>
            
            <tr>
                
                
                <th id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530"
                 class="row_heading level0 row9" rowspan=1>
                    charge_status
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row9_col0"
                 class="data row9 col0" >
                    0.83
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row9_col1"
                 class="data row9 col1" >
                    -0.7
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row9_col2"
                 class="data row9 col2" >
                    -0.7
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row9_col3"
                 class="data row9 col3" >
                    0.11
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row9_col4"
                 class="data row9 col4" >
                    -0.66
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row9_col5"
                 class="data row9 col5" >
                    -0.15
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row9_col6"
                 class="data row9 col6" >
                    -0.83
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row9_col7"
                 class="data row9 col7" >
                    -0.37
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row9_col8"
                 class="data row9 col8" >
                    0.99
                
                
                
                <td id="T_ed8c5e4c_48d5_11e8_b86a_f40f242f5530row9_col9"
                 class="data row9 col9" >
                    1
                
                
            </tr>
            
        </tbody>
        </table>
        


