import os
import sys
import json
import random
from time import sleep

import requests
from flask import Flask, render_template, request, make_response

sys.path.append(os.path.abspath(os.path.join('config')))
sys.path.append(os.path.abspath(os.path.join('utils')))
from config import read_config
from logger import setup_logger

config = read_config()
logger = setup_logger()

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
    logger.info("LockerApp: Sending request to UserService: {}".format(data))
    try:
        resp = requests.get(
            'http://{0}:{1}/users_service'.format(config.user_service_ip,
                                                  config.user_service_port),
            data=data)
        if resp.status_code == 200:
            resp = json.loads(resp.text)
            locker_answer = resp["response"]["data"]["locker_id"]
            logger.info("LockerApp received response that user {} has locker {}".format(name, locker_answer))
            message = "User {} occupies locker {}".format(
                name, locker_answer)
            return render_template(
                "check.html",
                success=message,
                locker_exists=True,
                animal_class=animal_class, animal_name=animal_name)
        elif resp.status_code == 400:
            resp = json.loads(resp.text)
            locker_answer = resp["response"]
            logger.warning("LockerApp received: user {} has locker {}".format(
                name, locker_answer))

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
                    user_exists=True,
                    animal_class=animal_class, animal_name=animal_name))
                resp.set_cookie("user_name", name)
                return resp

    except Exception as e:
        logger.critical("Exception {}".format(e))
        error = str(e)
        return render_template(
            "check.html",
            error=error,
            animal_class=animal_class, animal_name=animal_name)


@app.route("/adduser", methods=['POST'])
def add_user():
    logger.info("LockerApp: In add user function")
    message = None
    error = None
    name = request.cookies.get("user_name")
    data = {"message": "add_user", "user_name": name}
    logger.info("LockerApp: Sending request to UserService: {}".format(data))
    try:
        resp = requests.get(
            'http://{0}:{1}/users_service'.format(config.user_service_ip,
                                                  config.user_service_port),
            data=data)

        if resp.status_code == 200:
            resp = json.loads(resp.text)
            logger.info("LockerApp received: {}".format(resp))
            message = "User {} added. Return to Home screen to continue".format(name)
        elif resp.status_code == 404:
            resp = json.loads(resp.text)
            logger.warning("LockerApp received: {}".format(resp))
            error = "User {} already exists. Return to Home screen to continue".format(name)
            return render_template(
                "check.html",
                error=error,
                animal_class=animal_class, animal_name=animal_name)

    except Exception as e:
        logger.critical("Exception {}".format(e))
        message = "LockerApp: Adding user service temporary anavailable"

    return render_template(
        "check.html",
        success=message,
        error=error,
        animal_class=animal_class, animal_name=animal_name)


@app.route("/delete_user", methods=['POST'])
def delete_user():
    logger.info("LockerApp: In delete user function")
    message = None
    error = None
    name = request.cookies.get("user_name")
    data = {"message": "delete_user", "user_name": name}
    logger.info("LockerApp: Sending request to UserService: {}".format(data))
    try:
        resp = requests.get(
            'http://{0}:{1}/users_service'.format(config.user_service_ip,
                                                  config.user_service_port),
            data=data)

        if resp.status_code == 200:
            resp = json.loads(resp.text)
            logger.info("LockerApp received: {}".format(resp))
            message = "User {} deleted. Return to Home screen to continue".format(name)
        elif resp.status_code == 404:
            resp = json.loads(resp.text)
            logger.warning("LockerApp received: {}".format(resp))
            error = "User {} doesn't exist. Return to Home screen to continue".format(name)
            return render_template(
                "check.html",
                error=error,
                animal_class=animal_class, animal_name=animal_name)

    except Exception as e:
        logger.critical("Exception {}".format(e))
        message = "LockerApp: Adding user service temporary anavailable"

    return render_template(
        "check.html",
        success=message,
        error=error,
        animal_class=animal_class, animal_name=animal_name)


@app.route("/addlocker", methods=['GET', 'POST'])
def add_locker():
    logger.info("LockerApp: In add locker function")
    message = None
    error = None
    name = request.cookies.get("user_name")
    data = {"message": "get_locker_for_user", "user_name": name}
    logger.info("LockerApp: Sending request to UserService: {}".format(data))
    try:
        resp = requests.get(
            'http://{0}:{1}/users_service'.format(config.user_service_ip,
                                                  config.user_service_port),
            data=data)
        if resp.status_code == 200:
            data = {"message": "check_user", "user_name": name}
            logger.info("LockerApp: Sending request to UserService: {}".format(data))
            sleep(0.5)
            try:
                resp = requests.get(
                    'http://{0}:{1}/users_service'.format(
                        config.user_service_ip, config.user_service_port),
                    data=data)

                if resp.status_code == 200:
                    resp = json.loads(resp.text)
                    locker_answer = resp["response"]["data"]["locker_id"]
                    logger.info("LockerApp received response that user {} occupies locker {}", name, locker_answer)
                    message = "User {} occupies locker {}. Return to Home screen to continue".format(
                            name, locker_answer)
                    return render_template(
                        "check.html",
                        success=message,
                        locker_exists=True,
                        animal_class=animal_class, animal_name=animal_name)
                elif resp.status_code == 400:
                    resp = json.loads(resp.text)
                    locker_answer = resp["response"]
                    logger.warning("LockerApp received: {}".format(locker_answer))

                    if locker_answer["message"] == "user_without_locker":
                        no_locker_message = "No free lockers found. Return to Home screen to continue"
                        resp = make_response(render_template(
                            "check.html",
                            info=no_locker_message,
                            no_locker=True,
                            user_exists=True,
                            animal_class=animal_class,
                            animal_name=animal_name))
                        resp.set_cookie("user_name", name)
                        return resp

            except Exception as e:
                logger.critical("Exception {}".format(e))
                error = str(e)

            return render_template(
                "check.html",
                error=error,
                animal_class=animal_class, animal_name=animal_name)

        else:
            logger.error("Error while adding user")
            error = "Error occurred. Return to Home screen to continue".format(name)
            return render_template(
                "check.html",
                error=error,
                animal_class=animal_class, animal_name=animal_name)

    except Exception as e:
        logger.critical("Exception {}".format(e))
        error = str(e)

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
        logger.info("LockerApp: requesting from UserService")
        resp = requests.get('http://{0}:{1}/users'.format(
            config.user_service_ip, config.user_service_port))
        logger.info("LockerApp got response: {}".format(resp.text))

        if resp.status_code == 200:
            logger.info("LockerApp: Loading response from UserService")
            resp = json.loads(resp.text)
            data = resp["users"]
            return render_template("users.html", data=data,
                                   animal_class=animal_class,
                                   animal_name=animal_name)
        else:
            error = resp.text
            logger.error(error)
            return render_template("users.html", error=error,
                                   animal_class=animal_class,
                                   animal_name=animal_name)

    except Exception as e:
        logging.critical(e)
        error = "Service temporary unavailable. Please, try later"
        return render_template("users.html", error=error,
                               animal_class=animal_class,
                               animal_name=animal_name)


@app.route('/lockers', methods=['GET'])
def lockers():
    error = None
    resp = None
    try:
        logger.info("LockerApp: requesting from LockerService")
        resp = requests.get(
            "http://{0}:{1}/locker_service".format(config.locker_service_ip,
                                                   config.locker_service_port),
            data={'lockers': "LockerService"})
        logger.info("LockerApp got response: {}".format(resp.text))

        if resp.status_code == 200:
            logger.info("LockerApp: Loading response from LockerService")
            resp = json.loads(resp.text)
            data = resp['lockers']
            return render_template("lockers.html", data=data,
                                   animal_class=animal_class,
                                   animal_name=animal_name)
        else:
            error = resp.text
            logger.error(error)
            return render_template("lockers.html", error=error,
                                   animal_class=animal_class,
                                   animal_name=animal_name)

    except Exception as e:
        logging.critical(e)
        error = "Service temporary unavailable. Please, try later"
        return render_template("lockers.html", error=error,
                               animal_class=animal_class,
                               animal_name=animal_name)

if __name__ == "__main__":
    app.run(host=config.locker_app_ip, port=config.locker_app_port, debug=True)
