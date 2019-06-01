import os
import sys
import json

import pika
import requests
from flask import Flask, request, make_response
from flask_restful import Resource, Api, reqparse

sys.path.append(os.path.abspath(os.path.join('config')))
sys.path.append(os.path.abspath(os.path.join('utils')))
from config import read_config
from logger import setup_logger

import psycopg2

config = read_config()
logger = setup_logger()

app = Flask(__name__)
api = Api(app)

credentials = pika.PlainCredentials(config.rabbitmq_username,
                                    config.rabbitmq_password)

postgre_connection = None

try:
    postgre_connection = psycopg2.connect(database="users_db", user="postgres")
except (psycopg2.InternalError, psycopg2.IntegrityError) as e:
    logger.warning("WARNING: Can not connect to users database")
    logger.warning("WARNING INFO: {}".format(e))

if postgre_connection is not None:
    logger.info("Postgresql: set cursor")
    cursor = postgre_connection.cursor()


def get_locker_from_locker_service(queue_name='get_locker_id', message=''):
    logger.info("UserService: connecting to RabbitMQ")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    logger.info("UserService - RabbitMQ sent:  {}".format(message))

    connection.close()


def add_user_to_db(user_name):
    """
    Adding user with name user_name to db
    """
    cursor.execute(
        "insert into users (user_name, locker_id) values ('{}', {}); commit;".
        format(user_name, "NULL"))
    logger.info("DB added user {} to db".format(str(user_name)))


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
    logger.info(
        "DB update_locker_for_user_in_db for user {}, with locker {}".format(
            user_name, locker_id))
    cursor.execute(
        "UPDATE users SET locker_id = {} WHERE user_name = '{}'; commit;".
        format(int(locker_id), user_name))
    logger.info("UserLocker: adding locker_id {} for user {}".format(
        locker_id, user_name))


def get_users_lockers_dict_from_db():
    """
    Getting users and their lockers from DB and returning in dict format:
    dict = {"Ann": None, "Olha": 1, ...}
    """
    logger.info("DB users_db: getting users from db")
    cursor.execute("SELECT * FROM users;")
    logger.info("DB users_db: got users from db")
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
    logger.info("UserService.get_users_locker: ", users_lockers)
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
        logger.info("Users: get")
        try:
            logger.info("Users: trying to get users")
            users = get_users_lockers_dict_from_db()
            users_answer = {'users': users}

            logger.info("Users: sending answer {}".format(users_answer))
            return users_answer, 200
        except Exception as e:
            logger.error("Users exception: troubles".format(str(e)))
            return 'Cannot connect to users db', 404


class UserService(Resource):
    def get(self):
        """
        Request structure:
        request = {"message" : "message_text", "user_name" : "name}
        """
        logger.info("UserService: get")
        try:
            logger.info("UserService: parsing request")
            message_req = request.form.to_dict()

            logger.info("UserService: received request", message_req)

            if message_req["message"] == "check_user":
                user_name = message_req["user_name"]

                logger.info(
                    "UserService: checking user {} in db".format(user_name))
                check_user_db_answer = get_users_locker(user_name)

                if check_user_db_answer["status"] == "failed":
                    answer = form_response(check_user_db_answer["data"], None)
                    # user_without_locker or user_not_exists
                    logger.warning(
                        "UserService: sending answer {}".format(answer))
                    return resp_json(answer, 400)
                else:
                    answer = form_response(
                        "user_with_locker", {
                            "user_name": user_name,
                            "locker_id": check_user_db_answer["data"]
                        })
                    logger.info("UserService: sending answer {}".format(answer))
                    return resp_json(answer, 200)

            elif message_req["message"] == "get_locker_for_user":
                user_name = message_req["user_name"]

                logger.info(
                    "UserService: sending rabbit request to get locker for user {}"
                    .format(user_name))
                get_locker_from_locker_service(message=user_name)

                logger.info(
                    "UserService: sent rabbit request to get locker for user {}"
                    .format(user_name))
                answer = form_response("sent rabbit request", None)

                logger.info("UserService: sending answer {}".format(answer))
                return resp_json(answer, 200)

            elif message_req["message"] == "add_user":
                user_name = message_req["user_name"]

                logger.info(
                    "UserService: adding user {} to db".format(user_name))
                add_user_to_db(user_name)

                logger.info(
                    "UserService: added user {} to db".format(user_name))
                answer = form_response("added user to db", None)

                logger.info("UserService: sending answer {}".format(answer))
                return resp_json(answer, 200)

            elif message_req["message"] == "delete_user":
                user_name = message_req["user_name"]
                logger.info(
                    "UserService: deleting user {} from db".format(user_name))
                delete_user_from_db(user_name)

                logger.info(
                    "UserService: deleted user {} from db".format(user_name))
                answer = form_response("deleted user from db", None)

                logger.info("UserService: sending answer {}".format(answer))
                return resp_json(answer, 200)

        except Exception as e:
            logger.critical("UserService: exception - {}".format(str(e)))
            return "Error {}".format(str(e)), 404


class UserLocker(Resource):
    def post(self):
        try:
            logger.info(
                "UserLocker: parcing post from LockerService RabbitMQ receiver")
            user_name_locker = request.form.to_dict()
            logger.info(
                "UserLocker: parsed '{}' from LockerService RabbitMQ receiver".
                format(user_name_locker))

            locker_rabbitmq_answer = user_name_locker["locker_id"]

            if locker_rabbitmq_answer == "no_lockers":
                logger.warning(
                    "UserLocker: sending {}".format(locker_rabbitmq_answer))
                return locker_rabbitmq_answer, 200

            elif locker_rabbitmq_answer == "locker_db_error":
                answer = user_name_locker["locker_id"]
                logger.error("UserLocker: sending {}".format(answer))
                return answer, 404

            else:
                update_locker_for_user_in_db(user_name_locker["user_name"],
                                             user_name_locker["locker_id"])
                logger.info("UserLocker: sent {}".format(user_name_locker))
                return user_name_locker, 200

        except Exception as e:
            logger.critical(
                "UserLocker: error while receiving message from LockerService.\n Exception info: {}"
                .format(str(e)))


api.add_resource(Users, '/users')
api.add_resource(UserService, '/users_service')
api.add_resource(UserLocker, '/user_locker')
if __name__ == '__main__':
    app.run(
        host=config.user_service_ip, port=config.user_service_port, debug=True)