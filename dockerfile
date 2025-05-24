FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000
ENV GROQ_API_KEY="your-key-here"

EXPOSE $PORT

CMD ["gunicorn", "--worker-tmp-dir", "/dev/shm", "--bind", "0.0.0.0:$PORT", "--workers", "2", "--threads", "4", "--timeout", "120", "bot:application"]