from flask import Flask, request
app = Flask(__name__)


@app.route("/user", methods = ["POST"])
def create_user():
    print(request.headers)


@app.route("/murmel", methods = ["POST"])
def create_murmel():
    print(request.headers)


@app.route("/murmel/me/current", methods = ["GET"])
def get_current_murmel():
    print(request.headers)


@app.route("/murmel/radar?location=Foo", methods = ["GET"])
def get_murmel_radar():
    print(request.headers)


if __name__ == "__main__":
    app.run()
