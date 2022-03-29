#!/bin/bash
echo Starting django-categorization app.
cd /var/www/html/django-categorization/
gunicorn --workers=5 --bind  ec2-54-148-140-54.us-west-2.compute.amazonaws.com:3002 gettingstarted.wsgi:application
sudo python3 -m pip install django
sudo python3 -m pip install django-cors-headers
sudo python3 -m pip install django-sslserver
sudo python3 -m pip install nltk
sudo python3 -m pip install python-rake
sudo python3 -m pip install BeautifulSoup4
sudo python3 -m pip install pandas


sin evaluar, favorable verde, neutral gris, desfavorable rojo.

https://www.google.com/search?hl=es&as_q=create+modal+html+css&as_epq=&as_oq=&as_eq=&as_nlo=&as_nhi=&lr=&cr=countryPE&as_qdr=all&as_sitesearch=&as_occt=any&safe=images&as_filetype=&tbs=

&cr=countryPE
https://www.google.com/preferences?hl=es-419&prev=https://www.google.com/search?q%3Doec%26source%3Dhp%26ei%3DcjhDYpu9Mv-b1sQP_a6ZsAo%26iflsig%3DAHkkrS4AAAAAYkNGgnFxYatRO0r7RO8yP_nc_PmyCxpH%26ved%3D0ahUKEwibvtig4-v2AhX_jZUCHX1XBqYQ4dUDCAc%26uact%3D5%26oq%3Doec%26gs_lcp%3DCgdnd3Mtd2l6EAMyCwguEIAEEMcBENEDMgUIABCABDIFCAAQgAQyBQgAEIAEMgUILhCABDILCC4QgAQQxwEQowIyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEOggIABCPARDqAjoICC4QjwEQ6gI6CAgAEIAEELEDOg4ILhCABBCxAxDHARDRAzoLCAAQgAQQsQMQgwE6CAgAELEDEIMBOg4ILhCABBCxAxDHARCvAVCFBliRCWD8CmgBcAB4AIABZYgBhQKSAQMyLjGYAQCgAQGwAQo%26sclient%3Dgws-wiz#languages
