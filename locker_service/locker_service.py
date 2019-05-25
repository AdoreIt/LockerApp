import requests
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)


class LockerService(Resource):
    def get(self):
        print("Trying")
        try:
            print("try")
            answer = request.form['hello']
            print(answer)
            result = {'hello': answer}
            return result, 200
        except:
            print("Hello World problems!")
            return '', 404


api.add_resource(LockerService, '/locker_service')
if __name__ == '__main__':
    app.run(host="192.168.43.76", port="5020", debug=True)
