#!/bin/bash
echo Starting django-categorization app.
cd /var/www/html/django-categorization/
gunicorn --workers=5 --bind ec2-35-160-166-204.us-west-2.compute.amazonaws.com:4000 gettingstarted.wsgi:application
