import sys, os

import requests
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

sys.path.append(os.path.abspath(os.path.join('config')))
from config import read_config

config = read_config()
app = Flask(__name__)
api = Api(app)


def get_lockers_from_db():
    """
    Getting lockers from DB and returning in dict format:
    dict = {1: True, 2: False, ...}
    TODO: Substitute dummy dictionary with DB data
    """
    lockers_dict = {1: True, 2: False, 3: True, 4: True, 5: True, 6: False}
    return lockers_dict


class LockerService(Resource):
    def get(self):
        print("LockerService: get to get lockers")
        try:
            print("LockerService: trying")
            answer = get_lockers_from_db()

            print("LockerService: ", answer)
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
