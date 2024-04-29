from common import *

st.set_page_config(page_title='Prediksi Harga Pangan', layout='wide', initial_sidebar_state='auto',page_icon="🌾")

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

data = mf.create_time_features_ver2(df_merged)

#headersidebar
st.sidebar.header('Dashboard Prediksi Harga Pangan') 

#himagesidebar
st.sidebar.image('logogabungan.png')

# css file
with open('style.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

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
        encoder, extended_df = mf.create_outofsample_base_ver2(data, df_merged, tanggal_awal_prediksi, max_encoder_length, max_prediction_length)
        extended_df_time = mf.create_time_features_ver2(extended_df)
        decoder = mf.create_decoder(extended_df_time, max_prediction_length)

        new_prediction_data = pd.concat([encoder, decoder], ignore_index=True)
        raw_result = mf.do_pred(model, new_prediction_data)

        pred_date_index = decoder[decoder['jenis'] == pilihan_komoditas_prediksi]['Tanggal']
        df_prediction = mf.filter_prediction(raw_result, output_dict, pilihan_komoditas_prediksi, pred_date_index)
        
        tab_pred1, tab_pred2 = st.tabs(['Graph', ' Table'])
        with tab_pred1:
            st.data_editor(
            df_prediction,
            use_container_width=False,
            disabled = True,
            column_config={
                "Tanggal": st.column_config.DatetimeColumn(
                format="D MMMM YYYY",
                ),
                'Harga Prediksi': st.column_config.NumberColumn(
                    format = '%d'
                )
            })

        alt_predchart = mf.create_chart_pred(df_prediction)
        with tab_pred2:
            st.markdown('#### Grafik')
            st.altair_chart((alt_predchart).interactive(), use_container_width=True)

        st.markdown('##### Matriks')
        filtered_data = data[data['jenis'] == pilihan_komoditas_prediksi]
        mean_last_30 = round(filtered_data.tail(30)['harga'].mean())
        mean_pred = round(df_prediction['Harga Prediksi'].mean())
        
        percentage_difference = (round(((mean_pred - mean_last_30) / mean_last_30) * 100,1))
        st.metric('Rata-rata harga prediksi', locale.currency(mean_pred, grouping=True)[:-3], f'{percentage_difference}%')

with tab2:
    if 'updated_data' not in st.session_state:
        st.write('update data first in update page')
    else:
        updated_df = st.session_state.updated_data
        updated_df = mf.create_time_features_ver2(updated_df)
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
            encoder, extended_df = mf.create_outofsample_base_ver2(updated_df, df_merged, tanggal_awal_prediksi, max_encoder_length, max_prediction_length)
            extended_df_time = mf.create_time_features_ver2(extended_df)
            decoder = mf.create_decoder(extended_df_time, max_prediction_length)

            new_prediction_data = pd.concat([encoder, decoder], ignore_index=True)
            
            raw_result = mf.do_pred(model, new_prediction_data)
            pred_date_index = decoder[decoder['jenis'] == pilihan_komoditas_prediksi]['Tanggal']
            df_prediction = mf.filter_prediction(raw_result, output_dict, pilihan_komoditas_prediksi, pred_date_index)

            alt_predchart = mf.create_chart_pred(df_prediction)

            tab_pred1, tab_pred2 = st.tabs(['Graph', ' Table'])
            with tab_pred1:
                st.data_editor(
                df_prediction,
                use_container_width=False,
                disabled = True,
                column_config={
                    "Tanggal": st.column_config.DatetimeColumn(
                    format="D MMMM YYYY",
                    ),
                    'Harga Prediksi': st.column_config.NumberColumn(
                        format = '%d'
                    )
                })

            alt_predchart = mf.create_chart_pred(df_prediction)
            with tab_pred2:
                st.markdown('#### Grafik')
                st.altair_chart((alt_predchart).interactive(), use_container_width=True)

            st.markdown('##### Matriks')
            filtered_data = updated_df[updated_df['jenis'] == pilihan_komoditas_prediksi]
            mean_last_30 = round(filtered_data.tail(30)['harga'].mean())
            mean_pred = round(df_prediction['Harga Prediksi'].mean())
            
            percentage_difference = (round(((mean_pred - mean_last_30) / mean_last_30) * 100,1))
            st.metric('Rata-rata harga prediksi', locale.currency(mean_pred, grouping=True)[:-3], f'{percentage_difference}%')
