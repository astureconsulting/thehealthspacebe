FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE ${PORT:-3050}  # Fallback to 3050 if $PORT not set
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT:-3050}", "bot:app"]  # Uses $PORT or defaults to 3050