FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./kafka_read/collect_data_from_kafka.py /app/collect_data_from_kafka.py
COPY . .