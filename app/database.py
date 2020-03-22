from sqlalchemy import create_engine, select, func
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
import hashlib
import datetime
import os
import random


# get these from environment
MURMEL_POSTGRES_USER = os.getenv("MURMEL_POSTGRES_USER")
MURMEL_POSTGRES_PASSWORD = os.getenv("MURMEL_POSTGRES_PASSWORD")
MURMEL_POSTGRES_HOST = os.getenv("MURMEL_POSTGRES_HOST")
salt = "9236adc052fa3328316aa0540d16365221194159d1a49cb0f4172acf573ed02f"

metadata = MetaData()


users = Table(
    "users",
    metadata,
    Column("id", String, primary_key=True, nullable=False),
    Column("password", String),
    Column("last_login", DateTime),
)


murmel = Table(
    "murmel",
    metadata,
    Column("id", String, primary_key=True, nullable=False),
    Column("mood_value", Integer),
    Column("hashtag", String),
    Column("username", String),
    Column("created_at", DateTime),
    Column("chat_room_id", String),
)


def connect():
    print("connecting")
    connection_string = f"postgresql://{MURMEL_POSTGRES_USER}:{MURMEL_POSTGRES_PASSWORD}@{MURMEL_POSTGRES_HOST}"

    print(connection_string)

    engine = create_engine(connection_string, echo=True)
    conn = engine.connect()
    print("OK")

    # murmel.drop(engine)

    create_tables(engine)

    return conn


def create_tables(engine):
    metadata.create_all(engine)


def get_user_by_id(conn, id):
    s = select([users], users.c.id == id)
    result = conn.execute(s)
    row = result.fetchone()
    result.close()
    return row


def create_user(conn):
    plaintext_password = str(uuid.uuid4())
    hashed_password = hash_password(plaintext_password)
    id = str(uuid.uuid4())

    ins = users.insert().values(
        id=id, password=hashed_password, last_login=datetime.datetime.utcnow()
    )
    conn.execute(ins)

    return (id, plaintext_password)


def create_murmel(conn, mood_value, hashtag, username):

    # create murmel UUID:
    id = str(uuid.uuid4())

    ins = murmel.insert().values(
        id=id,
        mood_value=mood_value,
        hashtag=hashtag,
        username=username,
        created_at=datetime.datetime.utcnow(),
    )
    conn.execute(ins)

    return id


def get_murmel_by_id(conn, id):
    s = select([murmel], murmel.c.id == id)

    result = conn.execute(s)
    result = result.fetchone()

    return result


def get_murmel_by_user_id(conn, username):
    s = (
        select([murmel], murmel.c.username == username)
        .order_by(murmel.c.created_at.desc())
        .limit(1)
    )

    result = conn.execute(s)
    result = result.fetchone()

    return result


def set_murmel_chat_room(conn, murmel_id, room_id):
    stmt = murmel.update().where(murmel.c.id == murmel_id).values(chat_room_id=room_id)
    conn.execute(stmt)


def get_murmel_radar(conn, username):

    # just get large number of murmels, hoping there are distinct users
    # FIXME this will NOT scale to many users!
    s = (
        select([murmel])
        .where(murmel.c.username != username)
        .order_by(murmel.c.created_at.desc())
        .limit(1000)
    )

    result = conn.execute(s).fetchall()

    # collect distinct users's murmel
    res = []
    usernames = {}
    for r in result:

        d = {
            "id": r["id"],
            "mood_value": r["mood_value"],
            "hashtag": r["hashtag"],
            "username": r["username"],
            "created_at": r["created_at"],
        }

        # append only if username was not encountered before
        if r["username"] not in usernames.keys():

            res.append(d)

            usernames[r["username"]] = r["username"]

    # randomise user order
    random.shuffle(res)

    # return at most five murmels
    return res[0 : (min(len(res), 5))]


def hash_password(plaintext_password):
    salted_password = plaintext_password + salt
    return hashlib.sha512(salted_password.encode()).hexdigest()
