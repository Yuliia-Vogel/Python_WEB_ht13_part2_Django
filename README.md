# Python_WEB_ht10
App for adding quotes to the web-page. App created with Django 5.1

1) Install Postgres DB, create an account at MongoDB and prepare database cluster at MongoDB.
2) Create venv: python -m venv venv
3) pip install pymongo sqlalchemy psycopg2 python-dotenv django==5.1
4) Create "hw10_project/.env" file with your credentials for your MongoDB and your Postgres DB. You 
can see a list of necessary credentials in .env.example file.
5) Create migrations: python manage.py makemigrations
6) Run migrations: python manage.py migrate
7) Run script for data migration: python migrate_data.py
8) Check if all data were transferred from MongoDB to PostgreSQL.
9) Run server for work with service: python manage.py runserver

---> finally you can use ready service at localhost server http://127.0.0.1:8000/quotes/
To register (or login): press button "Register" (or "Login") in right top corner of the screen.
Nesessary to register: username, email, password. Necessary to login: username, password.
"Add quote" and "Add tag" buttons and options are available for users after login only.


There is no necessity to create a superadmin due to fact that the service contains a separate app for users creation. Users can be registered independently from each other.


