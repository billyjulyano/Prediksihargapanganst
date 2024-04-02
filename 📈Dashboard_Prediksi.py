import function as mf
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
from pytorch_forecasting import TemporalFusionTransformer
from functools import reduce
import datetime
import locale
import locale;locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
import warnings
warnings.filterwarnings("ignore")


st.set_page_config(page_title='Prediksi Harga Pangan', layout='wide', initial_sidebar_state='auto',page_icon="🌾")

model = mf.model_import('samplemodel.ckpt') 
output_dict = model._hparams.embedding_labels['jenis']

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

#headersidebar
st.sidebar.header('Dashboard Prediksi Harga Pangan') 

#himagesidebar
st.sidebar.image('logogabungan.png')

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


max_prediction_length = 30
max_encoder_length = 60

with st.form("prediksi"):
    st.subheader('Set Parameter', divider='blue', anchor = '3')
    latest_data = data['Tanggal'].max()
    pilihan_komoditas_prediksi = st.selectbox(
        "Pilih Jenis",
        ("BerasPremium", "BerasMedium",),
        placeholder="Pilih",
        )
    tanggal_awal_prediksi = st.date_input("Tanggal Awal prediksi", value = latest_data + datetime.timedelta(days=1))
    pred_button = st.form_submit_button("Run prediction")

if pred_button:
    encoder, extended_df = mf.create_outofsample_base(data, df_merged, tanggal_awal_prediksi, max_encoder_length, max_prediction_length)
    extended_df_time = mf.create_time_features(extended_df)
    decoder = mf.create_decoder(extended_df_time, max_prediction_length)

    new_prediction_data = pd.concat([encoder, decoder], ignore_index=True)
    raw_result = mf.do_pred(model, new_prediction_data)

    pred_date_index = decoder[decoder['jenis'] == pilihan_komoditas_prediksi]['Tanggal']
    df_prediction = mf.filter_prediction(raw_result, output_dict, pilihan_komoditas_prediksi, pred_date_index)

    alt_predchart = mf.create_chart_pred(df_prediction)

    st.markdown('#### Grafik')
    st.altair_chart((alt_predchart).interactive(), use_container_width=True)

    st.markdown('##### Matriks')

    filtered_data = data[data['jenis'] == pilihan_komoditas_prediksi]
    mean_last_30 = round(filtered_data.tail(30)['harga'].mean())
    mean_pred = round(df_prediction['Harga Prediksi'].mean())
    
    percentage_difference = (round(((mean_pred - mean_last_30) / mean_last_30) * 100,1))
    st.metric('Rata-rata harga prediksi', locale.currency(mean_pred, grouping=True)[:-3], f'{percentage_difference}%')
