import os
import sys
import json
import random

import requests
from flask import Flask, render_template, request, redirect, url_for

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
    try:
        resp = requests.get(
            'http://{0}:{1}/users_service'.format(config.user_service_ip,
                                                  config.user_service_port),
            data={"user_name": name})

        if resp.status_code == 200:
            resp = json.loads(resp.text)
            locker_answer = resp["users_locker"]

            if locker_answer == "user not exists":
                no_user_message = "User {} doesn't exist".format(name)
            if locker_answer == "user without locker":
                no_locker_message = "User {} has no locker".format(name)
            else:
                message = "User {} occupies locker {}".format(name,
                                                              locker_answer)
        elif resp.status_code == 404:
            error = resp.text

    except:
        error = "Service temporary anavailable"

    return render_template(
        "check.html",
        success=message,
        info=no_locker_message,
        warning=no_user_message,
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
