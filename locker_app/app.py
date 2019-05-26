import requests
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '2'


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/users', methods=['GET'])
def users():
    error = None
    resp = None
    try:
        print("requesting from UserService")
        resp = requests.get(
            'http://192.168.43.76:5010/users_service',
            data={'hello': "UserService"})
        print("response: " + resp.text)
    except:
        error = "Service temporary unavailable. Please, try later"
        return render_template("users.html", error=error)

    if resp.status_code == 200:
        print("Loading response from UserService")
        resp = json.loads(resp.text)
        data = resp['hello']
        return render_template("users.html", data=data)
    else:
        error = "No Hello World for you >:|"
        return render_template("users.html", error=error)


@app.route('/lockers', methods=['GET'])
def lockers():
    error = None
    resp = None
    try:
        print("requesting from LockerService")
        resp = requests.get(
            'http://192.168.43.76:5020/locker_service',
            data={'hello': "LockerService"})
        print("response: " + resp.text)
    except:
        error = "Service temporary unavailable. Please, try later"
        return render_template("lockers.html", error=error)

    if resp.status_code == 200:
        print("Loading response from LockerService")
        resp = json.loads(resp.text)
        data = resp['hello']
        return render_template("lockers.html", data=data)
    else:
        error = "No Hello World for you >:|"
        return render_template("lockers.html", error=error)


if __name__ == "__main__":
    app.run(host="192.168.43.76", port="5000", debug=True)
