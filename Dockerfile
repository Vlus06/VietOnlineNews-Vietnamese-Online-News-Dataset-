FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY src/ src/
COPY scripts/ scripts/
COPY README.md .

EXPOSE 8501

CMD ["sh", "-c", "python scripts/download_data.py && python -m streamlit run app/streamlit_app.py --server.address=0.0.0.0 --server.port=8501"]