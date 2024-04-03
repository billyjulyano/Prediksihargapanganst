import streamlit as st

# css file
with open('style.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.sidebar.header('Dashboard Prediksi Harga Pangan')
st.sidebar.image('logogabungan.png')

if 'creds' not in st.session_state:
    st.session_state['creds'] = False

if st.session_state['creds']:
    st.title('👋🏻 Silahkan Input Harga')

else:
    st.title('Silahkan Login dahulu❕')


