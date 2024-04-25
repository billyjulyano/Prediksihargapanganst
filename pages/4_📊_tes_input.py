import streamlit as st
import pandas as pd
import function as mf
from functools import reduce
from datetime import datetime, timedelta

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

    df_datasupport_monthly = pd.read_excel('datasupport2.xlsx')
    df_datasupport_monthly = df_datasupport_monthly[['Tanggal','Tahun', 'Bulan', 'ProduksiBeras']]
    df_datasupport_pibc = pd.read_excel('datasupport2.xlsx', sheet_name='DailyCipinang')
    df_occasion = pd.read_excel('datasupport2.xlsx', sheet_name='specialdays2')
    df_kurs = pd.read_excel('datasupport2.xlsx', sheet_name='kurs2')
    df_kurs = df_kurs.sort_values(by='Tanggal')
    df_kurs = df_kurs[['Kurs Jual', 'Kurs Beli', 'Tanggal']]
    df_price = pd.read_excel('price.xlsx')

    df_datasupport_monthly_p = mf.interpolate_df(df_datasupport_monthly)
    df_occasion_p = mf.preprocess_occasion(df_occasion)
    df_kurs = mf.preprocess_kurs(df_kurs)
    df_datasupport_pibc = mf.preprocess_pibc(df_datasupport_pibc)


    data_frames = [df_datasupport_monthly_p, df_occasion_p, df_datasupport_pibc, df_kurs, df_price]
    original_df = reduce(lambda left, right: pd.merge(left, right, on=['Tanggal'],how='outer'), data_frames)
    original_df.dropna(inplace=True)
    original_df = original_df.drop_duplicates(subset=['Tanggal'], keep='first')
    num_col_list = ['BerasPremium', 'BerasMedium','ProduksiBeras','StokCipinang','Kurs']
    original_df = mf.to_integer(original_df,num_col_list)

    original_df = original_df.tail(15)
    
    with st.form("input_data_form"):
        latest_date = original_df['Tanggal'].max() + timedelta(days=1)
        st.write(latest_date)

        BerasPremium = st.text_input('Insert a number', key = 'BerasPremium')
        BerasMedium = st.text_input('Insert a number', key = 'BerasMedium')
        ProduksiBeras = st.text_input('Insert a number', key = 'ProduksiBeras')
        StokCipinang = st.text_input('Insert a number', key = 'StokCipinang')
        Kurs = st.text_input('Insert a number', key = 'Kurs')
        submit = st.form_submit_button("Submit")
        if submit:
            new_row = {'Tanggal': latest_date,
                        'ProduksiBeras': ProduksiBeras,
                        'occasion': '-',
                        'StokCipinang': StokCipinang,
                        'Kurs': Kurs,
                        'BerasPremium': BerasPremium,
                        'BerasMedium': BerasMedium}
            original_df = original_df.append(new_row, ignore_index=True)
        st.data_editor(original_df, hide_index=True)


else:
    st.title('Silahkan Login dahulu❕')





