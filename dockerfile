FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .

ENV PORT=8000
ENV GROQ_API_KEY="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"

EXPOSE $PORT

CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "bot:app"]