
#%%

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


# ### Read in flow simulation data for various endcaps and visualize to see variability in performance

# In[10]:


cwd = os.getcwd()
filename = 'V3.2_Flow_Sim.xlsx'
filepath = os.path.join(cwd, 'Data', filename)

df_3p2_3D = pd.read_excel(filepath)

df_3p2_3D.drop(index = 0, inplace = True) # bad row
df_3p2_3D.dropna(axis = 0, inplace = True)
df_3p2_3D['Residence time [s]'] = df_3p2_3D['Residence time [s]'].astype('float')


# In[11]:


df_3p2_3D.head(100)


# In[12]:


df_3p2_3D.shape


# In[15]:


fig2 = plt.figure(figsize = [8, 8])
df_3p2_3D.hist(bins = 100)

