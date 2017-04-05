CREATE TABLE Users (
    username    VARCHAR(20),
    password    VARCHAR(20),
    email       VARCHAR(254),
    UNIQUE (email),
    PRIMARY KEY (username)
)

CREATE TABLE Neighborhood (
    name        VARCHAR(30),
    population  INTEGER,
    mean_income REAL,
    PRIMARY KEY (name)
)

CREATE TABLE Borough (
    name                VARCHAR(20),
    year_incorporated   INTEGER,
    county_name         VARCHAR(20),
    PRIMARY KEY (name)
)

CREATE TABLE Place_of_Interest (
    id      INTEGER,
    name    VARCHAR(50),
    PRIMARY KEY (id)
)

CREATE TABLE Park (
    id              INTEGER,
    acres           REAL,
    is_public       BOOLEAN,
    dogs_allowed    BOOLEAN,
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES Place_of_Interest
        ON DELETE CASCADE
)

CREATE TABLE Restaurant (
    id              INTEGER,
    restaurant_type VARCHAR(50),
    cost_rating     INTEGER,
    alcohol_served  BOOLEAN,
    PRIMARY KEY (id)
    FOREIGN KEY (id) REFERENCES Place_of_Interest
        ON DELETE CASCADE
)

CREATE TABLE School (
    id          INTEGER,
    mean_cost   REAL,
    school_type VARCHAR(30),
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES Place_of_Interest,
        ON DELETE CASCADE
)

CREATE TABLE Subway (
    name        VARCHAR(30),
    color       CHAR(7),
    is_express  BOOLEAN,
    PRIMARY KEY (name)
)

CREATE TABLE Review (
    time_written    TIMESTAMP,
    content         VARCHAR(1000),
    rating          REAL,
    username        VARCHAR(20),
    PRIMARY KEY (time_written, username),
    FOREIGN KEY (username) REFERENCES User
        ON DELETE CASCADE
)

CREATE TABLE Reviewed_By (
    username        VARCHAR(20),
    time_written    TIMESTAMP,
    neighborhood    VARCHAR(30),
    PRIMARY KEY (username, time_written, neighborhood)
    FOREIGN KEY (time_written, username) REFERENCES Review
        ON DELETE CASCADE,
    FOREIGN KEY (neighborhood) REFERENCES Neighborhood (name)
        ON DELETE CASCADE
)

CREATE TABLE Favorites (
    username        VARCHAR(20),
    neighborhood    VARCHAR(30),
    PRIMARY KEY (username, neighborhood),
    FOREIGN KEY (username) REFERENCES User
        ON DELETE CASCADE,
    FOREIGN KEY (neighborhood) REFERENCES Neighborhood (name)
        ON DELETE CASCADE
)

CREATE TABLE Serves (
    subway          VARCHAR(30),
    neighborhood    VARCHAR(30),
    PRIMARY KEY (subway, neighborhood),
    FOREIGN KEY (subway) REFERENCES Subway (name)
        ON DELETE CASCADE,
    FOREIGN KEY (neighborhood) REFERENCES Neighborhood (name)
        ON DELETE CASCADE
)

CREATE TABLE Placed_In (
    place_id        INTEGER,
    neighborhood    VARCHAR(30) NOT NULL,
    PRIMARY KEY (place_id),
    FOREIGN KEY (place_id) REFERENCES Place_of_Interest (id)
        ON DELETE CASCADE,
    FOREIGN KEY (neighborhood) REFERENCES Neighborhood (name)
        ON DELETE CASCADE
)

CREATE TABLE Located_In (
    neighborhood    VARCHAR(30),
    borough         VARCHAR(20) NOT NULL,
    PRIMARY KEY (neighborhood),
    FOREIGN KEY (neighborhood) REFERENCES Neighborhood (name)
        ON DELETE CASCADE
    FOREIGN KEY (borough) REFERENCES Borough (name)
        ON DELETE CASCADE
)
