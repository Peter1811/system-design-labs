import json

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from confluent_kafka import Consumer, KafkaException, KafkaError
from sqlalchemy.orm import Session
from time import sleep

from app.models import Conference
from app.db_config import SessionLocal

KAFKA_BROKER = 'kafka1:9092'
KAFKA_TOPIC = 'conference_topic'
GROUP_ID = 'conference-consumer-group'


def create_kafka_consumer():
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': GROUP_ID,
        'auto.offset.reset': 'earliest'
    })
    return consumer


def consume_messages(consumer, db_session: Session):
    consumer.subscribe([KAFKA_TOPIC])
    try:
        while True:
            msg = consumer.poll(timeout=1.0)  # Получаем сообщение с таймаутом 1 секунда
            if msg is None:
                continue
            elif msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # Мы достигли конца раздела, продолжаем
                    continue
                else:
                    raise KafkaException(msg.error())
            else:
                # Декодируем сообщение (предположим, что оно в JSON формате)
                message = msg.value().decode('utf-8')
                data = json.loads(message)

                # Добавляем данные в базу данных
                try:
                    name, description = data.split('=>')
                    new_pres = Conference(name=name, description=description)
                    db_session.add(new_pres)
                    db_session.commit()
                    print(f"Added conference: {name}")
                except Exception as e:
                    db_session.rollback()
                    print(f"Error adding conference: {e}")
    except Exception as e:
        print(f"Error consuming messages: {e}")
    finally:
        consumer.close()


def run_periodically(db_session: Session):
    consumer = create_kafka_consumer()
    consume_messages(consumer, db_session)


def start_scheduler():
    scheduler = BackgroundScheduler()
    # Запускаем задачу каждые 10 секунд
    scheduler.add_job(
        run_periodically, 
        IntervalTrigger(seconds=10),
        args=[SessionLocal()], 
        id="kafka_consumer_job", 
        replace_existing=True  
    )
    scheduler.start()

    try:
        # Держим приложение работающим
        while True:
            sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == '__main__':
    start_scheduler()