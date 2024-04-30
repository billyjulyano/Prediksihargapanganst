from common import *

st.set_page_config(page_title='Prediksi Harga Pangan', layout='wide', initial_sidebar_state='auto',page_icon="👋")

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

st.title('Visualisasi Data Harga')   

with st.form("price_history_form"):
    st.subheader('Pilih Parameter', divider='green', anchor = '1') 
    pilihan_komoditas = st.selectbox(
        "Tipe Komunitas",
        ("BerasPremium", "BerasMedium",),
        placeholder="Pilih",
        )
    tanggal_awal = data['Tanggal'].min()
    tanggal_akhir = data['Tanggal'].max()
    
    ds = st.date_input("Tanggal Awal Historis", min_value=tanggal_awal, max_value= tanggal_akhir, value = tanggal_akhir - datetime.timedelta(days=90))
    ds = pd.to_datetime(ds)
    de = st.date_input("Tanggal Akhir Historis", min_value=tanggal_awal, max_value=tanggal_akhir, value = tanggal_akhir)
    de = pd.to_datetime(de)
    st.form_submit_button("Submit")

price_history = data[(data['jenis'] == pilihan_komoditas) & (data['Tanggal'] >= ds) & (data['Tanggal'] <= de)]

alt_historychart = mf.create_chart_price_historical(price_history)
st.markdown('#### Grafik')
st.altair_chart((alt_historychart).interactive(), use_container_width=True)

st.title('Visualisasi Data Support')   
with st.form("stok"):
    st.subheader('Pilih Parameter', divider='green', anchor = '1') 
    pilihanstok = st.selectbox(
        "Pilih Stok",
        ("StokCipinang", "Kurs", 'ProduksiBeras'),
        placeholder="Pilih",
        )

    tanggal_awal = data['Tanggal'].min()
    tanggal_akhir =data['Tanggal'].max()
    ds = st.date_input("Tanggal Awal Historis",min_value=tanggal_awal, max_value= tanggal_akhir ,value = tanggal_akhir - datetime.timedelta(days=180))
    ds = pd.to_datetime(ds)
    de = st.date_input("Tanggal Akhir Historis",min_value=tanggal_awal, max_value=tanggal_akhir, value = tanggal_akhir)
    de = pd.to_datetime(de)
    st.form_submit_button("Submit")

df_stok = data[(data['jenis'] == pilihan_komoditas) & (data['Tanggal'] >= ds) & (data['Tanggal'] <= de)]

alt_datastok = mf.create_chart_stok(df_stok, pilihanstok)
st.markdown('#### Grafik')
st.altair_chart((alt_datastok).interactive(), use_container_width=True)
