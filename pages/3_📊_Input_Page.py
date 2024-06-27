from common import *

st.set_page_config(page_title='Price Prediction Dashboard', layout='wide', initial_sidebar_state='auto',page_icon="🌾")

# css file
with open('style.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

mf.menubar_template()

# st.session_state['creds'] = True

if 'creds' not in st.session_state:
    st.session_state['creds'] = False

if 'status' not in st.session_state:
    st.session_state['status'] = False

status = False
if st.session_state['creds']:
    st.title('📊 Data update page')
    df_datasupport_monthly = pd.read_excel('datasupport2.xlsx')
    df_datasupport_monthly = df_datasupport_monthly[['Tanggal','Tahun', 'Bulan', 'ProduksiBeras']]
    df_datasupport_pibc = pd.read_excel('datasupport2.xlsx', sheet_name='DailyCipinang')
    df_occasion = pd.read_excel('datasupport2.xlsx', sheet_name='specialdays2')
    df_kurs = pd.read_excel('datasupport.xlsx', sheet_name='kurs2')
    df_kurs = df_kurs.sort_values(by='Tanggal')
    df_kurs = df_kurs[['Kurs Jual', 'Kurs Beli', 'Tanggal']]
    df_price = pd.read_excel('price.xlsx')

    df_occasion_p = mf.preprocess_occasion(df_occasion)
    df_kurs = mf.preprocess_kurs(df_kurs)
    df_datasupport_pibc = mf.preprocess_pibc(df_datasupport_pibc)

    # DAILY
    st.subheader('Update Daily Data')
    data_frames = [df_occasion_p, df_datasupport_pibc, df_kurs, df_price]
    daily_dataframe = reduce(lambda left, right: pd.merge(left, right, on=['Tanggal'], how='outer'), data_frames)
    daily_dataframe.dropna(inplace=True)
    if 'updated_data_daily' not in st.session_state:
        st.session_state.updated_data_daily = daily_dataframe

    st.data_editor(st.session_state.updated_data_daily[-7:],
    # column_order=("Tanggal", "ProduksiBeras"),
    column_config={
            "Tanggal": st.column_config.DatetimeColumn(
            format="D MMMM YYYY"),
            'occasion': 'Hari Spesial',
            'StokCipinang': 'Stok PIBC',
            'BerasPremium': 'Beras Premium',
            'BerasMedium':'Beras Medium'
        })
    
    def delete_lastrow_daily():
        if (len(st.session_state.updated_data_daily)) > (len(daily_dataframe)):
            st.session_state.updated_data_daily = st.session_state.updated_data_daily[:-1]
        else:
            st.toast('Failed, there is no new data!')
    st.button(':red[Delete last row]', on_click=delete_lastrow_daily, key = 'del_d_key')
    
    st.write('##### Input new row data below:')

    st.session_state.input_df_form_date_latest_daily = st.session_state.updated_data_daily['Tanggal'].max() + timedelta(days=1)
    def add_dfForm_daily():
        date_input = st.session_state.input_df_form_date_latest_daily
        date_input = pd.to_datetime(date_input)
        row = pd.DataFrame({'Tanggal':[date_input],
                            'occasion':'-',
                            'StokCipinang':[st.session_state.input_df_form_StokCipinang],
                            'Kurs':[st.session_state.input_df_form_kurs],
                            'BerasPremium': [st .session_state.input_df_form_BP],
                            'BerasMedium': [st.session_state.input_df_form_BM]})
        st.session_state.updated_data_daily = pd.concat([st.session_state.updated_data_daily, row])
        st.session_state.updated_data_daily.reset_index(drop=True, inplace=True)
        st.session_state['status'] = True

    
    dfForm_daily= st.form(key='dfForm_daily', clear_on_submit=False)
    with dfForm_daily:
        dfFormColumns_daily = st.columns(4)
        with dfFormColumns_daily[0]:
            st.number_input('Stok Cipinang', step=897, key='input_df_form_StokCipinang', value = 31030)
        with dfFormColumns_daily[1]:
            st.number_input('Kurs', step=457, key='input_df_form_kurs', value = 12300)
        with dfFormColumns_daily[2]:
            st.number_input('Beras Premium', step=343, key='input_df_form_BP', value = 16991)
        with dfFormColumns_daily[3]:
            st.number_input('Beras Medium', step=242, key='input_df_form_BM', value = 13661)
        st.form_submit_button('Add data', on_click=add_dfForm_daily)

    # MONTHLY
    st.write('\n')
    st.subheader('Update Monthly Data')
    col1_mon, col2_mon = st.columns(2)
    if 'updated_data_monthly' not in st.session_state:
        st.session_state.updated_data_monthly = df_datasupport_monthly

    with col1_mon:
        st.data_editor(st.session_state.updated_data_monthly.tail(5),
        column_order=("Tanggal", "ProduksiBeras"),
        column_config={
                "Tanggal": st.column_config.DatetimeColumn(
                format="MMMM YYYY"),
                'ProduksiBeras': 'Produksi Beras',
            })
    
    def delete_lastrow_monthly():
        if (len(st.session_state.updated_data_monthly)) > (len(df_datasupport_monthly)):
            st.session_state.updated_data_monthly = st.session_state.updated_data_monthly[:-1]
        else:
            st.toast('Failed, there is no new data!')
    st.button(':red[Delete last row]', on_click=delete_lastrow_monthly, key='del_m_key')
    
    last_date_monthly = st.session_state.updated_data_monthly['Tanggal'].max()
    st.session_state.input_df_form_date_latest_monthly = (last_date_monthly + DateOffset(months=1)).replace(day=1)
    def add_dfForm_monthly():
        date_input = st.session_state.input_df_form_date_latest_monthly
        date_input = pd.to_datetime(date_input)
        row = pd.DataFrame({'Tanggal':[date_input],
                            'ProduksiBeras': [st.session_state.input_df_form_ProduksiBeras],
                           })
        st.session_state.updated_data_monthly = pd.concat([st.session_state.updated_data_monthly, row])
        st.session_state.updated_data_monthly.reset_index(drop=True, inplace=True)
        st.session_state.updated_data_monthly_p = mf.interpolate_df(st.session_state.updated_data_monthly)
        st.session_state['status'] = True

    with col2_mon:
        st.write('##### Input new row data below:')
        dfForm_monthly= st.form(key='dfForm_monthly', clear_on_submit=False)
        with dfForm_monthly:
            dfFormColumns = st.columns(1)
            with dfFormColumns[0]:
                st.number_input('Produksi Beras', step=13401, key='input_df_form_ProduksiBeras', value=1200327)
            st.form_submit_button('Add data', on_click=add_dfForm_monthly)
    
    
    
    if 'updated_data_monthly_p' not in st.session_state:
        st.session_state.updated_data_monthly_p = mf.interpolate_df(df_datasupport_monthly)

    print(st.session_state['status'])
    if st.session_state['status']:
        df_merged = reduce(lambda left, right: pd.merge(left, right, on=['Tanggal'],how='outer'), [st.session_state.updated_data_monthly_p,st.session_state.updated_data_daily])
        df_merged.dropna(inplace=True)
        df_merged = df_merged.drop_duplicates(subset=['Tanggal'], keep='first')
        original_df = df_merged
        original_df.reset_index(drop=True, inplace=True)
        st.session_state.updated_data = original_df

else:
    st.title('Silahkan Login dahulu❕')

