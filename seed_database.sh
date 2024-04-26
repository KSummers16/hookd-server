#!/bin/bash

rm db.sqlite3
rm -rf ./hookdapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations hookdapi
python3 manage.py migrate hookdapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata customers
# python3 manage.py loaddata orders
python3 manage.py loaddata category
python3 manage.py loaddata eyes
python3 manage.py loaddata rtsproducts
python3 manage.py loaddata cusproducts
# python3 manage.py loaddata cusrequests
python3 manage.py loaddata colors
python3 manage.py loaddata payment
