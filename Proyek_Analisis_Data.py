#!/usr/bin/env python
# coding: utf-8

# # Proyek Analisis Data: [Bike Sharing]
# - **Nama:** Nadiyah Syaidatus Shofa Abdul Hayat
# - **Email:** nadiyahsyaidatus.sah@gmail.com
# - **ID Dicoding:** nadiyahsah

# ## Menentukan Pertanyaan Bisnis

# - Apakah penyewaan sepeda meningkat atau menurun pada hari libur ?
# - Bagaimana pengaruh musim terhadap penyewaan sepeda?
# - Bagaimana tren penyewaan sepeda dari tahun ke tahun?

# ## Import Semua Packages/Library yang Digunakan

# In[67]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np


# ## Data Wrangling

# ### Gathering Data

# In[68]:


df_day = pd.read_csv("data/day.csv")
df_day.head()


# In[69]:


df_hour = pd.read_csv("data/hour.csv")
df_hour.head()


# **Insight:**
# - seluruh kolom dari semua data telah terlihat dan dapat diamati untuk bagaimana mengolahnya

# ### Assessing Data

# In[70]:


df_day.info()


# In[71]:


df_day = pd.read_csv("data/day.csv")
df_day.isnull().sum()


# In[72]:


print("Jumlah duplikasi tabel day: ", df_day.duplicated().sum())


# In[73]:


df_day.describe()


# In[74]:


df_hour.info()


# In[75]:


df_hour = pd.read_csv("data/hour.csv")
df_hour.isnull().sum()


# In[76]:


print("Jumlah duplikasi tabel hour: ", df_hour.duplicated().sum())


# In[77]:


df_hour.describe()


# **Insight:**
# pada kedua dataset tersebut tidak ditemukan adanya duplikasi

# ### Cleaning Data

# #### Change Value

# In[78]:


df_day.season.replace((1,2,3,4), ('Spring','Summer','Fall','Winter'), inplace=True)
df_hour.season.replace((1,2,3,4), ('Spring','Summer','Fall','Winter'), inplace=True)


# #### Drop

# In[79]:


columns_to_drop = ['atemp', 'weekday']
df_day.drop([col for col in columns_to_drop if col in df_day.columns], axis=1, inplace=True)
df_hour.drop([col for col in columns_to_drop if col in df_hour.columns], axis=1, inplace=True)


# #### Rename Coloum

# In[80]:


df_day.rename(columns={
    'dteday': 'date',
    'yr': 'year',
    'weathersit': 'weather',
    'mnth': 'month',
    'hum': 'humidity',
    'cnt': 'total_count'
}, inplace=True)

df_hour.rename(columns={
    'dteday': 'date',
    'yr': 'year',
    'weathersit': 'weather',
    'mnth': 'month',
    'hr': 'hour',
    'hum': 'humidity',
    'cnt': 'total_count'
}, inplace=True)


# In[81]:


print(df_day.head())
print(df_hour.head())


# **Insight:**
# -pada cleaning dilakukan drop pada kolom weekday dan atemp karena sudah ada kolom yang serupa yaitu workingday dan temp
# 

# ## Exploratory Data Analysis (EDA)

# #### Deskripsi Data

# In[82]:


print(df_day.describe(include="all"))
print(df_hour.describe(include="all"))


# ##### rata rata workingday

# In[83]:


workingday_stats = df_day.groupby('workingday').agg({
    'total_count': ['mean', 'median', 'std', 'min', 'max', lambda x: x.mode()[0]] 
})
workingday_stats.columns = ['mean', 'median', 'std', 'min', 'max', 'mode']
print(workingday_stats)


# #### rata rata holiday

# In[84]:


holiday_stats = df_day.groupby('holiday').agg({
    'total_count': ['mean', 'median', 'std', 'min', 'max', lambda x: x.mode()[0]]  # Menambahkan modus
})
holiday_stats.columns = ['mean', 'median', 'std', 'min', 'max', 'mode']
print(holiday_stats)


# #### Penyewaan berdasarkan musim

# In[85]:


# Menghitung jumlah penyewaan sepeda per musim
seasonal_rentals = df_day.groupby(by='season')['total_count'].sum().sort_values(ascending=False).reset_index()
seasonal_rentals.columns = ['season', 'total_count'] 
print(seasonal_rentals)


# #### rata rata berdasarkan musim

# In[86]:


season_stats = df_day.groupby(by='season').agg({
    'total_count': ['mean', 'median', 'std', 'min', 'max', lambda x: x.mode()[0]]  
})
season_stats.columns = ['mean', 'median', 'std', 'min', 'max', 'mode']
print(season_stats.sort_values(by='mean', ascending=False))


# #### Total penyewaan berdasarkan tahun

# In[87]:


yearly_rentals = df_day.groupby(by='year')['total_count'].sum().sort_values(ascending=False).reset_index()
yearly_rentals.columns = ['year', 'total_count'] 
print(yearly_rentals)


# #### ratarata penyewaan berdasarkan tahun

# In[88]:


yearly_stats = df_day.groupby(by='year').agg({
    'total_count': ['mean', 'median', 'std', 'min', 'max', lambda x: x.mode()[0]]  # Menambahkan modus
})
yearly_stats.columns = ['mean', 'median', 'std', 'min', 'max', 'mode']
print(yearly_stats.sort_values(by='mean', ascending=False))


# In[89]:


all_data = pd.merge(
    left=df_day,
    right=df_hour,
    how="left", 
    left_on="date",
    right_on="date"
)

print(all_data.head(10))

print(all_data.describe(include="all"))


# In[90]:


output_csv_path = "C:\\Users\\USER\\submission2\\data\\"

all_data.to_csv(output_csv_path + 'all_data.csv', index=False)


# ## Visualization & Explanatory Analysis

# ### Pertanyaan 1:

# ##### Apakah penyewaan sepeda meningkat atau menurun pada hari libur ?

# In[91]:


holiday_rentals = df_day.groupby('holiday')['total_count'].mean().reset_index()
holiday_rentals['holiday'] = holiday_rentals['holiday'].replace({0: 'Working day', 1: 'Holiday'})
plt.figure(figsize=(8, 6))
sns.barplot(x='holiday', y='total_count', data=holiday_rentals, palette='Set2')
plt.title('Rata-Rata Penyewaan Sepeda pada Hari Libur vs Hari Biasa', fontsize=16)
plt.xlabel('Tipe Hari', fontsize=12)
plt.ylabel('Rata-Rata Penyewaan Sepeda', fontsize=12)
plt.grid(axis='y')
plt.show()


# ##### Dari grafik ini, terlihat bahwa rata-rata penyewaan sepeda pada hari kerja (Working Day) lebih tinggi dibandingkan dengan hari libur (Holiday). Hal ini menunjukkan bahwa masyarakat lebih cenderung menggunakan sepeda untuk aktivitas sehari-hari, seperti pergi ke kantor atau sekolah, pada saat hari kerja. 

# ### Pertanyaan 2:

# ##### Bagaimana pengaruh musim terhadap penyewaan sepeda?

# In[92]:


seasonal_rentals = df_day.groupby('season')['total_count'].mean().reset_index()
seasonal_rentals['season'] = seasonal_rentals['season'].replace({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
plt.figure(figsize=(8, 8))
plt.pie(seasonal_rentals['total_count'], labels=seasonal_rentals['season'], autopct='%1.1f%%', startangle=90)
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.title('Rata-Rata Penyewaan Sepeda Berdasarkan Musim', fontsize=16)
plt.axis('equal') 
plt.show()


# ##### Dari diagram lingkaran ini, terlihat bahwa penyewaan sepeda paling tinggi terjadi di musim gugur, diikuti oleh musim panas, musim dingin, dan musim semi. Dominasi musim gugur dalam penyewaan sepeda mungkin terkait dengan cuaca yang cukup hangat namun tidak terlalu dingin sehingga lebih banyak kegiatan luar ruangan yang dilakukan orang.

# ### Pertanyaan 3:

# ##### Bagaimana tren penyewaan sepeda dari tahun ke tahun?

# In[93]:


yearly_rentals = df_day.groupby('year')['total_count'].sum().reset_index()
yearly_rentals['year'] = yearly_rentals['year'].replace({0: 2011, 1: 2012})
total_rentals = yearly_rentals['total_count'].sum()
yearly_rentals['percentage'] = (yearly_rentals['total_count'] / total_rentals) * 100
plt.figure(figsize=(8, 6))
sns.barplot(x='year', y='percentage', data=yearly_rentals, palette='Set2')
plt.title('Persentase Penyewaan Sepeda dari Tahun ke Tahun', fontsize=16)
plt.xlabel('Tahun', fontsize=12)
plt.ylabel('Persentase Penyewaan Sepeda (%)', fontsize=12)
plt.grid(axis='y')
plt.show()


# ##### Grafik ini menunjukkan perbandingan persentase penyewaan sepeda antara tahun 2011 dan 2012. Jika kita melihat bahwa terdapat peningkatan persentase penyewaan sepeda dari tahun ke tahun, ini dapat diartikan bahwa semakin banyak orang yang beralih ke penggunaan sepeda sebagai sarana transportasi

# ## Conclusion

# #### - Conslusion Pertanyaan 1:
# ##### Hasil analisis menunjukkan bahwa rata-rata penyewaan sepeda pada hari kerja jauh lebih tinggi dibandingkan dengan hari libur. Hal ini mengindikasikan bahwa masyarakat lebih cenderung menggunakan sepeda untuk aktivitas sehari-hari, seperti pergi ke kantor, sekolah, atau berbelanja, pada saat hari kerja. Beberapa faktor yang mungkin mempengaruhi kecenderungan ini adalah kebutuhan masyarakat untuk bertransportasi secara efisien dan menghindari kemacetan, serta dorongan untuk menggunakan sepeda sebagai alternatif yang lebih sehat dan ramah lingkungan. Meskipun hari libur memberikan kesempatan untuk beraktivitas di luar rumah, tampaknya banyak orang lebih memilih sepeda sebagai sarana transportasi utama mereka saat hari kerja.
# #### - Conclusion pertanyaan 2:
# ##### Dari analisis yang dilakukan, terlihat bahwa musim gugur memiliki persentase rata-rata penyewaan tertinggi dibandingkan dengan musim lainnya, seperti musim semi, musim panas, dan musim dingin. Hal ini menunjukkan bahwa banyak orang cenderung memilih untuk menyewa sepeda pada musim gugur, mungkin karena suhu yang sejuk dan cuaca yang nyaman untuk beraktivitas luar ruangan. Selain itu, pemandangan alam yang berubah warna di musim gugur mungkin memberikan daya tarik tersendiri bagi pengguna sepeda.
# #### - Conclution pertanyaan 3:
# ##### Grafik yang menunjukkan persentase penyewaan sepeda antara tahun 2011 dan 2012 mengindikasikan bahwa jumlah penyewa pada tahun 2012 lebih tinggi dibandingkan tahun 2011. Peningkatan ini dapat diartikan sebagai tren positif dalam penggunaan sepeda sebagai sarana transportasi

# In[ ]:




