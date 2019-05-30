import os
import sys

import pika
import requests
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

sys.path.append(os.path.abspath(os.path.join('config')))
from config import read_config

import psycopg2

config = read_config()
app = Flask(__name__)
api = Api(app)

credentials = pika.PlainCredentials(config.rabbitmq_username,
                                    config.rabbitmq_password)

postgre_connection = None

try:
    postgre_connection = psycopg2.connect(database="users_db", user="postgres")
except (psycopg2.InternalError, psycopg2.IntegrityError) as e:
    print("WARNING: Can not connect to users database")
    print("WARNING INFO: {}".format(e))

if postgre_connection is not None:
    print("Postgresql: set cursor")
    cursor = postgre_connection.cursor()


def get_locker_from_locker_service(queue_name='get_locker_id', message=''):
    print("UserService: connecting to RabbitMQ")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    print("UserService - RabbitMQ sent:  ", message)

    connection.close()


def add_user_to_db(user_name):
    """
    Adding user with name user_name to db
    """
    print("DB add_user_to_db")
    print(user_name)
    cursor.execute(
        "insert into users (user_name, locker_id) values ('{}', {}); commit;".
        format(user_name, "NULL"))

    print("DB added user to db")


def delete_user_from_db(user_name):
    """
    Delete user with name user_name from db
    """
    cursor.execute(
        "DELETE from users WHERE user_name = {}; commit;".format(user_name))


def update_locker_for_user_in_db(user_name, locker_id):
    """
    Update user with new locker_id (locker_id can be id or None)
    """
    print("DB update_locker_for_user_in_db for user {}, with locker {}".format(
        user_name, locker_id))
    cursor.execute(
        "UPDATE users SET locker_id = {} WHERE user_name = '{}'; commit;".
        format(int(locker_id), user_name))
    print("UserLocker: adding locker_id {} for user {}".format(
        locker_id, user_name))


def get_users_lockers_dict_from_db():
    """
    Getting users and their lockers from DB and returning in dict format:
    dict = {"Ann": None, "Olha": 1, ...}
    """
    print("DB users_db: getting users from db")
    cursor.execute("SELECT * FROM users;")
    data = cursor.fetchall()
    users_lockers = {}
    for row in data:
        users_lockers.update({row[1]: row[2]})
    return users_lockers


def get_users_locker(user_name):
    """
    Getting user's locker.
    Getting locker by user's name.
    If there is such user, and locker is not None - get his locker
    else try to get locker from LockerService bu user_name
    """
    users_lockers = get_users_lockers_dict_from_db()
    print("get_users_locker: ", users_lockers)
    if user_name in users_lockers:
        locker = users_lockers[user_name]
        if locker is not None:
            return locker
        else:
            get_locker_from_locker_service(message=user_name)
            return "user without locker"
    else:
        return "user not exists"


class Users(Resource):
    def get(self):
        print("Users: get")
        try:
            print("Users: trying to get users")
            users = get_users_lockers_dict_from_db()
            print(users)
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
            print("UserService: received request", user_name_req)

            users_locker = get_users_locker(user_name_req)  # answer
            print("UserService: ", users_locker)

            if users_locker == "user not exists":
                add_user_to_db(user_name_req)
                users_locker = get_users_locker(user_name_req)
                print(users_locker)

            print("UserService: ", users_locker)
            result = {'users_locker': users_locker}

            print("UserService: sending answer")
            return result, 200
        except:
            print("UserService: 'Cannot connect to locker service'")
            return 'Cannot connect to locker service', 404


class UserLocker(Resource):
    def post(self):
        print("UserLocker: receiving answer from LockerService")
        try:
            print("UserLocker: trying to receive answer from LockerService")
            user_name_locker = request.form.to_dict()
            print(user_name_locker)

            if user_name_locker["locker_id"] != "no_lockers":
                if user_name_locker["locker_id"] != "locker_db_error":
                    update_locker_for_user_in_db(user_name_locker["user_name"],
                                                 user_name_locker["locker_id"])
                    return user_name_locker, 200
                else:
                    answer = user_name_locker["locker_id"]
                    print("UserLocker: sending {}".format(
                        answer))  #locker_db_error
                    return answer, 201
            else:
                print("UserLocker: no free lockers")
            return "Received locker_id for user!", 200
        except:
            print(
                "UserLocker: error while receiving message from LockerService")


api.add_resource(Users, '/users')
api.add_resource(UserService, '/users_service')
api.add_resource(UserLocker, '/user_locker')
if __name__ == '__main__':
    app.run(
        host=config.user_service_ip, port=config.user_service_port, debug=True)
