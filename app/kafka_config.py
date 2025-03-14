from confluent_kafka import Producer

conf = {
    'bootstrap.servers': 'kafka1:9092', 
    'client.id': 'fastapi-producer'
}

producer = Producer(conf)

def send_data_to_kafka(topic: str, message: str):
    producer.produce(topic, message.encode('utf-8'))
    producer.flush()