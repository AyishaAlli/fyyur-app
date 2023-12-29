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

## Tech Stack (Dependencies)

### 1. Backend Dependencies

Tech stack includes the following:

- **virtualenv** as a tool to create isolated Python environments
- **SQLAlchemy ORM** to be our ORM library of choice
- **PostgreSQL** as our database of choice
- **Python3** and **Flask** as our server language and server framework
- **Flask-Migrate** for creating and running schema migrations
  You can download and install the dependencies mentioned above using `pip` as:

```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
```

### 2. Frontend Dependencies

You must have the **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend. Bootstrap can only be installed by Node Package Manager (NPM). Therefore, if not already, download and install the [Node.js](https://nodejs.org/en/download/). Windows users must run the executable as an Administrator, and restart the computer after installation. After successfully installing the Node, verify the installation as shown below.

```
node -v
npm -v
```

Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend:

```
npm init -y
npm install bootstrap@3
```

## Development Setup

**Download the project starter code locally**

```
git clone https://github.com/AyishaAlli/fyyur-app.git
```

1. **Initialize and activate a virtualenv using:** (For this project to run, you must be using Python3.9 or below)

```python
python -m virtualenv env
source env/bin/activate
```

> **Note**
>
> - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:

```python
source env/Scripts/activate
```

2. **Install the dependencies:**

```python
pip3 install -r requirements.txt
```

3. **Run the development server:**

```python
export FLASK_APP=myapp
export FLASK_ENV=development
python3 app.py
```

4. **Verify on the Browser**<br>
   Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000)

## Acknowledgements

Special thanks to [Udacity](https://www.udacity.com/) for providing this project as part of the Nanodegree. I have learnt so much building it out in such a short space of time and really enjoyed it.
