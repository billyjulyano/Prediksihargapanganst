import streamlit as st

def login(username, password):
    if username == 'admin' and password == 'abc123':
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
        else:
            st.error('Invalid username or password')

if __name__ == '__main__':
    main()