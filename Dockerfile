FROM python:3.9.0-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8501

# CMD ["rm", "/usr/local/lib/python/dist-packages/pytorch-lightning/src/lightning/pytorch/core/saving.py"]
# CMD ["CP", "saving.py" "/usr/local/lib/python/dist-packages/pytorch-lightning/src/lightning/pytorch/core/"]
CMD ["streamlit", "run", "📈Dashboard_Prediction.py"]
