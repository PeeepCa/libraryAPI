FROM python:3.9-slim

LABEL authors="Pokorny"

WORKDIR /app

# Upgrade pip first
RUN pip install --upgrade pip

# Install dependencies with fixed Werkzeug version
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt Werkzeug==2.2.3

COPY . .

EXPOSE 5000

# Explicitly name the container
ENV CONTAINER_NAME=library-api

CMD ["python", "app.py"]
