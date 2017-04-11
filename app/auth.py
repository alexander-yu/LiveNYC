import db


def authenticate(connection, session):
    username = session.get('username')
    if username:
        user = db.get_user(connection, username)
        if user is None:
            session.pop('username', None)

        return user

    else:
        return None
