import requests
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)


class UserService(Resource):
    def get(self):
        print("Trying")
        try:
            print("try")
            # TODO: Substitute dummy dictionary with DB data
            answer = {"User Ann": "Locker 1",
                      "User Olga": "Locker 3",
                      "User Natalie": "No locker assigned",
                      "User Alice": "Locker 2"}
            print(answer)
            result = {'hello': answer}
            return result, 200
        except:
            print("Hello World problems!")
            return '', 404


api.add_resource(UserService, '/users_service')
if __name__ == '__main__':
    app.run(host="192.168.43.76", port="5010", debug=True)
