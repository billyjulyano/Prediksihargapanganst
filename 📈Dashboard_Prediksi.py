from common import *

st.set_page_config(page_title='Prediksi Harga Pangan', layout='wide', initial_sidebar_state='auto',page_icon="🌾")

# css file
with open('style.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

pages_col = st.columns(4, gap='medium')
pages_col[0].page_link("📈Dashboard_Prediksi.py", label="📈Dashboard Prediksi")
pages_col[1].page_link("pages/1_🌍_Visualisasi Data.py", label="🌍 Visualisasi Data")
pages_col[2].page_link("pages/2_🔐_Login.py", label="🔐 Login")
pages_col[3].page_link("pages/3_📊_Input_Harga.py", label="📊 Input Harga")

st.sidebar.header('Dashboard Prediksi Harga Pangan')
st.sidebar.image('logogabungan.png')

st.sidebar.write('')
st.sidebar.page_link("📈Dashboard_Prediksi.py", label="📈Dashboard Prediksi")
st.sidebar.page_link("pages/1_🌍_Visualisasi Data.py", label="🌍 Visualisasi Data")
st.sidebar.page_link("pages/2_🔐_Login.py", label="🔐 Login")
st.sidebar.page_link("pages/3_📊_Input_Harga.py", label="📊 Input Harga")

model = mf.model_import('samplemodel_ver2.ckpt') 
output_dict = model._hparams.embedding_labels['jenis']

# import all data
df_datasupport_monthly = pd.read_excel('datasupport2.xlsx')
df_datasupport_monthly = df_datasupport_monthly[['Tanggal','Tahun', 'Bulan', 'ProduksiBeras']]
df_datasupport_pibc = pd.read_excel('datasupport2.xlsx', sheet_name='DailyCipinang')
df_occasion = pd.read_excel('datasupport2.xlsx', sheet_name='specialdays2')
df_kurs = pd.read_excel('datasupport.xlsx', sheet_name='kurs2')
df_kurs = df_kurs.sort_values(by='Tanggal')
df_kurs = df_kurs[['Kurs Jual', 'Kurs Beli', 'Tanggal']]
df_price = pd.read_excel('price.xlsx')

# interpolate and preprocess
df_datasupport_monthly_p = mf.interpolate_df(df_datasupport_monthly)
df_occasion_p = mf.preprocess_occasion(df_occasion)
df_kurs = mf.preprocess_kurs(df_kurs)
df_datasupport_pibc = mf.preprocess_pibc(df_datasupport_pibc)

# merge all data
data_frames = [df_datasupport_monthly_p, df_occasion_p, df_datasupport_pibc, df_kurs, df_price]
df_merged = reduce(lambda left, right: pd.merge(left, right, on=['Tanggal'],how='outer'), data_frames)
df_merged.dropna(inplace=True)
df_merged = df_merged.drop_duplicates(subset=['Tanggal'], keep='first')

data = mf.create_time_features(df_merged)

max_prediction_length = 30
max_encoder_length = 90

tab1, tab2 = st.tabs(['Original Data', 'Updated Data'])

with tab1:
    with st.form("prediksi"):
        st.subheader('Set Parameter', divider='blue', anchor = '3')
        latest_data = data['Tanggal'].max()
        pilihan_komoditas_prediksi = st.selectbox(
            "Pilih Jenis Pangan",
            ("BerasPremium", "BerasMedium",),
            placeholder="Pilih",
            )
        tanggal_awal_prediksi = st.date_input("Tanggal Awal prediksi", value = latest_data + datetime.timedelta(days=1))
        prediction_button = st.form_submit_button("Run prediction")

    if prediction_button:
        encoder, extended_df = mf.create_outofsample_base(data, df_merged, tanggal_awal_prediksi, max_encoder_length, max_prediction_length)
        extended_df_time = mf.create_time_features(extended_df)
        decoder = mf.create_decoder(extended_df_time, max_prediction_length)

        new_prediction_data = pd.concat([encoder, decoder], ignore_index=True)
        raw_result = mf.do_pred(model, new_prediction_data)

        pred_date_index = decoder[decoder['jenis'] == pilihan_komoditas_prediksi]['Tanggal']
        df_prediction = mf.filter_prediction(raw_result, output_dict, pilihan_komoditas_prediksi, pred_date_index)
        
        tab_pred1, tab_pred2 = st.tabs(['Graph', ' Table'])
        with tab_pred1:
            alt_predchart = mf.create_chart_pred(df_prediction)
            st.altair_chart((alt_predchart).interactive(), use_container_width=True)
        with tab_pred2:
            mf.create_table_pred(df_prediction)

        st.markdown('##### Matriks')
        percentage_difference, mean_pred = mf.create_metrics1(data, pilihan_komoditas_prediksi, df_prediction)
        st.metric('Rata-rata harga prediksi', locale.currency(mean_pred, grouping=True)[:-3], f'{percentage_difference}%')

with tab2:
    if 'updated_data' not in st.session_state:
        st.write('update data first in update page')
    else:
        updated_df = st.session_state.updated_data
        updated_df = mf.create_time_features(updated_df)
        st.write(updated_df.tail(3))

        with st.form("prediksi data baru"):
            st.subheader('Set Parameter', divider='blue', anchor = '3')
            latest_data = updated_df['Tanggal'].max()
            pilihan_komoditas_prediksi = st.selectbox(
                "Pilih Jenis Pangan",
                ("BerasPremium", "BerasMedium",),
                placeholder="Pilih",
                )
            tanggal_awal_prediksi = st.date_input("Tanggal Awal prediksi", value = latest_data + datetime.timedelta(days=1))
            prediction_button = st.form_submit_button("Run prediction")

        if prediction_button:
            encoder, extended_df = mf.create_outofsample_base(updated_df, df_merged, tanggal_awal_prediksi, max_encoder_length, max_prediction_length)
            extended_df_time = mf.create_time_features(extended_df)
            decoder = mf.create_decoder(extended_df_time, max_prediction_length)

            new_prediction_data = pd.concat([encoder, decoder], ignore_index=True)
            
            raw_result = mf.do_pred(model, new_prediction_data)
            pred_date_index = decoder[decoder['jenis'] == pilihan_komoditas_prediksi]['Tanggal']
            df_prediction = mf.filter_prediction(raw_result, output_dict, pilihan_komoditas_prediksi, pred_date_index)

            alt_predchart = mf.create_chart_pred(df_prediction)

            tab_pred1, tab_pred2 = st.tabs(['Graph', ' Table'])
            with tab_pred1:
                alt_predchart = mf.create_chart_pred(df_prediction)
                st.altair_chart((alt_predchart).interactive(), use_container_width=True)
            with tab_pred2:
                mf.create_table_pred(df_prediction)
                
            st.markdown('##### Matriks')
            percentage_difference, mean_pred = mf.create_metrics1(data, pilihan_komoditas_prediksi, df_prediction)
            st.metric('Rata-rata harga prediksi', locale.currency(mean_pred, grouping=True)[:-3], f'{percentage_difference}%')
