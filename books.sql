CREATE TABLE books (
    id serial PRIMARY KEY,
    isbn VARCHAR (16) UNIQUE,
    title VARCHAR(50),
    author VARCHAR(50),
    year INTEGER
);

CREATE TABLE users (
    id serial PRIMARY KEY,
    username VARCHAR(25) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE ratings (
    id serial PRIMARY KEY,
    book_id INTEGER REFERENCES books(id) NOT NULL,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    rating SMALLINT DEFAULT 5,
    comment TEXT,
    UNIQUE(book_id, user_id)
);