from pytorch_forecasting import TemporalFusionTransformer
import streamlit as st
import pandas as pd
import altair as alt

@st.cache_resource()
def model_import(model_name):
    model = TemporalFusionTransformer.load_from_checkpoint(model_name, map_location='cpu')
    return model

@st.cache_data()
def excel_import(excel_name):
    dataframe = pd.read_excel(excel_name)
    dataframe['Tanggal'] = pd.to_datetime(dataframe['Tanggal'])
    return dataframe

def interpolate_df(df):
    temp_df  = df.copy()
    temp_df.drop(columns=['Tahun','Bulan'],inplace=True)
    temp_df['Tanggal'] = pd.to_datetime(temp_df['Tanggal'])
    temp_df.set_index('Tanggal', inplace=True)
    temp_df = temp_df.resample('D').interpolate(method='polynomial', order=2)
    temp_df.reset_index(inplace=True)
    df = temp_df
    return df

def preprocess_occasion(df):
    full_date_range = pd.date_range(start=df['Tanggal'].min(), end=df['Tanggal'].max(), freq='D')
    full_date_df = pd.DataFrame({'Tanggal': full_date_range})
    temp_df = pd.merge(full_date_df, df, on='Tanggal', how='left')
    temp_df['occasion'] = temp_df['occasion'].fillna('-')
    df = temp_df
    return df


# Time based features
def create_time_features(df):
    time_df = pd.melt(
        df,
        id_vars=['Tanggal','StokCBP', 'LuasPanen', 'ProduksiPadi', 'ProduksiBeras', 'occasion'],
        var_name=["jenis"],
        value_name="harga",
    )
    time_df = time_df.sort_values(by=['jenis', 'Tanggal'])
    time_df['days_from_start'] = time_df.groupby('jenis').cumcount() + 1
    time_df['weeks_from_start'] = (time_df['days_from_start'] - 1) // 7 + 1
    time_df['months_from_start'] = (time_df['days_from_start'] - 1) // 30 + 1

    time_df['Tanggal'] = pd.to_datetime(time_df['Tanggal'])
    time_df.set_index('Tanggal', inplace=True)

    date = time_df.index
    time_df['Dates'] = date.day
    time_df['WeekDay'] = date.dayofweek
    time_df['Month'] = date.month
    time_df['Year'] = date.year
    time_df = time_df.reset_index(drop=False)

    month_mapping = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    day_mapping = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}

    time_df['Month_Str'] = time_df['Month'].map(month_mapping)
    time_df['Day_Str'] = time_df['WeekDay'].map(day_mapping)
    return time_df

def create_chart_price_historical(df):
    lowest = df['harga'].min()
    highest = df['harga'].max()
    hover = alt.selection_point(
        fields=["Tanggal"],
        nearest=True,
        on="mouseover",
        empty=False,
    )
    lines = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x="Tanggal",
            y = alt.Y('harga', scale=alt.Scale(domain=[lowest-10, highest+30])),
            )       
        )
    points = lines.transform_filter(hover).mark_circle(size=100)
    tooltips = (
        alt.Chart(df)
        .mark_rule()
        .encode(
            x="Tanggal",
            y="harga",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Tanggal", title="Date"),
                alt.Tooltip("harga", title="Price (IDR)"),
            ],
        )
        .add_params(hover)
    )
    return (lines + points + tooltips).interactive()

def create_chart_stok(df, jenis_datasupport):
    lowest = df[jenis_datasupport].min()
    highest = df[jenis_datasupport].max()
    hover = alt.selection_point(
        fields=["Tanggal"],
        nearest=True,
        on="mouseover",
        empty=False,
    )
    lines = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x="Tanggal",
            y = alt.Y(jenis_datasupport, scale=alt.Scale(domain=[lowest-10, highest+30])),
            )       
        )
    points = lines.transform_filter(hover).mark_circle(size=100)
    tooltips = (
        alt.Chart(df)
        .mark_rule()
        .encode(
            x="Tanggal",
            y=jenis_datasupport,
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Tanggal", title="Date"),
                alt.Tooltip(jenis_datasupport, title="Stok"),
            ],
        )
        .add_params(hover)
    )
    return (lines + points + tooltips).interactive()


def create_outofsample_base(final_df, merged_df, start_date, max_encoder_length, max_prediction_length):
    encoder_data = final_df[lambda x:x.days_from_start > x.days_from_start.max() - max_encoder_length]
    end_date = pd.to_datetime(start_date) + pd.DateOffset(days=max_prediction_length)
    date_range = pd.date_range(start=merged_df['Tanggal'].iloc[-1], end=end_date)
    extended_df = pd.DataFrame(date_range, columns=['Tanggal'])
    extended_df = pd.concat([merged_df, extended_df], ignore_index=True)
    
    return encoder_data, extended_df


def create_decoder(df, max_prediction_length):
    decoder_data = df.groupby('jenis').tail(max_prediction_length)
    decoder_data['occasion'] = '-'
    decoder_data.fillna(0, inplace=True)

    return decoder_data