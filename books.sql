CREATE TABLE book (
    id serial PRIMARY KEY,
    isbn CHAR (14),
    title VARCHAR(50),
    author VARCHAR(50),
    year INTEGER
);