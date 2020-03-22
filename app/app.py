from flask import Flask, request, abort
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from flask import jsonify
from .database import (
    create_user as db_create_user,
    connect,
    create_user as db_create_user,
    create_murmel as db_create_murmel,
    get_murmel_by_id,
    get_murmel_by_user_id as db_get_murmel_by_user_id,
    get_murmel_radar as db_get_murmel_radar,
    get_user_by_id,
    set_murmel_chat_room,
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

    print(murmel)

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

    murmel = db_get_murmel_radar(conn, auth.username())

    return (jsonify(murmel), 200)


@app.route("/murmel/<murmel_id>/chat_room", methods=["POST"])
def start_chat(murmel_id):
    body = request.get_json(force=True)
    chat_room_id = body["room_id"]

    murmel = get_murmel_by_id(conn, murmel_id)

    if murmel is None:
        abort(404)

    if murmel["chat_room_id"] is None or murmel["chat_room_id"] == "":
        set_murmel_chat_room(conn, murmel["id"], chat_room_id)
    else:
        abort(409)

    return ("", 200)


@app.route("/murmel/<murmel_id>/chat_room/<room_id>", methods=["DELETE"])
@auth.login_required
def delete_chat(murmel_id, room_id):
    murmel = get_murmel_by_id(conn, murmel_id)

    if murmel is None:
        abort(404)

    if murmel["chat_room_id"] is None or murmel["chat_room_id"] == "":
        return ("", 200)

    if murmel["chat_room_id"] != room_id:
        abort(404)

    set_murmel_chat_room(conn, murmel["id"], None)

    return ("", 200)


@app.route("/test", methods=["GET"])
@auth.login_required
def test():
    return (auth.username(), 200)
