FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PORT=8000
EXPOSE $PORT

CMD ["python", "bot.py"]