import streamlit as st
loginstate = False
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

