CREATE TABLE books (
    id serial PRIMARY KEY,
    isbn VARCHAR (16) UNIQUE,
    title VARCHAR(50),
    author VARCHAR(50),
    year INTEGER
);