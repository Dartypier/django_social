# Django Social

This is a small social network written in [Django web framework](https://www.djangoproject.com/), for a UNI Project. 
To ease the development and deployment process, docker compose files are configured.

[See the demo here.](http://ds.zecchi.co)

![Django Social Screenshot](/readme.assets/sc1.png)

## Functions

- User Creation
- Profile Edit
- User Profiles
- Password Change by Email
- Post creation
- Likes
- Comments
- Users follow/unfollow

## Architecture

- Django
- PostgreSQL
- SMTP proxy for email reset

## How to edit the project

The project is self contained with docker. There is by default a docker compose file called `docker-compose.yml` that contains all the containers and volumes for the development.
This environment contains:
- web (contains django web app)
- db (contains postgres DBMS), optional if you want to use SQLITE

You need to install [docker engine](https://docs.docker.com/engine/install/) and [docker compose](https://docs.docker.com/compose/install/) to use docker. 

> 🚩: is not necessary to use docker for development. You can build by yourself you environment by installing all the dependencies listed in `requirements.txt` if you want. That's it.

First of all you need to clone this repo:

```
git clone https://github.com/Dartypier/django_social/
```

It is important to define the envs files. This project use three env files (they must be located in the root of the project):
- `env.db`: used to define postgres variables (if you want you can switch back to SQLITE used by default by django, thus not use Postgres, but you must update the `django_social/setting.py` file)
- `env.dev`: used to define django variables for development 

`env.db`
Here you have to define postgres database used by django, the user and his password. Change the fields `[]` respectively:

```
POSTGRES_DB=[]
POSTGRES_USER=[]
POSTGRES_PASSWORD=[]
```

`env.dev` Here you have all the env variables used by django. Note that the following fields must match the values of the .env.db file:

- `SQL_DATABASE=[]`
- `SQL_USER=[]`
- `SQL_PASSWORD=[]`

Change the fields `[]` respectively:
```
SECRET_KEY=[]
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
DEFAULT_FROM_EMAIL=[]
EMAIL_HOST=[]
EMAIL_HOST_USER=[]
EMAIL_HOST_PASSWORD=[]
EMAIL_PORT=[]
EMAIL_USE_TLS=False
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=[]
SQL_USER=[]
SQL_PASSWORD=[]
SQL_HOST=db
```

Now you can run docker:

```
docker compose -f docker-compose.yml up -d --build 
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py makemigrations accounts posts
docker compose exec web python manage.py migrate
```

By default the web service is active on port 8000. 

## How to Deploy

The deploy is made with docker to minimize the deployment problems. You need to install [docker engine](https://docs.docker.com/engine/install/) and [docker compose](https://docs.docker.com/compose/install/). 
The docker compose file is `docker-compose.prod.yml`

First of all you need to clone this repo:

```
git clone https://github.com/Dartypier/django_social/
```

It is important to define the envs files. This project use three env files (they must be located in the root of the project):
- `env.db`: used to define postgres variables
- `env.prod`: used to define django variables

`env.db`
Here you have to define postgres database used by django, the user and his password. Change the fields `[]` respectively:

```
POSTGRES_DB=[]
POSTGRES_USER=[]
POSTGRES_PASSWORD=[]
```

`env.prod`
Here you have to define the django variables.  Note that the following fields must match the values of the .env.db file:

- `SQL_DATABASE=[]`
- `SQL_USER=[]`
- `SQL_PASSWORD=[]`

Change the fields `[]` respectively:

```
SECRET_KEY=[]
EMAIL_BACKEND=[]
DEFAULT_FROM_EMAIL=[]
EMAIL_HOST=[]
EMAIL_HOST_USER=[]
EMAIL_HOST_PASSWORD=[]
EMAIL_PORT=[]
EMAIL_USE_TLS=False
DEBUG=False
ALLOWED_HOSTS=[]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=[]
SQL_USER=[]
SQL_PASSWORD=[]
SQL_HOST=db
SQL_PORT=5432
```

Now you can do the build:

```
docker compose -f docker-compose.prod.yml build 
```

For the first run you need to initialize the DB and collect all the static files:

```
docker compose -f docker-compose.prod.yml up -d 
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py makemigrations accounts posts
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic
```

Now you have initialized the containers. Shut down the containers and restart the environment:

```
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d 
```

Now you can access the web app (by default on port 8000): http://[domain/IP]:8000
