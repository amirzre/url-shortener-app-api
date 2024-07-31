# UrlShortener

## project setup

1- compelete cookiecutter workflow (recommendation: leave project_slug empty) and go inside the project
```
cd UrlShortener
```

2- SetUp venv
```
python3 -m venv venv
source venv/bin/activate
```

3- install Dependencies
```
pip install -r requirements.txt
```

4- create your env
```
cp .env.example .env
```

5- Create tables
```
python manage.py migrate
```

6- spin off docker compose
```
docker compose -f docker-compose.yml up -d
```

7- run the project
```
python manage.py runserver
```