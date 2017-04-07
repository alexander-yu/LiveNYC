def authenticate_user(connection, username, password):
    query = """SELECT COUNT (*)
               FROM Users U
               WHERE U.username=%s AND
                    U.password=%s
               ;"""
    result = connection.execute(query, [username, password])
    user_count = result.first()
    return user_count > 0


def get_user(connection, username):
    query = """SELECT U.username
               FROM Users U
               WHERE U.username=%s
               ;"""
    result = connection.execute(query, [username])
    return result.first()


def add_user(connection, username, password, email):
    query = """INSERT INTO
               Users (username, password, email)
               VALUES (%s, %s, %s)
               ;"""
    connection.execute(query, [username, password, email])


def get_reviews_by_user(connection, username):
    query = """SELECT R1.time_written, R1.content, R1.rating, L.neighborhood,
                   L.borough
               FROM Review R1 INNER JOIN Reviewed_By R2
                       ON R1.username=%s USING (username, time_written)
                   INNER JOIN Located_In L USING (neighborhood)
               ORDER BY R1.time_written
               ;"""
    result = connection.execute(query, [username])
    return result.fetchall()


def get_favorites(connection, username):
    query = """SELECT L.neighborhood, L.borough
               FROM Favorites F INNER JOIN Located_In L
                   ON F.username=%s USING (neighborhood)
               ;"""
    result = connection.execute(query, [username])
    return result.fetchall()


def add_favorite(connection, username, neighborhood):
    query = """INSERT INTO
               Favorites (username, neighborhood)
               VALUES (%s, %s)
               ;"""
    connection.execute(query, [username, neighborhood])


def add_review(connection, neighborhood, username, review_data):
    rating, time_written, content = review_data['rating'], \
        review_data['time_written'], review_data['content']
    query = """INSERT INTO
               Review (time_written, content, rating, username)
               VALUES (%s, %s, %s, %s)
               ;"""
    connection.execute(query, [time_written, content, rating, username])

    query = """INSERT INTO
               Reviewed_By (username, time_written, neighborhood)
               VALUES (%s, %s, %s)
               ;"""
    connection.execute(query, [username, time_written, neighborhood])


def get_borough(connection, borough):
    query = """SELECT B.year_incorporated, B.county_name
               FROM Borough B
               WHERE B.name=%s
               ;"""
    result = connection.execute(query, [borough])
    return result.first()


def get_neighborhoods(connection, borough):
    query = """SELECT L.neighborhood
               FROM Located_In L
               WHERE L.borough=%s
               ;"""
    result = connection.execute(query, [borough])
    return result.fetchall()


def get_neighborhood(connection, neighborhood):
    query = """SELECT N.population, N.mean_income, S1.subway, S2.color,
                   S2.is_express
               FROM Neighborhood N INNER JOIN Serves S1
                       ON N.name=%s AND N.name=S1.neighborhood
                   INNER JOIN Subway S2
                       ON S2.name=S1.subway
               ;"""
    result = connection.execute(query, [neighborhood])
    return result.first()


def get_parks(connection, neighborhood):
    query = """SELECT P1.place_id, P2.name, P3.acres, P3.is_public,
                   P3.dogs_allowed
               FROM Placed_In P1 INNER JOIN Place_Of_Interest P2
                       ON P1.place_id=P2.id AND P1.neighborhood=%s
                   INNER JOIN Park P3
                       USING (id)
               ;"""
    result = connection.execute(query, [neighborhood])
    return result.fetchall()


def get_schools(connection, neighborhood):
    query = """SELECT P1.place_id, P2.name, S.mean_cost, S.school_type
               FROM Placed_In P1 INNER JOIN Place_Of_Interest P2
                       ON P1.place_id=P2.id AND P1.neighborhood=%s
                   INNER JOIN School S
                       USING (id)
               ;"""
    result = connection.execute(query, [neighborhood])
    return result.fetchall()


def get_restaurants(connection, neighborhood):
    query = """SELECT P1.place_id, P2.name, R.restaurant_type, R.cost_rating,
                   R.alcohol_served
               FROM Placed_In P1 INNER JOIN Place_Of_Interest P2
                       ON P1.place_id=P2.id AND P1.neighborhood=%s
                   INNER JOIN Restaurant R
                       USING (id)
               ;"""
    result = connection.execute(query, [neighborhood])
    return result.fetchall()
