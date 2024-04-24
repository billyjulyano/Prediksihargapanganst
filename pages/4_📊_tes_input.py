import streamlit as st
import pandas as pd
import function as mf
from functools import reduce

# css file
with open('style.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.sidebar.header('Dashboard Prediksi Harga Pangan')
st.sidebar.image('logogabungan.png')

st.session_state['creds'] = True

if 'creds' not in st.session_state:
    st.session_state['creds'] = False

if st.session_state['creds']:
    st.title('👋🏻 Silahkan Input Harga')

    df_datasupport_monthly = pd.read_excel('datasupport.xlsx')
    df_datasupport_cipinang = pd.read_excel('datasupport.xlsx', sheet_name='DailyCipinang')
    df_occasion = pd.read_excel('datasupport.xlsx', sheet_name='specialdays')
    df_price = pd.read_excel('price.xlsx')

    df_datasupport_monthly_p = mf.interpolate_df(df_datasupport_monthly)
    df_occasion_p = mf.preprocess_occasion(df_occasion)


    data_frames = [df_datasupport_monthly_p, df_occasion_p, df_price]
    original_df = reduce(lambda left, right: pd.merge(left, right, on=['Tanggal'], how='outer'), data_frames)
    original_df = original_df[['BerasPremium', 'BerasMedium', 'ProduksiBeras', 'occasion']]
    original_df.dropna(inplace=True)

    new_df = st.data_editor(original_df.tail(15), hide_index = True)

else:
    st.title('Silahkan Login dahulu❕')





