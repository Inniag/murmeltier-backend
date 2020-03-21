from flask import Flask, request
from .database import connect, create_user as db_create_user, create_murmel as db_create_murmel, get_murmel_by_user_id as db_get_murmel_by_user_id, get_murmal_radar as db_get_murmel_radar, get_user_by_id
import uuid

app = Flask(__name__)


@app.route("/user", methods=["POST"])
def create_user():

    conn = connect()

    id, password = db_create_user(conn)

    message = {
        "id": id,
        "password": password
    }

    return (message, 200)


@app.route("/murmel", methods=["POST"])
def create_murmel():

    conn = connect()

    # TODO add user ID!
    params = request.get_json(force=True)
    # TODO: validate mood_value between 1 and 5?

    db_create_murmel(conn, params)

    return ("", 200)


@app.route("/murmel/me/current", methods=["GET"])
def get_current_murmel():

    conn = connect()

    # TODO: get user ID here!
    params = {
        "user_id": "1234"
    }

    murmel = db_get_murmel_by_user_id(conn, params)

    message = {
        "id": murmel[0],
        "mood_value": murmel[1],
        "hashtag": murmel[2],
        "created_at": murmel[3]
    }

    return (message, 200)


# TODO support location in route
@app.route("/murmel/radar", methods=["GET"])
def get_murmel_radar():

    # TODO: get user ID here!
    params = {
        "user_id": "1234"
    }

    murmel = db_get_murmel_radar(conn, params)

    return ("", 200)
