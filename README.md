# The platform for organizing chess tournaments

This web application is an user-friendly solution for chess enthusiasts. It offers seamless registration on the platform, allowing users to easily create and manage chess tournaments. The platform also features a commenting system for users to engage in discussions and share insights about the tournaments. Whether you are a player or organizer this platform is designed to enhance your chess experience and foster a vibrant community.

## Install requirement project's packages

```commandline
pip install -r requirements.txt
```

## Create file .env

Go to folder Chess_Project, create file .env and write there your DB_NAME, DB_USER, DB_PASSWORD and SECRET_KEY.

## Run project

Go to the folder with manage.py file, run library
```commandline
python manage.py migrate 
```

```commandline
python manage.py runserver
```
