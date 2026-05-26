FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --default-timeout=120 --retries=10 -r requirements.txt

COPY app/ app/
COPY src/ src/
COPY scripts/ scripts/
COPY data/dashboard_cache/ data/dashboard_cache/
COPY README.md .

EXPOSE 8501

CMD ["sh", "-c", "echo '========================================' && echo ' VietOnlineNews Dashboard is starting...' && echo ' Open dashboard at: http://localhost:8501' && echo '========================================' && python -m streamlit run app/streamlit_app.py --server.address=0.0.0.0 --server.port=8501"]