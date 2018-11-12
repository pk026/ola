# ola
Problem stmt:
At random times a ride request comes from users.
The request is then broadcast to all drivers.
Whoever picks up first gets to service them.

# project design and explanation
    1. we have two tables trip and car.
    2. I am using Django user for both customer and drivers
    (we may have separate tables for customer and drivers for different information).
    3. Customer can request a trip any time.
        a. search for pickup (there will be suggestion from google this request is handled in anguler)
        b. when user select one of suggested items anguler app does ajax request on api: api/v1/company with lat and long in query set
        c. api (api/v1/company) returns the list of companies (we may have paging in this api but its not implemented yet).
    4. Customer select one of the listed company to check its available slots
        a. anguler does ajax with company_id on api: api/v1/slot/
        b. api returns the future slots for the selected company (we may have paging there and return monthly slots on this api).
        
# stacks used
django, djangorestframework, celery, postgresql, redis

# pre-requisite: install postgresql and redis on machine

# project setup
1. git clone https://github.com/pk026/ola.git
2. create a virtualenv using: virtualenv venv (install virtualenv on your machine if not already installed)
3. activate environment using: source venv/bin/activate
4. upgrade pip using: pip install --upgrade pip
5. curl https://bootstrap.pypa.io/get-pip.py | python
6. install requirements using: pip install -r requirements.txt
7. make database setting proper: create a database with name:ola, user:pramod, password: postgres
8. install redis and run it on machine
or you can create database with your own set of parameters and update them into settings.py: DATABASES
9. create database schema using: python manage.py migrate
10. create a superuser: python manage.py createsuperuser
11. run: python manage.py runserver
12. run: celery -A ola worker --app=ola.ola_celery:app --loglevel=info
(on other terminal)

# testbench
# request a ride
API: api/v1/trip/
Method:POST
data: {"user": 1}
(after we implement authentication we post location to server user_id we may get from auth token)

# pick the ride
API: api/v1/trip/1/?user_id=1
Method:PATCH
data: {"status": "ongoing"}
user_id in query params 
(when we implement login we can get user with auth token no need to pass this in query params)

# Customer app
put customer id if field and click ride now.
this would post: {"user": 1} on api/v1/trip/ this would create a trip with status waiting

# driver app
when driver opens up dashboard
(we identify driver by user_id query params, one we implement authentication
we can identify driver by his auth token or session token)
it calls the api: api/v1/trip/?source_app=DRIVER_APP&user_id=1

we get response like below:


driver can pick up any of waiting trips to server:
    to pick a ride:
    PATCH request on api/v1/trip/{waiting_trip_id}/?user_id=1
    data: {"status": "ongoing"}
    api returns the trip object with status 200 if succeded
    else returns error with status 400

# Dashboard app
it calls the api: api/v1/trip/?source_app=DASHBOARD_APP
it returns:
