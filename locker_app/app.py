from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '2'


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/users')
def users():
    return render_template("users.html")


@app.route('/lockers')
def lockers():
    return render_template("lockers.html")


if __name__ == "__main__":
    app.run(host="192.168.43.76", port="5000", debug=True)
