#!/bin/bash
echo Starting django-categorization app.
cd /var/www/html/django-categorization-http/
#gunicorn --bind 34.219.217.228:8000 gettingstarted.wsgi:application
gunicorn  --bind http://ec2-34-219-217-228.us-west-2.compute.amazonaws.com:8000 gettingstarted.wsgi:application
