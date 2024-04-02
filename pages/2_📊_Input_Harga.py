import streamlit as st

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {

  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center center;
  background-repeat: repeat;
  background-image: url("data:image/svg+xml;utf8,%3Csvg viewBox=%220 0 500 500%22 xmlns=%22http:%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cdefs%3E%3ClinearGradient id=%22b%22 gradientTransform=%22rotate(-45 .5 .5)%22%3E%3Cstop offset=%220%25%22 stop-color=%22%2308AEEA%22%2F%3E%3Cstop offset=%22100%25%22 stop-color=%22%232AF598%22%2F%3E%3C%2FlinearGradient%3E%3CclipPath id=%22a%22%3E%3Cpath fill=%22currentColor%22 d=%22M668.5 733Q500 966 289 733t0-464.5q211-231.5 379.5 0t0 464.5Z%22%2F%3E%3C%2FclipPath%3E%3C%2Fdefs%3E%3Cg clip-path=%22url(%23a)%22%3E%3Cpath fill=%22url(%23b)%22 d=%22M668.5 733Q500 966 289 733t0-464.5q211-231.5 379.5 0t0 464.5Z%22%2F%3E%3C%2Fg%3E%3C%2Fsvg%3E");


}
[data-testid="stSidebarContent"] {

  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center center;
  background-repeat: repeat;
  background-image: url("data:image/svg+xml;utf8,%3Csvg viewBox=%220 0 500 500%22 xmlns=%22http:%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cdefs%3E%3ClinearGradient id=%22b%22 gradientTransform=%22rotate(-45 .5 .5)%22%3E%3Cstop offset=%220%25%22 stop-color=%22%2308AEEA%22%2F%3E%3Cstop offset=%22100%25%22 stop-color=%22%232AF598%22%2F%3E%3C%2FlinearGradient%3E%3CclipPath id=%22a%22%3E%3Cpath fill=%22currentColor%22 d=%22M668.5 733Q500 966 289 733t0-464.5q211-231.5 379.5 0t0 464.5Z%22%2F%3E%3C%2FclipPath%3E%3C%2Fdefs%3E%3Cg clip-path=%22url(%23a)%22%3E%3Cpath fill=%22url(%23b)%22 d=%22M668.5 733Q500 966 289 733t0-464.5q211-231.5 379.5 0t0 464.5Z%22%2F%3E%3C%2Fg%3E%3C%2Fsvg%3E");


}
</style>
"""

st.markdown(page_bg_img,unsafe_allow_html=True)

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

