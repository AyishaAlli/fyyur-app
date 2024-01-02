# Fyyur

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

Your job is to build out the data models to power the API endpoints for the Fyyur site by connecting to a PostgreSQL database for storing, querying, and creating information about artists and venues on Fyyur.

## Features

A user can:

- successfully execute a Search that queries the database.
  - You can search for Name, City or State for both Artists and Venues
- view a Venues Page with venue information from the database.
- view an Artist Page with artist information from the database.
- create new venue listing via the New Venue Page.
- create new artist listing via the New Artist Page.
- Create a new show with the ID of an existing Artist and Venue.
- cannot submit an invalid form submission (e.g. using an invalid State enum, or with required fields missing; missing city, missing name, or missing genre is not required).
- Delete either an artist or venue on their description page.
  - If a show belongs to the Artist/Venue, that will also be deleted.

## Tech Stack (Dependencies)

### 1. Backend Dependencies

Tech stack includes the following:

- **virtualenv** as a tool to create isolated Python environments
- **SQLAlchemy ORM** to be our ORM library of choice
- **PostgreSQL** as our database of choice
- **Python3** and **Flask** as our server language and server framework
- **Flask-Migrate** for creating and running schema migrations

### 2. Frontend Dependencies

- **HTML**
- **CSS**
- **JavaScript**

## Development Setup

1. **If you havent already, Download the project locally**

```bash
git clone https://github.com/AyishaAlli/fyyur-app.git
cd fyyur-app
```

2. **Install frontend dependencies**

```bash
npm install
```

3. **Initialize and activate a virtualenv using:** (For this project to run, you must be using Python3.9, The below command will only work if you have this version already installed on your PC)

```bash
python3.9 -m venv env
source env/bin/activate
```

> **Note**
>
> - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:

```python
source env/Scripts/activate
```

4. **Install the dependencies:**

```python
pip3 install -r requirements.txt
```

5. **Create Database:**

Please make sure you have postgreSQL installed
To download please see [https://www.postgresql.org/download/](https://www.postgresql.org/download/)

First, start your PostgreSQL database server by running:

```bash
sudo service postgresql start

OR

brew services start postgresql
```

6. **create the database:**

```bash
createdb fyyur
```

Add your details to line 14 in the _config.py_ file (Replace USERNAME with your postgres user and add a password if you have one. if you dont have a password please just remove the word 'PASSWORD'):

```bash
SQLALCHEMY_DATABASE_URI = 'postgresql://USERNAME:PASSWORD@localhost:5432/fyyur' # e.g. postgresql://ayishaalli:123@localhost:5432/fyyur
```

7. **Make Migrations:**

```bash
flask db migrate # after running this it may say 'ERROR [flask_migrate] Error: Target database is not up to date.' Please ignore and move on to the next command.
flask db upgrade
```

1. **Run the development server:**

```bash
python3 app.py
```

9. **Verify on the Browser**<br>
   Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000)

## Acknowledgements

Special thanks to [Udacity](https://www.udacity.com/) for providing this project as part of the Nanodegree. I have learnt so much building it out in such a short space of time and really enjoyed it.
