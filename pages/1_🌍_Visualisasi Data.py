import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

st.set_page_config(
    page_title="Prediksi Harga Pangan",
    page_icon="👋",
)


data = pd.read_excel('sample_data.xlsx')
data['Tanggal'] = pd.to_datetime(data['Tanggal'])


st.sidebar.image ('logobapanas.jpg')
st.sidebar.header('Prediksi Harga Pangan')


st.sidebar.markdown('# [Visualisasi Data](#2)')

st.title('Visualisasi Data')  
    

with st.form("stok"):

    pilihanstok = st.selectbox(
        "Pilih Stok",
        ("StokA", "StokB",),
        placeholder="Pilih",
        )
    st.write('Pilihan:', option)
    tanggal_awal = data['Tanggal'].min()
    tanggal_akhir =data['Tanggal'].max()
    ds = st.date_input("Tanggal Awal Historis",min_value=tanggal_awal, max_value= tanggal_akhir ,value = pd.to_datetime('2024-01-01'))
    ds = pd.to_datetime(ds)
    de = st.date_input("Tanggal Akhir Historis",min_value=tanggal_awal, max_value=tanggal_akhir, value = pd.to_datetime('2024-01-12'))
    de = pd.to_datetime(de)


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

    submitted = st.form_submit_button("Submit")
    if submitted:
       pass

df_stok = data[(data['Jenis'] == option) & (data['Tanggal'] >= ds) & (data['Tanggal'] <= de)]

st.subheader('Pergerakan Visualisasi Data Support', divider='blue')



datastok=create_chart_stok(df_stok)
st.altair_chart((datastok).interactive(), use_container_width=True)
    

 