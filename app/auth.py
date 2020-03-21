from .database import get_user_by_id, hash_password


def login(conn, id, password):
    if password is None or password == "":
        return False

    user = get_user_by_id(conn, id)

    if user is None:
        return False

    password_hash = hash_password(password)

    print(user)
    print(password_hash)

    if user["password"] == password_hash:
        return True

    return False
