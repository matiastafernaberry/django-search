#!/bin/bash
echo Starting django-categorization app.
cd /var/www/html/django-categorization-http/
#gunicorn --bind ec2-52-38-13-82.us-west-2.compute.amazonaws.com:80 gettingstarted.wsgi:application
gunicorn --workers=5  --bind ec2-52-38-13-82.us-west-2.compute.amazonaws.com:3001 gettingstarted.wsgi:application
