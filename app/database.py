from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Date, MetaData, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
import hashlib

# get these from environment
username = "postgres"
password = ""

metadata = MetaData()
users = Table(
    "users",
    metadata,
    Column("id", UUID, primary_key=True, nullable=False),
    Column("password", String),
    Column("last_login", Date),
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
    s = select([users])
    result = conn.execute(s)
    row = result.fetchone()
    print(row)
    result.close()


def create_user(conn):
    dk = hashlib.pbkdf2_hmac("sha256", b"password", b"salt", 100000)
    ins = users.insert().values(id=uuid.uuid4(), password=dk.hex(), last_login=0)
    print(ins)
    res = conn.execute(ins)
    print(res)
