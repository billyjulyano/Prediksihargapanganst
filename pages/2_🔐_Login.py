import streamlit as st
from time import sleep

# css file
with open('style.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.sidebar.header('Dashboard Prediksi Harga Pangan')
st.sidebar.image('logogabungan.png')

username = 'a'
password = '1'
state = False

st.title('Please login')

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
            sleep(0.5)
            st.session_state['creds'] = True
            st.switch_page('pages/3_📊_Input_Harga.py')
        else:
            st.error('Invalid username or password')

