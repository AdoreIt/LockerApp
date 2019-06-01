import os
import sys
import json

import pika
from requests import post
from locker_service import update_lockers_db, get_empty_locker_from_db

sys.path.append(os.path.abspath(os.path.join('config')))
sys.path.append(os.path.abspath(os.path.join('utils')))
from config import read_config
from logger import setup_logger

config = read_config()
logger = setup_logger()

credentials = pika.PlainCredentials(config.rabbitmq_username,
                                    config.rabbitmq_password)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='get_locker_id', durable=True)
channel.queue_declare(queue='free_locker_id', durable=True)


def callback_get(ch, method, properties, body):
    body = str(body.decode("utf-8"))
    logger.info(
        "LockerService RabbitMQ receiver: RabbitMQ received: {}".format(body))
    logger.info(
        "LockerService RabbitMQ receiver: is searching for empty locker")
    locker_id = get_empty_locker_from_db()
    logger.info(
        "LockerService RabbitMQ receiver: got locker_id {}".format(locker_id))
    if locker_id is not None:
        try:
            logger.info(
                "LockerService RabbitMQ receiver: trying to send empty locker id"
            )
            data = {"user_name": body, "locker_id": str(locker_id)}
            update_lockers_db(locker_id, False)
            logger.info("LockerService RabbitMQ receiver: Found empty locker")
            resp = post(
                'http://{}:{}/user_locker'.format(config.user_service_ip,
                                                  config.user_service_port),
                data=data)
            if resp.status_code == 200:
                logger.info(
                    'LockerService RabbitMQ receiver: posted to UserService locker id: ',
                    data)
                return
            else:
                logger.warning(
                    'LockerService RabbitMQ receiver: Cannot make POST locker_id'
                )
        except Exception as e:
            logger.critical(
                "LockerService RabbitMQ receiver: exception: {}".format(str(e)))
            return
    else:
        logger.warning("LockerService RabbitMQ receiver: no free lockers")
        data = {"user_name": body, "locker_id": "no_lockers"}
        try:
            logger.info(
                "LockerService RabbitMQ receiver: trying to post {}".format(
                    data))
            resp = post(
                'http://{}:{}/user_locker'.format(config.user_service_ip,
                                                  config.user_service_port),
                data=data)
            if resp.status_code == 200:
                logger.info(
                    'LockerService RabbitMQ receiver: posted to UserService locker id: {}'.format(data))
                return
            else:
                logger.error(
                    'LockerService RabbitMQ receiver: Cannot make POST no lockers'
                )
        except:
            logger.critical(
                "LockerService RabbitMQ receiver: Failed to send no lockers")


def callback_free(ch, method, properties, body):
    body = str(body.decode("utf-8"))
    data = {"user_name": body, "locker_id": "NULL"}
    logger.info(
        "LockerService RabbitMQ receiver: RabbitMQ received: {}".format(body))
    logger.info("LockerService RabbitMQ receiver: frees up locker")
    if update_lockers_db(int(body), True):
        try:
            logger.info(
                "LockerService RabbitMQ receiver: trying to post {}".format(
                    body))
            resp = post(
                'http://{}:{}/user_locker'.format(config.user_service_ip,
                                                  config.user_service_port),
                data=data)
            if resp.status_code == 200:
                logger.info(
                    'LockerService RabbitMQ receiver: posted to UserService: {}'.format(body))
                return
            else:
                logger.error('LockerService RabbitMQ receiver: Cannot make POST about free locker')
        except Exception as e:
            logger.critical(
                "LockerService RabbitMQ receiver: Failed to send no lockers {}".format(e))
    else:
        logger.warning("Cannot empty locker: DB errors")
        data = {"user_name": body, "locker_id": "locker_db_error"}
        try:
            logger.info(
                "LockerService RabbitMQ receiver: trying to post: None")
            resp = post(
                'http://{}:{}/user_locker'.format(config.user_service_ip,
                                                  config.user_service_port),
                data=data)
            if resp.status_code == 200:
                logger.info(
                    'LockerService RabbitMQ receiver: posted to UserService: None')
                return
            else:
                logger.error('LockerService RabbitMQ receiver: Cannot make POST about unable to free up locker')
        except Exception as e:
            logger.critical(
                "LockerService RabbitMQ receiver: Failed to send no lockers {}".format(e))


channel.basic_consume(
    queue='get_locker_id', on_message_callback=callback_get, auto_ack=True)

channel.basic_consume(
    queue='free_locker_id', on_message_callback=callback_free, auto_ack=True)

logger.info(
    "LockerService RabbitMQ receiver: RabbitMQ is waiting for messages. To exit press CTRL+C"
)
channel.start_consuming()
