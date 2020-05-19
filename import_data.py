import csv
import sys
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


load_dotenv()

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def get_data_from_csv(filename):
    with open(filename) as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]

        return data


def import_books(books):
    for book in books:
        db.execute(
            "INSERT INTO books (isbn, author, title, year) VALUES (:isbn, :author, :title, :year)",
            book)
        db.commit()
        print(f"DATA ADDED: {book}")


if __name__ == "__main__":
    filename = sys.argv[1]

    books = get_data_from_csv(filename)
    import_books(books)
