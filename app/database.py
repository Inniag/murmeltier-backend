from sqlalchemy import create_engine, select
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
import hashlib
import datetime

# get these from environment
username = "postgres"
password = ""

metadata = MetaData()
users = Table(
    "users",
    metadata,
    Column("id", String, primary_key=True, nullable=False),
    Column("password", String),
    Column("last_login", DateTime),
)


def connect():
    print("connecting")
    connection_string = f"postgresql://{username}:{password}@murmeltier-dev.cesmdqo7uee8.eu-central-1.rds.amazonaws.com"
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
