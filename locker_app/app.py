import requests
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '2'


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/', methods=['POST'])
def check():
    message = None
    no_user_message = None
    no_locker_message = None
    error = None

    name = request.form.get("name", "")
    resp = requests.get('http://192.168.43.136:5010/users_service',
                        data={"user_name": name})

    if resp.status_code == 200:
        resp = json.loads(resp.text)
        locker_answer = resp["users_locker"]

        if locker_answer == "user not exists":
            no_user_message = "User {} doesn't exist".format(name)
        elif locker_answer == "user without locker":
            no_locker_message = "User {} has no locker".format(name)
        else:
            message = "User {} occupies locker {}".format(name, locker_answer)
    elif resp.status_code == 404:
        error = resp.text

    return render_template("check.html", success=message,
                           info=no_locker_message,
                           warning=no_user_message,
                           error=error)


@app.route('/users', methods=['GET'])
def users():
    error = None
    resp = None
    try:
        print("LockerApp: requesting from UserService")
        resp = requests.get('http://192.168.43.136:5010/users')
        print("LockerApp got response: " + resp.text)
    except:
        error = "Service temporary unavailable. Please, try later"
        return render_template("users.html", error=error)

    if resp.status_code == 200:
        print("LockerApp: Loading response from UserService")
        resp = json.loads(resp.text)
        data = resp["users"]
        return render_template("users.html", data=data)
    else:
        error = "No Hello World for you >:|"
        return render_template("users.html", error=error)


@app.route('/lockers', methods=['GET'])
def lockers():
    error = None
    resp = None
    try:
        print("LockerApp: requesting from LockerService")
        resp = requests.get('http://192.168.43.136:5020/locker_service',
                            data={'lockers': "LockerService"})
        print("LockerApp got response: " + resp.text)
    except:
        error = "Service temporary unavailable. Please, try later"
        return render_template("lockers.html", error=error)

    if resp.status_code == 200:
        print("LockerApp: Loading response from LockerService")
        resp = json.loads(resp.text)
        data = resp['lockers']
        return render_template("lockers.html", data=data)
    else:
        error = "No Hello World for you >:|"
        return render_template("lockers.html", error=error)


if __name__ == "__main__":
    app.run(host="192.168.43.76", port="5000", debug=True)
