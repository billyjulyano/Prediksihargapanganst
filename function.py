from pytorch_forecasting import TemporalFusionTransformer
import streamlit as st
import pandas as pd

@st.cache_resource()
def model_import(model_name):
    model = TemporalFusionTransformer.load_from_checkpoint(model_name, map_location='cpu')
    return model

@st.cache_data()
def excel_import(excel_name):
    dataframe = pd.read_excel(excel_name)
    dataframe['Tanggal'] = pd.to_datetime(dataframe['Tanggal'])
    return dataframe