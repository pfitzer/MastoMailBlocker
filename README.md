# MastoMailBlocker

[![Django CI](https://github.com/pfitzer/MastoMailBlocker/actions/workflows/django.yml/badge.svg)](https://github.com/pfitzer/MastoMailBlocker/actions/workflows/django.yml)

### This project is under heavy construction

This is a Django application where Mastodon admins can join their instances and let automatically
push disposable email domains from https://github.com/disposable-email-domains/disposable-email-domains to their blocked
email domains using Mastodons REST-API.

run with docker
---------------

You need a .env file with some variables in it. Take a look at .env.example. The docker-compose.yml ist just an example, more or less.
If you want to run it in production, take a look at the commented parts of the letsencrypt container and adjust it to your needs.

If you have your own nginx-proxy running, commend the proxy part.

```
# clone the project
git clone https://github.com/pfitzer/MastoMailBlocker.git

cd MastoMailBlocker
# generate the .env file from .env.example
cp .env.example .env

# at first time or after code update
docker-compose up -d --build
```

development
-----------

If you want to contribute, feel free to do so. Help is always welcome.

```
# clone the project
git clone https://github.com/pfitzer/MastoMailBlocker.git

cd MastoMailBlocker
# create a virtual environment
python -m venv -venv

# install requirements
pip install -r requirements.txt

# run the management commands
python manage.py migrate
python manage.py createsuperuser
python manage.py createcachetable
python manage.py import_domains
python manage.py loaddata app/fixtures/db.json
python manage.py collectstatic
python manage.py generate_schedules

# start the server
python manage.py runserver

# if your want to test the queue and scheduler tasks
python manage.py qcluster
```

[![buy me a coffe](https://cdn.buymeacoffee.com/buttons/lato-orange.png)](https://www.buymeacoffee.com/pfitzer)

