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

from nltk import sent_tokenize, ne_chunk, pos_tag, word_tokenize
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
from nltk.chunk import conlltags2tree, tree2conlltags
from nltk.stem import SnowballStemmer
from bs4 import BeautifulSoup

nltk.data.path.append('./nltk_data/')

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from os import listdir
from os.path import isfile, join


#from .models import Greeting
from django.conf import settings


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__).replace("views","")),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)



class BuzzTrackerClass(View):
	"""docstring for MainClass"""
	def get(self, request):
		
		#mypath = os.path.dirname(__file__).replace("views","").replace("hello","tmp")
		mypath = "hello/static/files/"
		#print(mypath)
		import glob
		#paths = sorted(Path(mypath).iterdir(), key=os.path.getmtime)
		#onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
		files = list(filter(os.path.isfile, glob.glob(mypath + "*")))
		files.sort(key=lambda x: os.path.getmtime(x))
		print(files)
		files.reverse()
		fil = []
		for i in files:
			fil.append(i.replace('hello/static/files/', ''))
		#onlyfiles.sort(key=os.path.getctime)
		return TemplateResponse(request, 'buzztracker.html', {'files': fil})

	def post(self, request):
		if 'myfile' in self.request.FILES:
			data = self.request.FILES['myfile']
			name_file = self.request.POST['mytext']
			name_file = 'hello/static/files/' + name_file + '.csv'
			jsonFilePath = 'hello/static/files/' + self.request.POST['mytext'] + '.json'
			path = default_storage.save(name_file, ContentFile(data.read()))
			tmp_file = os.path.join(settings.MEDIA_ROOT, path)
			data = {}
			with open(name_file, encoding='utf-8', errors='ignore') as csv_file: #, 'rb'
				#contents = csv_file.read()
				#csv_reader = csv.DictReader(x.replace('\0', '') for x in csv_file)
				#print(type(contents.decode(encoding="utf-8")));;;;;;;;;;;;;;;;;;;;
				try:
					csv_reader = csv.DictReader((x.replace('\0', '') for x in csv_file), delimiter='\t')
					#csv_reader = csv.reader(csv_file, delimiter=',')
					for row in csv_reader:
						#print(row)
						key = row['URL']
						data[key] = row
				except KeyError:
					print(traceback.format_exc())
					return TemplateResponse(request, 'buzztracker.html', {'error': 'Debe guardar el csv separado por tabuladores, y no por ; o ,'})
				except:
					print(traceback.format_exc())
					return TemplateResponse(request, 'buzztracker.html', {'error': 'error desconocido'})

			with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
				jsonf.write(json.dumps(data, indent=4))
			#with open(tmp_file, newline='') as csvfile:
			#	reader = csv.reader(csvfile)
			#	for row in reader:
			#		print(row)
			#		context["csv_rows"].append(" ".join(row))
			

		mypath = "hello/static/files/"
		onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
		onlyfiles.reverse()
		return TemplateResponse(request, 'buzztracker.html', {'files': onlyfiles})


class FileClass(View):
	"""docstring for MainClass"""
	def get(self, request):
		return TemplateResponse(request, 'files.html', {'files': ''})

	def post(self, request):
		dataPost = request.body.decode('utf-8')
		proyecto = self.request.POST['proyecto']
		busqueda = self.request.POST['busqueda']
		tipobusqueda = self.request.POST['tipobusqueda']
		paises = self.request.POST['paises']
		print(proyecto)
		print(busqueda)
		print(tipobusqueda)
		print(paises)

		return redirect('/')


class NuevaBusquedaClass(View):
	"""docstring for MainClass"""
	def get(self, request):
		f = open("paises.yml", "r")
		lista_paises = {}
		for x in f:
			pais = x.split()
			lista_paises[pais[0]] = pais[1].lower()

		return TemplateResponse(request, 'nueva-busqueda.html', {'lista_paises': lista_paises})

	def post(self, request):
		dataPost = request.body.decode('utf-8')
		proyecto = self.request.POST['proyecto']
		busqueda = self.request.POST['busqueda']
		tipobusqueda = self.request.POST['tipobusqueda']
		paises = self.request.POST['paises']
		print(" ")
		print(proyecto)
		print(busqueda)
		print(tipobusqueda)
		print(paises)
		USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
		headers = {"user-agent" : USER_AGENT}
		query = busqueda.replace(' ', '+')
		URL = f"https://google.com/search?q={query}&num=20"
		resp = requests.get(URL, headers=headers)
		soup = BeautifulSoup(resp.text, "html.parser")
		f = open("google.txt", "wb")
		f.write(soup.prettify().encode('cp1252', errors='ignore') )
		f.close()
		if resp.status_code == 200:
			soup = BeautifulSoup(resp.content, "html.parser")
			results = []
			for g in soup.find_all('div', class_='g'):
				anchors = g.find_all('a')
				
				if anchors:
					print(" ")
					try: 
						print(anchors[0]['href'])
						link = anchors[0]['href']
						results.append(link)
					except: 
						print(" error ")
						print(anchors[0])

		f = open("paises.yml", "r")
		lista_paises = {}
		for x in f:
			pais = x.split()
			lista_paises[pais[0]] = pais[1].lower()


		return TemplateResponse(request, 'nueva-busqueda.html', {'results': results, 'lista_paises': lista_paises})


