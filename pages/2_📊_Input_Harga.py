import streamlit as st

# css file
with open('style.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.sidebar.header('Dashboard Prediksi Harga Pangan')
st.sidebar.image('logogabungan.png')

def login(username, password):
    if username == 'admin' and password == '1':
        return True
    else:
        return False

def main():
    st.title('Input Harga')

    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        if login(username, password):
            st.success('Login successful!')
            st.switch_page("your_app.py")
        else:
            st.error('Invalid username or password')

if __name__ == '__main__':
    main()

