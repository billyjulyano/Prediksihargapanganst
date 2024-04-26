import streamlit as st
import pandas as pd

st.write('# Solution using a dataframe')

# Create an empty dataframe on first page load, will skip on page reloads
if 'data' not in st.session_state:
    data = pd.DataFrame({'tanggal':[],'income':[],'expense':[],'net':[]})
    st.session_state.data = data

# Show current data
st.dataframe(st.session_state.data, use_container_width = True)

st.write('#### Using form submission')

# Function to append inputs from form into dataframe
def add_dfForm():
    row = pd.DataFrame({'tanggal':[st.session_state.input_df_form_name],
            'income':[st.session_state.input_df_form_income],
            'expense':[st.session_state.input_df_form_expense],
            'net':[st.session_state.input_df_form_income-st.session_state.input_df_form_expense]})
    st.session_state.data = pd.concat([st.session_state.data, row])

# Inputs listed within a form
dfForm = st.form(key='dfForm', clear_on_submit=True)
with dfForm:
    dfFormColumns = st.columns(4)
    with dfFormColumns[0]:
        st.date_input('name')
    with dfFormColumns[1]:
        st.number_input('income', step=4, key='input_df_form_income')
    with dfFormColumns[2]:
        st.number_input('expense', step=19, key='input_df_form_expense')
    with dfFormColumns[3]:
        pass
    st.form_submit_button(on_click=add_dfForm)

st.write('#### Not using form submission')

# Function to append non-form inputs into dataframe
def add_df():
    row = pd.DataFrame({'tanggal':[st.session_state.input_df_name],
            'income':[st.session_state.input_df_income],
            'expense':[st.session_state.input_df_expense],
            'net':[st.session_state.input_df_income-st.session_state.input_df_expense]})
    st.session_state.data = pd.concat([st.session_state.data, row])