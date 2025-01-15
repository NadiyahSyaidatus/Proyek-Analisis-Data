import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

st.set_page_config(page_title="Dashboard Penyewaan Sepeda", page_icon="🚲")

st.markdown(
    """
    <style>
    
    .css-18e3th9 {
        background-color: #E6E6FA; 
    }
  
    .css-1d391kg {
        background-color: #FF69B4; 
    }
    </style>
    """, unsafe_allow_html=True)

sns.set(style='darkgrid')


st.title("Dashboard Penyewaan Sepeda")

st.sidebar.header("Menu")
option = st.sidebar.selectbox("Pilih Analisis:", 
                               ("Rata-rata Penyewaan Sepeda", "Visualisasi Musim", "Penyewaan Hari Libur vs Hari Biasa"))

data_path = "all_data.csv"
all_data = pd.read_csv(data_path)


if option == "Rata-rata Penyewaan Sepeda":
    st.subheader("Rata-rata Penyewaan Sepeda per Musim")
    
    seasonal_rentals = all_data.groupby('season_x')['total_count_y'].mean().reset_index() 

    fig, ax = plt.subplots(figsize=(10, 6)) 
    sns.barplot(x='season_x', y='total_count_y', data=seasonal_rentals, palette='Set2', ax=ax)
    plt.title("Rata-rata Penyewaan Sepeda per Musim", fontsize=16, color='purple')
    plt.xlabel("Musim", fontsize=12)
    plt.ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
    plt.grid(axis='y', color='pink')
    st.pyplot(fig)

elif option == "Visualisasi Musim":
    st.subheader("Visualisasi Penyewaan Sepeda Berdasarkan Musim")
    
    seasonal_rentals = all_data.groupby('season_x')['total_count_y'].sum().reset_index()  

    fig, ax = plt.subplots(figsize=(8, 8)) 
    wedges, texts, autotexts = ax.pie(seasonal_rentals['total_count_y'], 
                                       labels=seasonal_rentals['season_x'], 
                                       autopct='%1.1f%%', startangle=90,
                                       colors=sns.color_palette('Set2', len(seasonal_rentals)))
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    plt.title("Penyewaan Sepeda Berdasarkan Musim", fontsize=16, color='purple')
    plt.axis('equal') 
    st.pyplot(fig)

elif option == "Penyewaan Hari Libur vs Hari Biasa":
    st.subheader("Penyewaan Sepeda pada Hari Libur vs Hari Biasa")
    
    holiday_rentals = all_data.groupby('holiday_y')['total_count_y'].mean().reset_index() 
    holiday_rentals['holiday_y'] = holiday_rentals['holiday_y'].replace({0: 'Hari Biasa', 1: 'Hari Libur'})

    fig, ax = plt.subplots(figsize=(10, 6))  
    sns.barplot(x='holiday_y', y='total_count_y', data=holiday_rentals, palette='Set2', ax=ax)
    plt.title("Rata-rata Penyewaan Sepeda pada Hari Libur vs Hari Biasa", fontsize=16, color='purple')
    plt.xlabel("Tipe Hari", fontsize=12)
    plt.ylabel("Rata-rata Penyewaan Sepeda", fontsize=12)
    plt.grid(axis='y', color='pink')
    st.pyplot(fig)

if __name__ == "__main__":
    st.write("Dashboard ini dibangun menggunakan Streamlit.")
