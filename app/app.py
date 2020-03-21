from flask import Flask, request
from .database import connect, create_user, get_user_by_id

app = Flask(__name__)


@app.route("/user", methods=["POST"])
def create_user():
    print(request.headers)


@app.route("/murmel", methods=["POST"])
def create_murmel():
    print(request.headers)


@app.route("/murmel/me/current", methods=["GET"])
def get_current_murmel():
    print(request.headers)


@app.route("/murmel/radar?location=Foo", methods=["GET"])
def get_murmel_radar():
    print(request.headers)


@app.route("/test", methods=["GET"])
def test():
    conn = connect()
    create_user(conn)
    get_user_by_id(conn, 1)
