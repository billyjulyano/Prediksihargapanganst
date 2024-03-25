import function as mf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
from pytorch_forecasting import TemporalFusionTransformer
from functools import reduce
import warnings
warnings.filterwarnings("ignore")


st.set_page_config(page_title='Prediksi Harga Pangan', layout='wide', initial_sidebar_state='auto')

model = mf.model_import('samplemodel.ckpt')

# data = mf.excel_import('sample_data.xlsx')
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

st.sidebar.image ('logobapanas.jpg')
st.sidebar.header('Dashboard Prediksi Harga Pangan')

st.sidebar.markdown('# [Pergerakan Historis](#1)')
st.sidebar.markdown('# [Visualisasi Data](#2)')
st.sidebar.markdown('# [Prediksi Model](#3)')


st.title('Prediksi Harga Pangan')  
st.header('Pergerakan historis harga pangan', divider='green')  

with st.form("my_form"):

    option = st.selectbox(
        "Tipe Komunitas",
        ("BerasPremium", "BerasMedium",),
        placeholder="Pilih",
        )
    st.write('Pilihan:', option)
    tanggal_awal = data['Tanggal'].min()
    tanggal_akhir =data['Tanggal'].max()
    ds = st.date_input("Tanggal Awal Historis",min_value=tanggal_awal, max_value= tanggal_akhir ,value = pd.to_datetime('2023-12-01'))
    ds = pd.to_datetime(ds)
    de = st.date_input("Tanggal Akhir Historis",min_value=tanggal_awal, max_value=tanggal_akhir, value = pd.to_datetime('2024-01-01'))
    de = pd.to_datetime(de)
    submitted = st.form_submit_button("Submit")
    if submitted:
       pass

df_baru = data[(data['jenis'] == option) & (data['Tanggal'] >= ds) & (data['Tanggal'] <= de)]

st.subheader('Pergerakan Historis Harga Pangan', divider='blue', anchor = '1')

def create_chart_price_historical(df):
    lowest = df['harga'].min()
    highest = df['harga'].max()
    hover = alt.selection_point(
        fields=["Tanggal"],
        nearest=True,
        on="mouseover",
        empty=False,
    )
    lines = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x="Tanggal",
            y = alt.Y('harga', scale=alt.Scale(domain=[lowest-10, highest+30])),
            )       
        )
    points = lines.transform_filter(hover).mark_circle(size=100)
    tooltips = (
        alt.Chart(df)
        .mark_rule()
        .encode(
            x="Tanggal",
            y="harga",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Tanggal", title="Date"),
                alt.Tooltip("harga", title="Price (IDR)"),
            ],
        )
        .add_params(hover)
    )
    return (lines + points + tooltips).interactive()

historychart = mf.create_chart_price_historical(df_baru)
st.altair_chart((historychart).interactive(), use_container_width=True)
    

with st.form("stok"):

    pilihanstok = st.selectbox(
        "Pilih Stok",
        ("StokCBP", "LuasPanen",),
        placeholder="Pilih",
        )
    st.write('Pilihan:', option)
    tanggal_awal = data['Tanggal'].min()
    tanggal_akhir =data['Tanggal'].max()
    ds = st.date_input("Tanggal Awal Historis",min_value=tanggal_awal, max_value= tanggal_akhir ,value = pd.to_datetime('2023-12-01'))
    ds = pd.to_datetime(ds)
    de = st.date_input("Tanggal Akhir Historis",min_value=tanggal_awal, max_value=tanggal_akhir, value = pd.to_datetime('2024-01-01'))
    de = pd.to_datetime(de)
    submitted = st.form_submit_button("Submit")
    if submitted:
       pass

df_stok = data[(data['jenis'] == option) & (data['Tanggal'] >= ds) & (data['Tanggal'] <= de)]

st.subheader('Pergerakan Historis Data Support', divider='blue', anchor = '2')

def create_chart_stok(df):
    lowest = df[pilihanstok].min()
    highest = df[pilihanstok].max()
    hover = alt.selection_point(
        fields=["Tanggal"],
        nearest=True,
        on="mouseover",
        empty=False,
    )
    lines = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x="Tanggal",
            y = alt.Y(pilihanstok, scale=alt.Scale(domain=[lowest-10, highest+30])),
            )       
        )
    points = lines.transform_filter(hover).mark_circle(size=100)
    tooltips = (
        alt.Chart(df)
        .mark_rule()
        .encode(
            x="Tanggal",
            y=pilihanstok,
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Tanggal", title="Date"),
                alt.Tooltip(pilihanstok, title="Stok"),
            ],
        )
        .add_params(hover)
    )
    return (lines + points + tooltips).interactive()

datastok=create_chart_stok(df_stok)
st.altair_chart((datastok).interactive(), use_container_width=True)
    

 