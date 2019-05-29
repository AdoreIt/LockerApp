import sys, os

import pika
import requests
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

sys.path.append(os.path.abspath(os.path.join('config')))
from config import read_config

config = read_config()
app = Flask(__name__)
api = Api(app)

credentials = pika.PlainCredentials(config.rabbitmq_username,
                                    config.rabbitmq_password)


def get_locker_from_locker_service(queue_name='get_locker_id', message=''):
    print("UserService: connecting to RabbitMQ")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    print("UserService - RabbitMQ sent:  ", message)

    connection.close()


def get_users_lockers_dict():
    """
    Getting users from DB and returning in dict format:
    dict = {"Ann": None, "Olha": 1, ...}
    TODO: Substitute dummy dictionary with DB data
    """
    users_lockers = {"Ann": 1, "Olha": 2, "Natalie": None, "Alice": 3}
    return users_lockers


def get_users_locker(user_name):
    users_lockers = get_users_lockers_dict()
    if user_name in users_lockers:
        locker = users_lockers[user_name]
        if locker is not None:
            return locker
        else:
            get_locker_from_locker_service(message="get_locker_id")
            return "user without locker"
    else:
        return "user not exists"


class Users(Resource):
    def get(self):
        print("Users: get")
        try:
            print("Users: trying to get users")
            users = get_users_lockers_dict()
            users_answer = {'users': users}

            print("Users: sending answer")
            return users_answer, 200
        except:
            print("Users: troubles")
            return 'Cannot connect to users db', 404


class UserService(Resource):
    def get(self):
        print("UserService: get")
        try:
            print("UserService: trying to get user's locker")
            user_name_req = request.form['user_name']
            # TODO: Substitute dummy dictionary with DB data
            # TODO: Change request structure to:
            # request_structure = {
            #     'request_message': "message from with req to do smth",
            #     'data': 'data'
            # }

            users_locker = get_users_locker(user_name_req)  # answer

            print("UserService: ", users_locker)
            result = {'users_locker': users_locker}

            print("UserService: sending answer")
            return result, 200
        except:
            print("UserService: 'Cannot connect to locker service'")
            return 'Cannot connect to locker service', 404


api.add_resource(Users, '/users')
api.add_resource(UserService, '/users_service')
if __name__ == '__main__':
    app.run(
        host=config.user_service_ip, port=config.user_service_port, debug=True)
