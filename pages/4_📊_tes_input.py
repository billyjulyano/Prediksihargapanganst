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
    original_df = df_merged

    num_col_list = ['BerasPremium', 'BerasMedium','ProduksiBeras','StokCipinang','Kurs']
    original_df = mf.to_integer(original_df,num_col_list)

    original_df = original_df.tail(5)
    updated_df = original_df

    input_data =  st.form("input_data_form")
    latest_date = original_df['Tanggal'].max() + timedelta(days=1)
    input_data.write(latest_date)

    BerasPremium = input_data.number_input('Insert a number', key = 'BerasPremium', value = 5)
    BerasMedium = input_data.number_input('Insert a number', key = 'BerasMedium', value = 5)
    ProduksiBeras = input_data.number_input('Insert a number', key = 'ProduksiBeras', value = 3)
    StokCipinang = input_data.number_input('Insert a number', key = 'StokCipinang', value = 1)
    Kurs = input_data.number_input('Insert a number', key = 'Kurs', value = 2)
    submit = input_data.form_submit_button("Submit")
    if submit:
        new_row = {'Tanggal': latest_date,
                    'ProduksiBeras': ProduksiBeras,
                    'occasion': '-',
                    'StokCipinang': StokCipinang,
                    'Kurs': Kurs,
                    'BerasPremium': BerasPremium,
                    'BerasMedium': BerasMedium}
        updated_df = updated_df.append(new_row, ignore_index=True)
try:
    st.data_editor(updated_df, hide_index=True)
except:
    st.subheader('tambahkan data terlebih dahulu lalu klik submit')


else:
    st.title('Silahkan Login dahulu❕')





