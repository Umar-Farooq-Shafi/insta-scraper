## Install all dependencies:

```
python3 -m pip install -r requirements.txt
```

## start redis server
```
docker composer up
```


## activate virtual env

```
source django-env/bin/activate
```

## Open Jupyter notebook
```
jupyter notebook
```

## Next, navigate into the newly created project folder. Then, start a new Django app. We will also run migrations and start up the server:

```
cd src
celery -A api worker --beat -l INFO
python3 manage.py migrate
python3 manage.py runserver
```

## start tailwind complier

```
python3 manage.py tailwind start
```

## build the tailwind for prod

```
python3 manage.py tailwind build
```
