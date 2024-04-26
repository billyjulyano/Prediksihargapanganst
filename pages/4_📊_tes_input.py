from common import *

st.write('# Add new data')

# Create an empty dataframe on first page load, will skip on page reloads
if 'updated_data' not in st.session_state:
    updated_data = pd.DataFrame({'Tanggal': [],
                        'ProduksiBeras': [],
                        'occasion': [],
                        'StokCipinang': [],
                        'Kurs': [],
                        'BerasPremium': [],
                        'BerasMedium': []})
    st.session_state.updated_data = updated_data

# Show current data
st.dataframe(st.session_state.updated_data, use_container_width = True)

st.write('#### Use form below:')

# Function to append inputs from form into dataframe
def add_dfForm():
    st.session_state.input_df_form_occasion = '-'
    date_input = st.session_state.input_df_form_date
    date_input = pd.to_datetime(date_input)
    row = pd.DataFrame({'Tanggal':[date_input],
                        'ProduksiBeras':[st.session_state.input_df_form_ProduksiBeras],
                        'occasion':[st.session_state.input_df_form_occasion],
                        'StokCipinang':[st.session_state.input_df_form_StokCipinang],
                        'Kurs':[st.session_state.input_df_form_kurs],
                        'BerasPremium': [st.session_state.input_df_form_BP],
                        'BerasMedium':[st.session_state.input_df_form_BM]})
    st.session_state.updated_data = pd.concat([st.session_state.updated_data, row])

# Inputs listed within a form
dfForm = st.form(key='dfForm', clear_on_submit=False)
with dfForm:
    dfFormColumns = st.columns(6)
    with dfFormColumns[0]:
        st.date_input('tanggal', key='input_df_form_date')
    with dfFormColumns[1]:
        st.number_input('Produksi Beras', step=13401, key='input_df_form_ProduksiBeras', value = 1200327)
    with dfFormColumns[2]:
        st.number_input('Stok Cipinang', step=897, key='input_df_form_StokCipinang', value = 31030)
    with dfFormColumns[3]:
        st.number_input('Kurs', step=457, key='input_df_form_kurs', value = 12300)
    with dfFormColumns[4]:
        st.number_input('Beras Premium', step=343, key='input_df_form_BP', value = 16991)
    with dfFormColumns[5]:
        st.number_input('Beras Medium', step=242, key='input_df_form_BM', value = 13661)
    st.form_submit_button(on_click=add_dfForm)