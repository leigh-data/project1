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