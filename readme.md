# Set up

- Clone the repository, cd into it

```
git clone "https://github.com/mozilla01/sih23-api"
cd sih23_api
```

- Create a virtual environment and activate it

```
py -m venv .env
.env/scripts/activate
```

- Install dependency modules

```
pip install -r requirements.txt
```

- Run migrations to setup database

```
python manage.py migrate
```

- Start the server

```
python manage.py runserver
```

# Managing the database

We are using SQLite3 to store data. All data can be viewed from a web interface by visiting the `/admin` route. But first we need to create a superuser.

```
python manage.py createsuperuser
```

Visit `http://127.0.0.1:8000/admin` and login.

# Endpoints

- User Registration: `/api/register/` for user registeration
- User Login: `/api/login/` for user login. Returns all useful user data.
