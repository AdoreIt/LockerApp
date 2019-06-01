import os
import sys
import json

import pika
import requests
from flask import Flask, request, make_response
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
    cursor.execute(
        "insert into users (user_name, locker_id) values ('{}', {}); commit;".
        format(user_name, "NULL"))
    print("DB added user {} to db".format(user_name))


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
    print("DB users_db: got users from db")
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
            return {"status": "success", "data": locker}
        else:
            return {"status": "failed", "data": "user_without_locker"}
    else:
        return {"status": "failed", "data": "user_not_exists"}


def form_response(message_text, data):
    """
    Request structure:
    data = {
        "response": {
            "message": "message_text",
            "data": {
                "user_name": "Natalie", # or any other data
                "locker_id": None       # or any other data
            }
        }
    }
    """
    return {"response": {"message": message_text, "data": data}}


def resp_json(data, code):
    """Makes a Flask response with a JSON encoded body"""
    resp = make_response(json.dumps(data), code)
    return resp


class Users(Resource):
    def get(self):
        print("Users: get")
        try:
            print("Users: trying to get users")
            users = get_users_lockers_dict_from_db()
            print(users)
            users_answer = {'users': users}

            print("Users: sending answer {}".format(users_answer))
            return users_answer, 200
        except:
            print("Users: troubles")
            return 'Cannot connect to users db', 404


class UserService(Resource):
    def get(self):
        """
        Request structure:
        request = {"message" : "message_text", "user_name" : "name}
        """
        print("UserService: get")
        try:
            print("UserService: parsing request")
            message_req = request.form.to_dict()

            print("UserService: received request", message_req)

            if message_req["message"] == "check_user":
                user_name = message_req["user_name"]

                print("UserService: checking user {} in db".format(user_name))
                check_user_db_answer = get_users_locker(user_name)

                if check_user_db_answer["status"] == "failed":
                    answer = form_response(check_user_db_answer["data"], None)
                    # user_without_locker or user_not_exists
                    print("UserService: sending answer {}".format(answer))
                    return resp_json(answer, 400)
                else:
                    answer = form_response(
                        "user_with_locker", {
                            "user_name": user_name,
                            "locker_id": check_user_db_answer["data"]
                        })
                    print("UserService: sending answer {}".format(answer))
                    return resp_json(answer, 200)

            elif message_req["message"] == "get_locker_for_user":
                user_name = message_req["user_name"]

                print(
                    "UserService: sending rabbit request to get locker for user {}"
                    .format(user_name))
                get_locker_from_locker_service(message=user_name)

                print(
                    "UserService: sent rabbit request to get locker for user {}"
                    .format(user_name))
                answer = form_response("sent rabbit request", None)

                print("UserService: sending answer {}".format(answer))
                return resp_json(answer, 200)

            elif message_req["message"] == "add_user":
                user_name = message_req["user_name"]

                print("UserService: adding user {} to db".format(user_name))
                add_user_to_db(user_name)

                print("UserService: added user {} to db".format(user_name))
                answer = form_response("added user to db", None)

                print("UserService: sending answer {}".format(answer))
                return resp_json(answer, 200)

            elif message_req["message"] == "delete_user":
                user_name = message_req["user_name"]
                print("UserService: deleting user {} from db".format(user_name))
                delete_user_from_db(user_name)

                print("UserService: deleted user {} from db".format(user_name))
                answer = form_response("deleted user from db", None)

                print("UserService: sending answer {}".format(answer))
                return resp_json(answer, 200)

        except Exception as e:
            print("UserService: exception - {}".format(str(e)))
            return "Error {}".format(str(e)), 404


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
                    return answer, 200
            elif user_name_locker["locker_id"] == "no_lockers":
                print("UserLocker: no free lockers. Sending answer")
                return user_name_locker["locker_id"], 200
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

data = {
    "request": {
        "message": "message_text",
        "data": {
            "user_name": "Natalie",
            "locker_id": None
        }
    }
}
