from common import *

#isi atas 
st.set_page_config(page_title='Prediksi Harga Pangan', layout='wide', initial_sidebar_state='auto',page_icon="👋")

# css file
with open('style.css') as f: #buka file style.css disimpan di variable f
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True) 

pages_col = st.columns(4) 
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

username = 'a'
password = '1'
state = False

st.title('Login Page')

if 'creds' not in st.session_state:
    st.session_state['creds'] = False

with st.form("login_form"):
    st.write('Enter login credentials:')
    username_input = st.text_input('Username')
    password_input = st.text_input('Password', type='password')

    submitted_login = st.form_submit_button("Login") 
    if submitted_login:
        if username_input == username and password_input == password:
            st.success('Login successful!')
            sleep(0.5) #membuat program tidak melakukan apa apa, selama 5 detik, delay intinya
            st.session_state['creds'] = True
            st.switch_page('pages/3_📊_Input_Harga.py')
        else:
            st.error('Invalid username or password')

