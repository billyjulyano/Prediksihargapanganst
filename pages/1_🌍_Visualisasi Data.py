import function as mf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
from pytorch_forecasting import TemporalFusionTransformer
from functools import reduce
import datetime
import warnings
warnings.filterwarnings("ignore")


st.set_page_config(page_title='Prediksi Harga Pangan', layout='wide', initial_sidebar_state='auto',page_icon="👋")

# import all data
df_datasupport_monthly = pd.read_excel('datasupport.xlsx')
df_datasupport_cipinang = pd.read_excel('datasupport.xlsx', sheet_name='DailyCipinang')
df_occasion = pd.read_excel('datasupport.xlsx', sheet_name='specialdays')
df_price = pd.read_excel('price.xlsx')

df_datasupport_monthly_p = mf.interpolate_df(df_datasupport_monthly)
df_occasion_p = mf.preprocess_occasion(df_occasion)


data_frames = [df_datasupport_monthly_p, df_occasion_p, df_price]
df_merged = reduce(lambda left, right: pd.merge(left, right, on=['Tanggal'],how='outer'), data_frames)
df_merged.dropna(inplace=True)

data = mf.create_time_features(df_merged)

st.sidebar.header('Dashboard Prediksi Harga Pangan')
st.sidebar.image('logogabungan.png')

st.title('Visualisasi Data Harga')   
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {

  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center center;
  background-repeat: repeat;
  background-image: url("data:image/svg+xml;utf8,%3Csvg viewBox=%220 0 500 500%22 xmlns=%22http:%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cdefs%3E%3ClinearGradient id=%22b%22 gradientTransform=%22rotate(-45 .5 .5)%22%3E%3Cstop offset=%220%25%22 stop-color=%22%2308AEEA%22%2F%3E%3Cstop offset=%22100%25%22 stop-color=%22%232AF598%22%2F%3E%3C%2FlinearGradient%3E%3CclipPath id=%22a%22%3E%3Cpath fill=%22currentColor%22 d=%22M668.5 733Q500 966 289 733t0-464.5q211-231.5 379.5 0t0 464.5Z%22%2F%3E%3C%2FclipPath%3E%3C%2Fdefs%3E%3Cg clip-path=%22url(%23a)%22%3E%3Cpath fill=%22url(%23b)%22 d=%22M668.5 733Q500 966 289 733t0-464.5q211-231.5 379.5 0t0 464.5Z%22%2F%3E%3C%2Fg%3E%3C%2Fsvg%3E");


}
[data-testid="stSidebarContent"] {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center center;
  background-repeat: repeat;
  background-image: url("data:image/svg+xml;utf8,%3Csvg viewBox=%220 0 1000 400%22 xmlns=%22http:%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cdefs%3E%3ClinearGradient id=%22b%22 gradientTransform=%22rotate(-45 .5 .5)%22%3E%3Cstop offset=%220%25%22 stop-color=%22%2308AEEA%22%2F%3E%3Cstop offset=%22100%25%22 stop-color=%22%232AF598%22%2F%3E%3C%2FlinearGradient%3E%3CclipPath id=%22a%22%3E%3Cpath fill=%22currentColor%22 d=%22M658 714q-158 214-405 0t0-370q247-156 405 0t0 370Z%22%2F%3E%3C%2FclipPath%3E%3C%2Fdefs%3E%3Cg clip-path=%22url(%23a)%22%3E%3Cpath fill=%22url(%23b)%22 d=%22M658 714q-158 214-405 0t0-370q247-156 405 0t0 370Z%22%2F%3E%3C%2Fg%3E%3C%2Fsvg%3E");

}
</style>
"""

st.markdown(page_bg_img,unsafe_allow_html=True)


with st.form("price_history_form"):
    st.subheader('Pilih Parameter', divider='green', anchor = '1') 
    pilihan_komoditas = st.selectbox(
        "Tipe Komunitas",
        ("BerasPremium", "BerasMedium",),
        placeholder="Pilih",
        )
    tanggal_awal = data['Tanggal'].min()
    tanggal_akhir = data['Tanggal'].max()
    
    ds = st.date_input("Tanggal Awal Historis", min_value=tanggal_awal, max_value= tanggal_akhir, value = tanggal_akhir - datetime.timedelta(days=90))
    ds = pd.to_datetime(ds)
    de = st.date_input("Tanggal Akhir Historis", min_value=tanggal_awal, max_value=tanggal_akhir, value = tanggal_akhir)
    de = pd.to_datetime(de)
    st.form_submit_button("Submit")

price_history = data[(data['jenis'] == pilihan_komoditas) & (data['Tanggal'] >= ds) & (data['Tanggal'] <= de)]

alt_historychart = mf.create_chart_price_historical(price_history)
st.markdown('#### Grafik')
st.altair_chart((alt_historychart).interactive(), use_container_width=True)

st.title('Visualisasi Data Support')   
with st.form("stok"):
    st.subheader('Pilih Parameter', divider='green', anchor = '1') 
    pilihanstok = st.selectbox(
        "Pilih Stok",
        ("StokCBP", "LuasPanen",),
        placeholder="Pilih",
        )

    tanggal_awal = data['Tanggal'].min()
    tanggal_akhir =data['Tanggal'].max()
    ds = st.date_input("Tanggal Awal Historis",min_value=tanggal_awal, max_value= tanggal_akhir ,value = tanggal_akhir - datetime.timedelta(days=180))
    ds = pd.to_datetime(ds)
    de = st.date_input("Tanggal Akhir Historis",min_value=tanggal_awal, max_value=tanggal_akhir, value = tanggal_akhir)
    de = pd.to_datetime(de)
    st.form_submit_button("Submit")

df_stok = data[(data['jenis'] == pilihan_komoditas) & (data['Tanggal'] >= ds) & (data['Tanggal'] <= de)]

alt_datastok = mf.create_chart_stok(df_stok, pilihanstok)
st.markdown('#### Grafik')
st.altair_chart((alt_datastok).interactive(), use_container_width=True)