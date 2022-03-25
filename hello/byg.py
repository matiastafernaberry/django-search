#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import nltk
import json
import os
import re
import traceback 
import six
import operator
import RAKE
import jinja2
import csv
import datetime
from datetime import datetime, timedelta

from nltk import sent_tokenize, ne_chunk, pos_tag, word_tokenize
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
from nltk.chunk import conlltags2tree, tree2conlltags
from nltk.stem import SnowballStemmer

nltk.data.path.append('./nltk_data/')

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from os import listdir
from os.path import isfile, join
import mysql.connector
import pandas as pd
from pandas import DataFrame


#from .models import Greeting
from django.conf import settings


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__).replace("views","")),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)


class ApiGetDocumentsSharedCount7Class(View):
	"""docstring for MainClass"""
	# def get(self, request):
	# 	mypath = "hello/static/sfiles/"
	# 	import glob
	# 	files = list(filter(os.path.isfile, glob.glob(mypath + "*")))
	# 	files.sort(key=lambda x: os.path.getmtime(x))
	# 	print(files)
	# 	files.reverse()
	# 	fil = []
	# 	for i in files:
	# 		fil.append(i.replace('hello/static/sfiles/', ''))
	# 	return TemplateResponse(request, 'files.html', {'files': fil})

	def post(self, request):
		dataPost = request.body.decode('utf-8')
		dataPost = json.loads(dataPost)
		print(dataPost['similar'])
		#dataPostStr = ','.join(map(str, dataPost['similar']))
		try: dataPost = tuple(dataPost['similar'])
		except: dataPost = str(dataPost['similar'])
		#print(dataPostStr)
		cnx = mysql.connector.connect(user='admin', password='3y3w4tch20204dm1n',
            host='meltwater-dbcluster-instance-1.cffatgb5exir.us-west-2.rds.amazonaws.com',
            database='meltwater')
		cursor1 = cnx.cursor(buffered=True)
		if isinstance(dataPost, tuple):
			cursor1.execute("""SELECT DISTINCT( dsc.`URL`), dsc.`Date`, dsc.`Share_Count`, d.Id_URL 
				FROM DOCUMENTS_SHAREDCOUNT_TREND_7_DIAS as dsc, DOCUMENTS as d 
				where d.Id_URL in {} and dsc.url=d.url ORDER By dsc.Date ASC""".format(dataPost))
		else:
			cursor1.execute("""SELECT DISTINCT( dsc.`URL`), dsc.`Date`, dsc.`Share_Count`, d.Id_URL 
				FROM DOCUMENTS_SHAREDCOUNT_TREND_7_DIAS as dsc, DOCUMENTS as d 
				where d.Id_URL = {} and dsc.url=d.url ORDER By dsc.Date ASC""".format(dataPost))
		myresult = cursor1.fetchall()
		data = DataFrame(myresult,
  			columns=['URL', 'Date', 'Share_Count', 'Id_URL'])
		listData = []
		for row in data.iterrows():
			d = {}
			d['URL'] = row[1]["URL"]
			d['Date'] = row[1]["Date"].strftime('%Y-%m-%d %H:%M:%S')
			d['Share_Count'] = row[1]["Share_Count"]
			listData.append(d)
		dataResponse = {
			'status': "success",
			'code': 200,
			'data': listData,
			'message': 'null'
		}
		dataResponse = json.dumps(dataResponse)
		#print(dataResponse)
		return HttpResponse(dataResponse, content_type='application/json')



class ApiGetBGDocuments7AllByClient(View):
	def get(self, request):

		dataResponse = {
			'status': "success",
			'code': 200,
			'data': listData,
			'message': 'null'
		}
		dataResponse = json.dumps(dataResponse)
		#print(dataResponse)
		return HttpResponse(dataResponse, content_type='application/json')