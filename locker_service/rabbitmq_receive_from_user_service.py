import sys, os
import json

import pika
from requests import post
from locker_service import get_lockers_from_db

sys.path.append(os.path.abspath(os.path.join('config')))
from config import read_config

config = read_config()

credentials = pika.PlainCredentials(config.rabbitmq_username,
                                    config.rabbitmq_password)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='get_locker_id', durable=True)


def callback(ch, method, properties, body):
    body = str(body.decode("utf-8"))
    print("LockerService - RabbitMQ received: ", body)
    if body == "get_locker_id":
        print("LockerService is searching for empty locker")
        lockers_dict = get_lockers_from_db()
        for locker_id, is_empty in lockers_dict.items():
            if is_empty:
                try:
                    pass
                    # TODO: send locker_id to UserService via REST API
                    # TODO: update lockers DB to occupy locker with locker_id
                except:
                    print("LockerService: Failed to send empty locker id")


channel.basic_consume(
    queue='get_locker_id', on_message_callback=callback, auto_ack=True)

print("LockerService - RabbitMQ is waiting for messages. To exit press CTRL+C")
channel.start_consuming()
