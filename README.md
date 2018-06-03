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
user_id in query params (when we implement login we can get user with auth token no need to pass this in query params)

# Customer app
put customer id if field and click ride now.
this would post: {"user": 1} on api/v1/trip/ this would create a trip with status waiting

# driver app
when driver opens up dashboard (we identify driver by user_id query params, one we implement authentication we can identify driver by his auth token or session token)
it calls the api: api/v1/trip/?source_app=DRIVER_APP&user_id=1

we get response like below:
{
    "completed": [
        {
            "id": 8,
            "request_time_lapsed": "404.038872",
            "pickup_time_lapsed": "19.127396",
            "completed_time_lapsed": 350.127396,
            "source": null,
            "destination": null,
            "status": "completed",
            "completed_at": null,
            "pickup_at": "2018-06-03T13:24:00.687421Z",
            "created": "2018-06-03T13:17:35.775922Z",
            "user": 1,
            "driver": 1,
            "car": 1
        }
    ],
    "ongoing": [
        {
            "id": 9,
            "request_time_lapsed": "401.342999",
            "pickup_time_lapsed": "27.030906",
            "completed_time_lapsed": null,
            "source": null,
            "destination": null,
            "status": "ongoing",
            "completed_at": null,
            "pickup_at": "2018-06-03T13:23:52.783553Z",
            "created": "2018-06-03T13:17:38.471427Z",
            "user": 1,
            "driver": 1,
            "car": 1
        }
    ],
    "waiting": [
        {
            "id": 7,
            "request_time_lapsed": "404.790879",
            "pickup_time_lapsed": null,
            "completed_time_lapsed": null,
            "source": null,
            "destination": null,
            "status": "waiting",
            "completed_at": null,
            "pickup_at": null,
            "created": "2018-06-03T13:17:35.030502Z",
            "user": 1,
            "driver": null,
            "car": null
        }
    ]
}

driver can pick up any of waiting trips to server:
    to pick a ride:
    PATCH request on api/v1/trip/{waiting_trip_id}/?user_id=1
    data: {"status": "ongoing"}
    api returns the trip object with status 200 if succeded
    else returns error with status 400

# Dashboard app
it calls the api: api/v1/trip/?source_app=DASHBOARD_APP
it returns:
[
    {
        "id": 9,
        "request_time_lapsed": "834.398308",
        "pickup_time_lapsed": "460.086204",
        "completed_time_lapsed": null,
        "source": null,
        "destination": null,
        "status": "ongoing",
        "completed_at": null,
        "pickup_at": "2018-06-03T13:23:52.783553Z",
        "created": "2018-06-03T13:17:38.471427Z",
        "user": 1,
        "driver": 1,
        "car": 1
    },
    {
        "id": 5,
        "request_time_lapsed": "839.516749",
        "pickup_time_lapsed": null,
        "completed_time_lapsed": null,
        "source": null,
        "destination": null,
        "status": "waiting",
        "completed_at": null,
        "pickup_at": null,
        "created": "2018-06-03T13:17:33.353683Z",
        "user": 1,
        "driver": null,
        "car": null
    },
    {
        "id": 5,
        "request_time_lapsed": "839.516749",
        "pickup_time_lapsed": 460.086204,
        "completed_time_lapsed": 60.086204,
        "source": null,
        "destination": null,
        "status": "completed",
        "completed_at": null,
        "pickup_at": null,
        "created": "2018-06-03T13:17:33.353683Z",
        "user": 1,
        "driver": null,
        "car": null
    }
]
