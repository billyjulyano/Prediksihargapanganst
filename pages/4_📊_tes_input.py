from common import *

st.write('# Solution using a dataframe')

# Create an empty dataframe on first page load, will skip on page reloads
if 'data' not in st.session_state:
    data = pd.DataFrame({'Tanggal': [],
                        'ProduksiBeras': [],
                        'occasion': [],
                        'StokCipinang': [],
                        'Kurs': [],
                        'BerasPremium': [],
                        'BerasMedium': []})
    st.session_state.data = data

# Show current data
st.dataframe(st.session_state.data)

st.write('#### Using form submission')

# Function to append inputs from form into dataframe
def add_dfForm():
    row = pd.DataFrame({'Tanggal':[st.session_state.input_df_form_date],
                        'ProduksiBeras':[st.session_state.input_df_form_ProduksiBeras],
                        'occasion':[st.session_state.input_df_form_occasion],
                        'StokCipinang':[st.session_state.input_df_form_StokCipinang],
                        'Kurs':[st.session_state.input_df_form_kurs],
                        'BerasPremium': [st.session_state.input_df_form_BP],
                        'BerasMedium':[st.session_state.input_df_form_BM]})
    st.session_state.data = pd.concat([st.session_state.data, row])

# Inputs listed within a form
# dfForm = st.form(key='dfForm', clear_on_submit=True)
# with dfForm:
#     dfFormColumns = st.columns(6)
#     with dfFormColumns[0]:
#         st.date_input('tanggal', key='input_df_form_date')
#         date_input = st.session_state.input_df_form_date
#         date_input = pd.to_datetime(date_input)
#     with dfFormColumns[1]:
#         st.number_input('Produksi Beras (ton)', step=1, key='input_df_form_ProduksiBeras')
#         ProduksiBeras = st.session_state.input_df_form_ProduksiBeras
#     with dfFormColumns[2]:
#         st.number_input('Stok Cipinang (ton)', step=1, key='input_df_form_StokCipinang')
#         StokCipinang = st.session_state.input_df_form_StokCipinang
#     with dfFormColumns[3]:
#         st.number_input('Kurs', step=1, key='input_df_form_kurs')
#         kurs_input = st.session_state.input_df_form_kurs
#     with dfFormColumns[4]:
#         st.number_input('Beras Premium', step=1, key='input_df_form_BP')
#         BP_input = st.session_state.input_df_form_BP
#     with dfFormColumns[5]:
#         st.number_input('Beras Medium', step=1, key='input_df_form_BM')
#         BM_input = st.session_state.input_df_form_BM
#     st.session_state.input_df_form_occasion = '-'
#     occasion_input = st.session_state.input_df_form_occasion
#     st.form_submit_button(on_click=add_dfForm)

dfForm = st.form(key='dfForm', clear_on_submit=True)
with dfForm:
    dfFormColumns = st.columns(6)
    with dfFormColumns[0]:
        date_input = st.date_input('tanggal', key='input_df_form_datex')
        date_input = pd.to_datetime(date_input)
        st.session_state.input_df_form_date = date_input
    with dfFormColumns[1]:
        ProduksiBeras = st.number_input('Produksi Beras (ton)', step=1, key='input_df_form_ProduxksiBeras')
        st.session_state.input_df_form_ProduksiBeras = ProduksiBeras
    with dfFormColumns[2]:
        StokCipinang = st.number_input('Stok Cipinang (ton)', step=1, key='input_df_form_StokCxipinang')
        st.session_state.input_df_form_StokCipinang = StokCipinang
    with dfFormColumns[3]:
        kurs_input = st.number_input('Kurs', step=1, key='input_df_xform_kurs')
        st.session_state.input_df_form_kurs = kurs_input
    with dfFormColumns[4]:
        BP_input = st.number_input('Beras Premium', step=1, key='input_xdf_form_BP')
        st.session_state.input_df_form_BP = BP_input
    with dfFormColumns[5]:
        BM_input = st.number_input('Beras Medium', step=1, key='input_dfx_form_BM')
        st.session_state.input_df_form_BM = BM_input
    st.session_state.input_df_form_occasion = '-'
    st.form_submit_button(on_click=add_dfForm)