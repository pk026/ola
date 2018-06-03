# ola
Problem stmt:
At random times a ride request comes from users.
The request is then broadcast to all drivers.
Whoever picks up first gets to service them.

# stacks used
django, djangorestframework, celery, postgresql, redis

# pre-requisite: install postgresql and redis on machine

# project setup
1. git clone https://github.com/pk026/ola.git
2. create a virtualenv using: virtualenv venv (install virtualenv on your machine if not already installed)
3. activate environment using: source venv/bin/activate
4. upgrade pip using: pip install --upgrade pip
curl https://bootstrap.pypa.io/get-pip.py | python
5. install requirements using: pip install -r requirements.txt
6. make database setting proper: create a database with name:ola, user:pramod, password: postgres
7. install redis and run it on machine
or you can create database with your own set of parameters and update them into settings.py: DATABASES
7. create database schema using: python manage.py migrate
8. create a superuser: python manage.py createsuperuser
