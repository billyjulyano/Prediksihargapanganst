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

def preprocess_kurs(df):
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    start_date = df['Tanggal'].min()
    end_date = df['Tanggal'].max()
    all_dates = pd.date_range(start=start_date, end=end_date)

    df = df.set_index('Tanggal').reindex(all_dates).reset_index()

    df['Kurs Jual'] = df['Kurs Jual'].interpolate(method='polynomial', order=2)
    df['Kurs Beli'] = df['Kurs Beli'].interpolate(method='polynomial', order=2)
    df = df.rename(columns={'index': 'Tanggal'})
    df = df.rename(columns={'Kurs Beli': 'Kurs'})
    df = df.drop(columns=['Kurs Jual'])
    return df

def preprocess_pibc(df):
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    df = df.drop(columns=['Pemasukan','Pengeluaran','Stok Akhir'])
    df = df.rename(columns={'Stok Awal': 'StokCipinang'})
    return df

def to_integer(df, col_list):
    for col in col_list:
        df[col_list] = df[col_list].astype(int)
    return df

def create_time_features(df):
    time_df = pd.melt(
    df,
    id_vars=['Tanggal', 'Kurs', 'StokCipinang', 'ProduksiBeras', 'occasion'],
    var_name=["jenis"],
    value_name="harga",
    )
    # day of year
    time_df['day_of_year'] = time_df['Tanggal'].dt.dayofyear

    # day index
    time_df['Tanggal'] = pd.to_datetime(time_df['Tanggal'])
    time_df = time_df.sort_values(by=['jenis', 'Tanggal'])
    start_Tanggal = time_df.groupby('jenis')['Tanggal'].transform('min')
    time_df['days_count'] = (time_df['Tanggal'] - start_Tanggal).dt.days
    time_df['days_count'] += 1
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
    encoder_data = final_df[lambda x:x.days_count > x.days_count.max() - max_encoder_length]
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

@st.cache_data()
def do_pred(_model, prediction_data):
    new_raw_predictions = _model.predict(prediction_data, mode="raw", return_x=True, trainer_kwargs={'logger': False})
    raw_result = new_raw_predictions.output.prediction.cpu().numpy()[:,:, 3]
    return raw_result


def filter_prediction(raw_prediction, output_dict, data_type, pred_date_index):
    filtered = raw_prediction[output_dict[data_type]]
    df_pred = pd.DataFrame({'Tanggal': pred_date_index, 'Harga Prediksi': filtered})
    return df_pred

def create_chart_pred(df):
    lowest = df['Harga Prediksi'].min()
    highest = df['Harga Prediksi'].max()
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
            y = alt.Y('Harga Prediksi', scale=alt.Scale(domain=[lowest-10, highest+30])),
            )       
        )
    points = lines.transform_filter(hover).mark_circle(size=100)
    tooltips = (
        alt.Chart(df)
        .mark_rule()
        .encode(
            x="Tanggal",
            y='Harga Prediksi',
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Tanggal", title="Date"),
                alt.Tooltip('Harga Prediksi', title="Harga"),
            ],
        )
        .add_params(hover)
    )
    return (lines + points + tooltips).interactive()

def create_table_pred(df):
    st.data_editor(
        df,
        use_container_width=False,
        disabled = True,
        column_config={
            "Tanggal": st.column_config.DatetimeColumn(
                format="D MMMM YYYY",
            ),
            'Harga Prediksi': st.column_config.NumberColumn(
                format = '%d'
            )
        }
    )

def create_metrics1(data, pilihan_komoditas_prediksi, df_prediction):
    filtered_data = data[data['jenis'] == pilihan_komoditas_prediksi]
    mean_last_30 = round(filtered_data.tail(30)['harga'].mean())
    mean_pred = round(df_prediction['Harga Prediksi'].mean())
    percentage_difference = (round(((mean_pred - mean_last_30) / mean_last_30) * 100, 1))
    
    return percentage_difference, mean_pred
