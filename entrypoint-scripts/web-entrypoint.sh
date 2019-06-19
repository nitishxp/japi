#!/bin/bash
echo running post install scripts for web..;
python /code/manage.py makemigrations
python /code/manage.py migrate
python /code/manage.py test
python /code/manage.py runserver 0.0.0.0:8000