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
                               ("Rata-rata Penyewaan Sepeda", "tren penyewaan sepeda dari tahun ke tahun", "Penyewaan Hari Libur vs Hari Biasa"))

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

elif option == "tren penyewaan sepeda dari tahun ke tahun":
    st.subheader("Persentase penyewaan sepeda dari tahun ke tahun")

    # Mengelompokkan data berdasarkan tahun dan menghitung total penyewaan sepeda per tahun
    yearly_rentals = all_data.groupby('year')['total_count'].sum().reset_index()
    yearly_rentals['year'] = yearly_rentals['year'].replace({0: 2011, 1: 2012})
    total_rentals = yearly_rentals['total_count'].sum()

    # Menambahkan kolom persentase untuk setiap tahun
    yearly_rentals['percentage'] = (yearly_rentals['total_count'] / total_rentals) * 100

    # Membuat visualisasi bar chart
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x='year', y='percentage', data=yearly_rentals, palette='Set2', ax=ax)

    # Menambahkan detail pada plot
    ax.set_title('Persentase Penyewaan Sepeda dari Tahun ke Tahun', fontsize=16, color='purple')
    ax.set_xlabel('Tahun', fontsize=12)
    ax.set_ylabel('Persentase Penyewaan Sepeda (%)', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Menampilkan plot di Streamlit
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
