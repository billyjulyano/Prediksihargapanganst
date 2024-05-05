FROM python:3.9.0-slim

WORKDIR /app

COPY . /app

# Set the locale to id_ID.UTF-8
ENV LC_ALL="id_ID.UTF-8"
ENV LC_CTYPE="id_ID.UTF-8"

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "📈Dashboard_Prediksi.py"]