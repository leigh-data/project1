CREATE TABLE books (
    id serial PRIMARY KEY,
    isbn VARCHAR (16) UNIQUE,
    title VARCHAR(50),
    author VARCHAR(50),
    year INTEGER,
    tsv tsvector
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

CREATE OR REPLACE FUNCTION search_params_trigger() RETURNS trigger as $$
    begin
        new.tsv := to_tsvector(
            'pg_catalog.english',
            substring(
                new.isbn || ' ' ||
                new.title ||' ' ||
                new.author,
                1, 500000
                )
            );
        return new;
    end
$$ LANGUAGE plpgsql;

CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
ON books FOR EACH ROW EXECUTE PROCEDURE search_params_trigger();

CREATE INDEX ix_books_tsv ON books USING GIN(tsv);