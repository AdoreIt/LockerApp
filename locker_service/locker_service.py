import os
import sys

import requests
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

sys.path.append(os.path.abspath(os.path.join('config')))
from config import read_config

from pymongo import MongoClient
from pymongo.read_preferences import ReadPreference

config = read_config()
app = Flask(__name__)
api = Api(app)


client = MongoClient('localhost',
                     replicaSet='lockers_rs',
                     read_preference=ReadPreference.SECONDARY,
                     serverSelectionTimeoutMS=10000)
lockers_db = client["lockers_db"]


def get_lockers_from_db():
    """
    Getting lockers from DB and returning in dict format:
    dict = {1: True, 2: False, ...}
    """
    lockers_collection = lockers_db["lockers"]
    return lockers_collection


def update_lockers_db(locker_id, is_empty):
    """
    Update instance in lockers DB
    TODO: Check work
    """
    lockers_collection = get_lockers_from_db()
    locker = lockers_collection.find_one({"_id": locker_id})
    try:
        locker["free"] = is_empty
        lockers_collection.save(locker)
    except:
        return False
    return True


def get_empty_locker_from_db():
    """
    Select locker_id from DB where is_empty = True
    Choose one of them
    If there are no empty lockers, return None
    TODO: Check work
    """
    lockers_collection = get_lockers_from_db()
    empty_locker = lockers_collection.find_one({"free": True})
    if empty_locker:
        return empty_locker["_id"]
    return None


class LockerService(Resource):
    def get(self):
        print("LockerService: get request to get lockers")
        try:
            print("LockerService: trying")
            answer = {}
            answer_cursor = get_lockers_from_db()
            for doc in answer_cursor.find():
                answer.update({doc["_id"]: doc["free"]})

            print("LockerService: ", answer)
            answer = {i: answer[i] for i in sorted(answer.keys())}
            result = {'lockers': answer}
            return result, 200
        except:
            print("LockerService: cannot connect to db")
            return '', 404


api.add_resource(LockerService, '/locker_service')
if __name__ == '__main__':
    app.run(
        host=config.locker_service_ip,
        port=config.locker_service_port,
        debug=True)
