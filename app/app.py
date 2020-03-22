from flask import Flask, request, abort
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from .database import (
    create_user as db_create_user,
    connect,
    create_user as db_create_user,
    create_murmel as db_create_murmel,
    get_murmel_by_user_id as db_get_murmel_by_user_id,
    get_murmel_radar as db_get_murmel_radar,
    get_user_by_id,
)
from .auth import login
import uuid

app = Flask(__name__)
auth = HTTPBasicAuth()
CORS(app)
conn = connect()


@auth.verify_password
def verify_password(username, password):
    print("verify_password")
    return login(conn, username, password)


@app.route("/user", methods=["POST"])
def create_user():

    conn = connect()

    id, password = db_create_user(conn)

    message = {"id": id, "password": password}

    return (message, 200)


@app.route("/murmel", methods=["POST"])
@auth.login_required
def create_murmel():

    conn = connect()

    # murmel info from request
    params = request.get_json(force=True)
    # TODO: validate mood_value between 1 and 5?

    id = db_create_murmel(
        conn, params["mood_value"], params["hashtag"], auth.username()
    )

    message = {"id": id}

    return (message, 200)


@app.route("/murmel/me/current", methods=["GET"])
@auth.login_required
def get_current_murmel():

    conn = connect()

    print(auth.username())
    murmel = db_get_murmel_by_user_id(conn, auth.username())

    # special case when user has no murmel
    if murmel is None:

        return ("", 404)

    else:

        message = {
            "id": murmel[0],
            "mood_value": murmel[1],
            "hashtag": murmel[2],
            "created_at": murmel[4],
        }

        return (message, 200)


# TODO support location in route
@app.route("/murmel/radar", methods=["GET"])
@auth.login_required
def get_murmel_radar():

    # TODO: get user ID here!
    params = {"user_id": "1234"}

    murmel = db_get_murmel_radar(conn, params)
    return ("", 200)


@app.route("/test", methods=["GET"])
@auth.login_required
def test():
    return (auth.username(), 200)
