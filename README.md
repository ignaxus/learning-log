# Learning Log

A web-based note-taking application built with Django.

Learning Log allows users to organize their study notes by topic, create detailed entries, and access them from any device through a web browser. The project was developed as a learning exercise for Django and can also serve as a reference project for beginners who want to learn web development with Django.

## Features

* User registration and authentication
* Create, edit, and delete topics
* Create, edit, and delete entries
* Personal note organization by topic
* Account ownership and access control
* My Account page with:

  * Username
  * Account age
  * Number of topics
  * Number of entries
  * Latest activity
* Password change functionality
* Log out functionality
* Responsive interface using Bootstrap 5
* Mobile-friendly design

## Technologies Used

* Python
* Django
* Bootstrap 5
* SQLite (default Django database)

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/ignaxus/learning-log.git
cd learning-log
```

### 2. Install dependencies

```bash
pip install django
pip install django-bootstrap5
```

### 3. Apply migrations

```bash
python manage.py migrate
```

### 4. Start the development server

```bash
python manage.py runserver
```

### 5. Open the website

Visit:

```text
http://127.0.0.1:8000/
```

in your web browser.

## Project Purpose

This project was created to learn Django fundamentals, including:

* Models
* Forms
* Authentication
* URL routing
* Templates
* Bootstrap integration
* Database relationships
* CRUD operations

It may also be useful as a reference project for students and developers who are beginning to learn Django.

## License

This project is licensed under the Apache License 2.0.

Copyright (c) 2026 Veratic Labs

