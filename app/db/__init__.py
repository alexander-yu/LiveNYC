USER_FIELDS = ['username', 'password', 'email']


def authenticate_user(cursor, username, password):
    query = """SELECT *
               FROM Users U
               WHERE U.username=%s AND
                    U.password=%s
               ;"""
    cursor.execute(query, [username, password])
    users = cursor.fetchall()
    return len(users) != 0


def get_user(cursor, username):
    query = """SELECT *
               FROM Users U
               WHERE U.username=%s
               ;"""
    cursor.execute(query, [username])
    user_data = cursor.fetchone()

    if user_data is None:
        return None
    else:
        return dict(zip(USER_FIELDS, user_data))


def add_user(cursor, username, password, email):
    query = """INSERT INTO
               Users (username, password, email)
               VALUES (%s, %s, %s)
               ;"""
    cursor.execute(query, [username, password, email])
