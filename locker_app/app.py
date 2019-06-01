import os
import sys
import json
import random
from time import sleep

import requests
from flask import Flask, render_template, request, make_response

sys.path.append(os.path.abspath(os.path.join('config')))
from config import read_config

config = read_config()
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '2'


animal_dict = {"cat": "Furry", "crow": "Black", "dog": "Happy",
               "dove": "White", "dragon": "Chinese", "fish": "Wet",
               "frog": "Green", "hippo": "Cute", "horse": "Fast",
               "kiwi-bird": "Small", "otter": "Cunny", "spider": "Frightening"}
animal = random.choice(list(animal_dict.keys()))
animal_class = "fas fa-" + animal
animal_name = animal_dict[animal] + " " + animal


@app.route('/')
def home():
    print(animal_class)
    return render_template("home.html",
                           animal_class=animal_class, animal_name=animal_name)


@app.route('/', methods=['POST'])
def check():
    message = None
    no_user_message = None
    no_locker_message = None
    error = None

    name = request.form.get("name", "")
    data = {"message": "check_user", "user_name": name}
    print("LockerApp: Sending request to UserService: ", data)
    try:
        resp = requests.get(
            'http://{0}:{1}/users_service'.format(config.user_service_ip,
                                                  config.user_service_port),
            data=data)

        if resp.status_code == 200:
            resp = json.loads(resp.text)
            locker_answer = resp["response"]["data"]["locker_id"]
            message = "User {} occupies locker {}".format(name,
                                                          locker_answer)
        elif resp.status_code == 400:
            resp = json.loads(resp.text)
            locker_answer = resp["response"]

            if locker_answer["message"] == "user_not_exists":
                no_user_message = "User {} doesn't exist".format(name)
                resp = make_response(render_template(
                    "check.html",
                    info=no_user_message,
                    no_user=True,
                    animal_class=animal_class, animal_name=animal_name))
                resp.set_cookie("user_name", name)
                return resp

            if locker_answer["message"] == "user_without_locker":
                no_locker_message = "User {} has no locker".format(name)
                resp = make_response(render_template(
                    "check.html",
                    info=no_locker_message,
                    no_locker=True,
                    animal_class=animal_class, animal_name=animal_name))
                resp.set_cookie("user_name", name)
                return resp

    except Exception as e:
        print("Exception", e)
        error = e

    return render_template(
        "check.html",
        success=message,
        error=error,
        animal_class=animal_class, animal_name=animal_name)


@app.route("/adduser", methods=['POST'])
def add_user():
    print("LockerApp: In add user function")
    message = None
    error = None
    name = request.cookies.get("user_name")
    data = {"message": "add_user", "user_name": name}
    print("LockerApp: Sending request to UserService: ", data)
    try:
        resp = requests.get(
            'http://{0}:{1}/users_service'.format(config.user_service_ip,
                                                  config.user_service_port),
            data=data)

        if resp.status_code == 200:
            resp = json.loads(resp.text)
            message = "User {} added. \
                Return to Home screen to continue".format(name)
        elif resp.status_code == 404:
            resp = json.loads(resp.text)
            error = "User {} already exists. \
                Return to Home screen to continue".format(name)
            return render_template(
                "check.html",
                error=error,
                animal_class=animal_class, animal_name=animal_name)

    except Exception as e:
        print("Exception", e)
        message = "LockerApp: Adding user service temporary anavailable"

    return render_template(
        "check.html",
        success=message,
        error=error,
        animal_class=animal_class, animal_name=animal_name)


@app.route("/addlocker", methods=['GET', 'POST'])
def add_locker():
    print("LockerApp: In add locker function")
    message = None
    error = None
    name = request.cookies.get("user_name")
    data = {"message": "get_locker_for_user", "user_name": name}
    print("LockerApp: Sending request to UserService: ", data)
    try:
        resp = requests.get(
            'http://{0}:{1}/users_service'.format(config.user_service_ip,
                                                  config.user_service_port),
            data=data)
        print(resp.text)

        if resp.status_code == 200:
            data = {"message": "check_user", "user_name": name}
            print("LockerApp: Sending request to UserService: ", data)
            sleep(0.5)
            try:
                resp = requests.get(
                    'http://{0}:{1}/users_service'.format(
                        config.user_service_ip, config.user_service_port),
                    data=data)

                print(resp.text)

                if resp.status_code == 200:
                    resp = json.loads(resp.text)
                    print("200")
                    locker_answer = resp["response"]["data"]["locker_id"]
                    message = "User {} occupies locker {}. \
                        Return to Home screen to continue".format(
                            name, locker_answer)
                elif resp.status_code == 400:
                    print("400")
                    resp = json.loads(resp.text)
                    locker_answer = resp["response"]

                    if locker_answer["message"] == "user_without_locker":
                        no_locker_message = "No free lockers found. \
                            Return to Home screen to continue"
                        resp = make_response(render_template(
                            "check.html",
                            info=no_locker_message,
                            no_locker=True,
                            animal_class=animal_class,
                            animal_name=animal_name))
                        resp.set_cookie("user_name", name)
                        return resp

            except Exception as e:
                print("Exception", e)
                error = e

            return render_template(
                "check.html",
                success=message,
                error=error,
                animal_class=animal_class, animal_name=animal_name)

        else:
            error = "Error occured. \
                Return to Home screen to continue".format(name)
            return render_template(
                "check.html",
                error=error,
                animal_class=animal_class, animal_name=animal_name)

    except Exception as e:
        print("Exception", e)
        error = e

    return render_template(
        "check.html",
        success=message,
        error=error,
        animal_class=animal_class, animal_name=animal_name)


@app.route('/users', methods=['GET'])
def users():
    error = None
    resp = None
    try:
        print("LockerApp: requesting from UserService")
        resp = requests.get('http://{0}:{1}/users'.format(
            config.user_service_ip, config.user_service_port))
        print("LockerApp got response: " + resp.text)

        if resp.status_code == 200:
            print("LockerApp: Loading response from UserService")
            resp = json.loads(resp.text)
            data = resp["users"]
            return render_template("users.html", data=data,
                                   animal_class=animal_class,
                                   animal_name=animal_name)
        else:
            error = resp.text
            return render_template("users.html", error=error,
                                   animal_class=animal_class,
                                   animal_name=animal_name)

    except:
        error = "Service temporary unavailable. Please, try later"
        return render_template("users.html", error=error,
                               animal_class=animal_class,
                               animal_name=animal_name)


@app.route('/lockers', methods=['GET'])
def lockers():
    error = None
    resp = None
    try:
        print("LockerApp: requesting from LockerService")
        resp = requests.get(
            "http://{0}:{1}/locker_service".format(config.locker_service_ip,
                                                   config.locker_service_port),
            data={'lockers': "LockerService"})
        print("LockerApp got response: " + resp.text)

        if resp.status_code == 200:
            print("LockerApp: Loading response from LockerService")
            resp = json.loads(resp.text)
            data = resp['lockers']
            return render_template("lockers.html", data=data,
                                   animal_class=animal_class,
                                   animal_name=animal_name)
        else:
            error = resp.text
            return render_template("lockers.html", error=error,
                                   animal_class=animal_class,
                                   animal_name=animal_name)

    except:
        error = "Service temporary unavailable. Please, try later"
        return render_template("lockers.html", error=error,
                               animal_class=animal_class,
                               animal_name=animal_name)

if __name__ == "__main__":
    app.run(host=config.locker_app_ip, port=config.locker_app_port, debug=True)
