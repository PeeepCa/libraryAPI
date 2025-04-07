FROM python:3.9-slim

LABEL authors="Pokorny"

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt Werkzeug==2.2.3

COPY . .

EXPOSE 5000

ENV CONTAINER_NAME=library-api

CMD ["python", "app.py"]