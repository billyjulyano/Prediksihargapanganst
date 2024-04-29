from common import *

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
    original_df = df_merged
    original_df.reset_index(drop=True, inplace=True)

    num_col_list = ['BerasPremium', 'BerasMedium','ProduksiBeras','StokCipinang','Kurs']
    original_df = mf.to_integer(original_df,num_col_list)

    st.write('delete row by use check in left of table border')
    # Create an empty dataframe on first page load, will skip on page reloads
    if 'updated_data' not in st.session_state:
        updated_data = pd.DataFrame({'Tanggal': [],
                            'ProduksiBeras': [],
                            'occasion': [],
                            'StokCipinang': [],
                            'Kurs': [],
                            'BerasPremium': [],
                            'BerasMedium': []})
        st.session_state.updated_data = original_df

    # Show current data
    st.data_editor(
        st.session_state.updated_data.tail(5),
        use_container_width=True,
        num_rows='dynamic',
        # disabled=True,
        column_config={
            "Tanggal": st.column_config.DatetimeColumn(
            format="D MMMM YYYY",
            )
        })

    st.session_state.input_df_form_date_latest = st.session_state.updated_data['Tanggal'].max() + timedelta(days=1)

    st.write('#### Use form below:')

    # Function to append inputs from form into dataframe
    def add_dfForm():
        st.session_state.input_df_form_occasion = '-'
        date_input = st.session_state.input_df_form_date_latest
        date_input = pd.to_datetime(date_input)
        row = pd.DataFrame({'Tanggal':[date_input],
                            'ProduksiBeras':[st.session_state.input_df_form_ProduksiBeras],
                            'occasion':[st.session_state.input_df_form_occasion],
                            'StokCipinang':[st.session_state.input_df_form_StokCipinang],
                            'Kurs':[st.session_state.input_df_form_kurs],
                            'BerasPremium': [st.session_state.input_df_form_BP],
                            'BerasMedium': [st.session_state.input_df_form_BM]})
        st.session_state.updated_data = pd.concat([st.session_state.updated_data, row])
        st.session_state.updated_data.reset_index(drop=True, inplace=True)

    # Inputs listed within a form
    dfForm = st.form(key='dfForm', clear_on_submit=False)
    with dfForm:
        dfFormColumns = st.columns(5)
        with dfFormColumns[0]:
            st.number_input('Produksi Beras', step=13401, key='input_df_form_ProduksiBeras', value = 1200327)
        with dfFormColumns[1]:
            st.number_input('Stok Cipinang', step=897, key='input_df_form_StokCipinang', value = 31030)
        with dfFormColumns[2]:
            st.number_input('Kurs', step=457, key='input_df_form_kurs', value = 12300)
        with dfFormColumns[3]:
            st.number_input('Beras Premium', step=343, key='input_df_form_BP', value = 16991)
        with dfFormColumns[4]:
            st.number_input('Beras Medium', step=242, key='input_df_form_BM', value = 13661)
        st.form_submit_button(on_click=add_dfForm)

else:
    st.title('Silahkan Login dahulu❕')

