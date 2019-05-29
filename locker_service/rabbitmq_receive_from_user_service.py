import sys
import os
import json

import pika
from requests import post
from locker_service import update_lockers_db, get_empty_locker_from_db

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
    print("LockerService is searching for empty locker")
    locker_id = get_empty_locker_from_db()
    if locker_id:
        try:
            print("LockerService: trying to send empty locker id")
            data = {"user_name": body, "locker_id": str(empty_locker_id)}
            resp = post('http://{}:{}/user_locker'
                        .format(config.user_service_ip,
                                config.user_service_port),
                        data=data)
            update_lockers_db(empty_locker_id, False)
            if resp.status_code == 200:
                print('LockerService: posted to UserService locker id: ',
                      data)
                return
            else:
                print('LockerService: Cannot make POST locker_id')
        except:
            print("LockerService: Failed to send locker id")
            return
    data = {"user_name": body, "locker_id": "no_lockers"}
    print(data)
    try:
        resp = post('http://{}:{}/user_locker'
                    .format(config.user_service_ip,
                            config.user_service_port),
                    data=data)
        if resp.status_code == 200:
            print('LockerService: posted to UserService locker id: ', data)
        else:
            print('LockerService: Cannot make POST np lockers')
    except:
        print("LockerService: Failed to send no lockers")


channel.basic_consume(
    queue='get_locker_id', on_message_callback=callback, auto_ack=True)

print("LockerService - RabbitMQ is waiting for messages. To exit press CTRL+C")
channel.start_consuming()
