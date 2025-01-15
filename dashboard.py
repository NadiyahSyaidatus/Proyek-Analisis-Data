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
    
    # Menghitung rata-rata penyewaan sepeda per musim
    seasonal_rentals = all_data.groupby('season_x')['total_count_y'].mean().reset_index()

    # Membuat plot donat chart
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        seasonal_rentals['total_count_y'], 
        labels=seasonal_rentals['season_x'], 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=sns.color_palette('Set2', len(seasonal_rentals))
    )
    
    # Menambahkan lingkaran di tengah untuk membuat grafik menjadi donat
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    
    # Pengaturan tambahan
    plt.title("Rata-rata Penyewaan Sepeda per Musim", fontsize=16, color='purple')
    plt.axis('equal')  # Menjaga proporsi grafik
    
    # Menampilkan grafik ke Streamlit
    st.pyplot(fig)


elif option == "tren penyewaan sepeda dari tahun ke tahun":
    st.subheader("Persentase Penyewaan Sepeda dari Tahun ke Tahun")

    # Mengelompokkan data berdasarkan tahun dan menghitung total penyewaan sepeda per tahun
    yearly_rentals = all_data.groupby('year_x')['total_count_y'].sum().reset_index()
    yearly_rentals['year_x'] = yearly_rentals['year_x'].replace({0: 2011, 1: 2012})
    total_rentals = yearly_rentals['total_count_y'].sum()

    # Menambahkan kolom persentase untuk setiap tahun
    yearly_rentals['percentage'] = (yearly_rentals['total_count_y'] / total_rentals) * 100

    # Membuat visualisasi pie chart
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(
        yearly_rentals['percentage'],
        labels=yearly_rentals['year_x'],
        autopct='%1.1f%%',
        startangle=90,
        colors=['#66c2a5', '#fc8d62']
    )
    ax.set_title('Persentase Penyewaan Sepeda dari Tahun ke Tahun', fontsize=16, color='purple')

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
