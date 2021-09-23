[![Build Status](https://app.travis-ci.com/Paccy10/activo-api.svg?token=WAzzRJkVxdCSbeHdvear&branch=main)](https://app.travis-ci.com/Paccy10/activo-api) [![Test Coverage](https://api.codeclimate.com/v1/badges/000696a2b1aecb6240ed/test_coverage)](https://codeclimate.com/github/Paccy10/activo-api/test_coverage) [![Maintainability](https://api.codeclimate.com/v1/badges/000696a2b1aecb6240ed/maintainability)](https://codeclimate.com/github/Paccy10/activo-api/maintainability)

# Activo API

Asset management is defined as the systematic and coordinated activities and practices through which an organization optimally and sustainably manages its assets and asset systems, their associated performance, risks and expenditures over their life cycles to achieve its organizational strategic plan where an
organizational strategic plan is defined as the overall long-term plan for the organization that is derived from, and embodies, its vision, mission, values, business policies, stakeholder requirements, objectives and the management of its risks.

## Getting started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

```
- Python 3.9.4
- Docker
```

## Installation and setup

- Clone the repo

```
git clone https://github.com/Paccy10/activo-api.git
```

- Download python

```
https://www.python.org/downloads/
```

- Create the virtual environment

```
python -m venv venv
```

- Activate virtual environment

  - MacOS and Linux

  ```
  source venv/bin/activate
  ```

  - Windows

  ```
  .\venv\Scripts\activate
  ```

- Install dependencies

```
pip install -r requirements.txt
```

- Make a copy of the .env.sample file and rename it to .env and update the variables accordingly

- Apply migrations

```
python manage.py migrate
```

- When you make changes to the database models, run migrations as follows

  - Make new migrations

  ```
  python manage.py makemigrations
  ```

  - Run migrations

  ```
  python manage.py migrate
  ```

## Running

- Running app

```
python manage.py runserver
```

- Running tests

```
pytest
```

## Use Docker

Make sure you have installed Docker and Docker daemon on your computer

- Build and run the app

```
docker-compose -f docker-compose-dev.yml up --build -d --remove-orphans
```

- Run the app

```
docker-compose -f docker-compose-dev.yml up -d
```

- Stop the app

```
docker-compose -f docker-compose-dev.yml down
```

- View logs

```
docker-compose -f docker-compose-dev.yml logs
```

- Running migrations

```
docker-compose -f docker-compose-dev.yml exec api python manage.py migrate
```

- Make migrations

```
docker-compose -f docker-compose-dev.yml exec api python manage.py makemigrations
```

- Create a super user

```
docker-compose -f docker-compose-dev.yml exec api python manage.py createsuperuser
```

- Bring down containers and delete volumes

```
docker-compose -f docker-compose-dev.yml down -v
```

- Running tests

```
docker-compose -f docker-compose-dev.yml exec api pytest
```
