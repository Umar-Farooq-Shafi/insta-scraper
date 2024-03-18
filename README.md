# Installation

```
python3 -m venv django-env
```

## activate virtual env

```
source django-env/bin/activate
```

## Install all dependencies:

```
pip3 install -r requirements.txt
```

## Next, navigate into the newly created project folder. Then, start a new Django app. We will also run migrations and start up the server:

```
cd api
python3 manage.py migrate
python3 manage.py runserver
```

## start tailwind complier

```
manage.py tailwind start
```

## build the tailwind for prod

```
manage.py tailwind build
```
