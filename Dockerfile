FROM python:3.9.0-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "📈Dashboard_Prediksi.py"]