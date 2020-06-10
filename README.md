# Project 1

Web Programming with Python and JavaScript

Website: [heroku](https://classic-book-report.herokuapp.com)

Screencast: [Youtube](https://youtu.be/-GZP9YNyXZQ)

---

## Classic Book Report

This Flask web application allows users to register and log in using username and password to write reviews of 5000 classic books.
The books are fed into a PostgreSQL database via a script that handles csv files. The index page contains, for the logged-in user, a search form to search the database based on title,author, and ISBN number. If the search comes up with more than 5 books, they are paginated on the search page. The links lead to a detail page for a specific book. The title, author, year, and ISBN are displayed in a Bootstrap 4 Card component. In addition, in other Card components, are Goodreads total reviews and average review data and unpaginated reviews from individual users. Book data (author, title, year, ISBN, average review, and total reviews) can be retrieved in JSON format with the `/api/<isbn>` url. Note that this data is in-app and does not come from Goodreads.

## / Directory

This directory contains the main project directory, as well a files to support serving the application.

### requirements.txt

The Python packages needed for the application to run.

### Procfile

A script used to serve the application on the Heroku cloud platform.

### package.json

An npm file used to compile the **styles.scss** file into the main **static/css/styles.css** files (using the `npm run scss`)

### manage.py

A Flask command-line utility script. `python manage.py run` runs the development server, and `python manage.py shell` runs the application in a REPL.

## import_data.py

A script used to import csv data into the database. It is run with this command in the command-line interface: `python import_data.py books.csv`

## books.sql

The SQL script that builds the tables, indices, and triggers needed to store, alter, and search data.

## books.csv

A csv file containing all of the books in the **Classic Book Report** universe

## test_books.csv

A csv file containing a sampling of books in **books.csv**. Used for development.

## .gitignore

List of files never to be committed to the repository.

## /utils

Folder containing utility items.

### /utils/decorators.py

File containing decorators for the app. There is only one for the application: **login_required**, which protects a view from being accessed by a user who is not authenticated.

## scss/

Folder cantaining needed scss files.

### scss/font-awesome

Folder containing **font-awesome** scss files.

### scss/\_main.scss

File containing custom scss selectors.

### scss/styles.scss

File that contains variables and imports for the main css stylesheet.

## /project

This file contains the blueprints, static files, and templates for **Classic Book Report**

### \_\_init\_\_.py

This init file is not a blank file as in other **\_\_init\_\_\.py** files in the repository. It contains some configuration and contains the **create_app** factory function used to serve the application.

### config.py

Basic configuration settings for the app.

### static/

#### css/

Contains the style sheet (**styles.css**) used for the application.

#### img/

Contains the **hero.jpg** file used for the hero image in the route **/**.

### fonts/

Contains the fonts used to render **font-awesome** icons.

---

## Blueprints

**/project** contains 4 Flask Blueprints: **api**, **auth**, **books**, and **ratings**.
All the directories contain an **\_\_init\_\_.py** file and a **routes.py** file, containing all of the urls and url handlers specific for that Blueprint. **auth** and **ratings** contain a **forms.py** file, which contains **WTForms** used to enter and validate data.

### auth

Handles registration, login, and logout routes.

### books

Handles search, detail, and the home page.

### ratings

Handles rating creation, updating, and deleting.

### api

Handles requests for a book detail in JSON format.

---

## Environment Variables

There are several environment variables needed to make this application work.

**FLASK_ENV** - The environment used to run the application. In production, the environment is **production**; in development, the environment is **development**

**APP_SETTINGS** - The configuration class. In production, the variable is **project.config.ProductionConfig**; in development, the variable is **project.config.DevelopmentConfig**

**DATABASE_URL** - The URL where the database can be accessed. On **Heroku**, the URL is provided by the platform when you provision a database.

**SECRET_KEY** - A key used by the **Flask** framework.

**GOODREADS_KEY** - The API key used to access the **Goodreads** API.

In development, these variables are stored in a file called **.env**, which is never commited to the repository because it contains sensitive data. In production, the settings are set individually in the settings page belonging to the app.

---

## Credits

Hero Image Photo by 🇸🇮[Janko Ferlič](https://unsplash.com/@itfeelslikefilm?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on Unsplash

Patterson, Jordan. "Full Text Searching with Postgres" [forestry.io](https://forestry.io/blog/full-text-searching-with-postgres/) August 1, 2019. May 16, 2019.
