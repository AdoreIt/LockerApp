import requests
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)


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
            users_locker = get_users_locker(user_name_req)  # answer

            print("UserService: ", users_locker)
            result = {'users_locker': users_locker}

            print("UserService: sending answer")
            return result, 200
        except:
            print("UserService: 'Cannot connect to users db'")
            return 'Cannot connect to users db', 404


api.add_resource(Users, '/users')
api.add_resource(UserService, '/users_service')
if __name__ == '__main__':
    app.run(host="192.168.43.136", port="5010", debug=True)
