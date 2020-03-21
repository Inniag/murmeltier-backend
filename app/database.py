from sqlalchemy import create_engine, select
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
import hashlib
import datetime
import os

# get these from environment
MURMEL_POSTGRES_USER = os.getenv("MURMEL_POSTGRES_USER")
MURMEL_POSTGRES_PASSWORD = os.getenv("MURMEL_POSTGRES_PASSWORD")
MURMEL_POSTGRES_HOST = os.getenv("MURMEL_POSTGRES_HOST")


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
    Column("created_at", DateTime),
)


def connect():
    print("connecting")
    connection_string = f"postgresql://{MURMEL_POSTGRES_USER}:{MURMEL_POSTGRES_PASSWORD}@{MURMEL_POSTGRES_HOST}"

    print(connection_string)

    engine = create_engine(connection_string, echo=True)
    conn = engine.connect()
    print("OK")

    create_tables(engine)

    return conn


def create_tables(engine):
    metadata.create_all(engine)


def get_user_by_id(conn, id):
    s = select([users], users.c.id == id)
    result = conn.execute(s)
    row = result.fetchone()
    print(row)
    result.close()


def create_user(conn):
    dk = hashlib.pbkdf2_hmac("sha256", uuid.uuid4().bytes, b"salt", 100000)
    password = dk.hex()
    id = str(uuid.uuid4())

    ins = users.insert().values(
        id=id, password=password, last_login=datetime.datetime.utcnow()
    )
    conn.execute(ins)

    return (id, password)


def create_murmel(conn, params):

    id = str(uuid.uuid4())

    # TODO add user UD!
    ins = murmel.insert().values(
        id=id,
        mood_value=params["mood_value"],
        hashtag=params["hashtag"],
        created_at=datetime.datetime.utcnow(),
    )
    conn.execute(ins)

    return None


def get_murmel_by_user_id(conn, params):

    # TODO should select by user ID
    s = select([murmel])

    result = conn.execute(s)
    # TODO select latest/current rather than just fetchone
    result = result.fetchone()

    return result


def get_murmel_radar(conn, params):

    # TODO exclude current user
    s = select([murmel])

    result = conn.execute(s)

    print(result)

    return None
