#!/bin/bash

rm db.sqlite3
rm -rf ./hookdapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations hookdapi
python3 manage.py migrate hookdapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

