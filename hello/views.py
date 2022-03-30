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
from .forms import BusquedaForm

from hello.models import Busqueda, ResultadoBusqueda


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
		datos = Busqueda.objects.all()
		return TemplateResponse(request, 'files.html', {'files': '','datos': datos})

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
		form = BusquedaForm()
		lista_paises = {}
		for x in f:
			pais = x.split()
			lista_paises[pais[0]] = pais[1].lower()

		return TemplateResponse(request, 'nueva-busqueda.html', {'lista_paises': lista_paises, 'form': form})

	def post(self, request):
		form = BusquedaForm()
		dataPost = request.body.decode('utf-8')
		proyecto = self.request.POST['proyecto']
		busqueda = self.request.POST['busqueda']
		tipobusqueda = self.request.POST['tipobusqueda']
		paises = self.request.POST['paises']
		paisesUpper = paises.upper()

		if not paises: paises = "com"
		USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
		headers = {"user-agent" : USER_AGENT}
		query = busqueda.replace(' ', '+')
		if tipobusqueda == "busqueda":
			
			#https://www.google.com.pa/search?q=guillermo+liberman+panama&oq=guillermo+liberman+panama&uule=w+CAIQICINUGFuYW1hLFBhbmFtYQ&hl=es&gl=pa&sourceid=chrome&ie=UTF-8
			#https://www.google.com/search?q=guillermo+liberman+panama&sxsrf=APq-WBvGXackTIj_DHQuRa2uxUgsi-4NrQ:1648661270855&source=hp&ei=FpNEYum0Mair1sQP4oq6mAo&iflsig=AHkkrS4AAAAAYkShJrKtZ1sEr6JMBz_8txCIItTx4QMo&oq=guillermo+liberman+pana&gs_lcp=Cgdnd3Mtd2l6EAMYADIFCAAQgAQ6BgizARCFBDoFCC4QgAQ6BggAEBYQHlCDfVj5kQFgvaEBaAFwAHgAgAGvAYgBkAeSAQMwLjaYAQCgAQKgAQGwAQE&sclient=gws-wiz
			#https://www.google.com/search?q=guillermo+liberman+panama&source=hp&ei=NZVEYvufH82Q1sQP38O66Ac&iflsig=AHkkrS4AAAAAYkSjRSEmYo6frwLzCxPbT39V1HhadYSo&ved=0ahUKEwi7jv_tr-72AhVNiJUCHd-hDn0Q4dUDCAY&uact=5&oq=guillermo+liberman+panama&gs_lcp=Cgdnd3Mtd2l6EAMyBQgAEIAEUABYAGCoCGgAcAB4AIABWYgBWZIBATGYAQCgAQKgAQE&sclient=gws-wiz
			print(paises)
			if paises != "com":
				URL = f"https://google.com.{paises}/search?q={query}&oq={query}&num=20&hl=es&gl={paises}&ie=UTF-8" #&lr=lang_es
			else:
				URL = f"https://google.com/search?q={query}&oq={query}&num=20&hl=es&gl={paises}&ie=UTF-8" #&lr=lang_es
			#URL = f"https://google.com/search?q={query}&oq={query}&num=20hl=es&gl={paises}&cr=country{paisesUpper}&ie=UTF-8" #&lr=lang_es
			print(URL)
		if tipobusqueda == "imagen":
			URL = f"https://images.google.com/search?q={query}&num=20"
		if tipobusqueda == "video":
			URL = f"https://www.google.com/search?tbm=vid&hl=es-UY&source=hp&biw=&bih=&q={query}&num=20&cr=country{paises}"

		resp = requests.get(URL, headers=headers)
		soup = BeautifulSoup(resp.text, "html.parser")
		f = open("google.txt", "wb")
		f.write(soup.prettify().encode('cp1252', errors='ignore'))
		f.close()
		if resp.status_code == 200:
			soup = BeautifulSoup(resp.content, "html.parser")
			results = []
			for g in soup.find_all('div', class_='g'):
				anchors = g.find_all('a')
				for data in g.find_all('span'):
					description = data.get_text()
				for data in g.find_all('h3'):
					title_search = data.get_text()
				if anchors:
					#title_search = anchors.find('h3')
					try: 
						#print(anchors[0]['href'])
						link = anchors[0]['href']
						print(link)
						d = {"title": title_search,"url":link,"description":description}
						results.append(d)
					except: 
						print(" error ")
						print(anchors[0])
		#form_post = BusquedaForm(request.POST)
		#form_post.save()
		f = open("paises.yml", "r")
		lista_paises = {}
		for x in f:
			pais = x.split()
			lista_paises[pais[0]] = pais[1].lower()

		return TemplateResponse(request, 'nueva-busqueda.html', {
			'results': results, 
			'lista_paises': lista_paises, 
			'form': form,
			'proyecto': proyecto,
			'busqueda': busqueda
		})


class GuardarResultadosBusquedaClass(View):
	"""docstring for MainClass"""
	def post(self, request):
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode) 
		
		
		print(body["busqueda"])
		print(body["datos"])
		busqueda = json.loads(body["busqueda"]) 
		datos = json.loads(body["datos"]) 
		print(datos[0])

		b2 = Busqueda(proyecto=busqueda["proyecto"], busqueda=busqueda["busqueda"])
		b2.save()
		print(b2.id)
		for i in datos:
			b3 = ResultadoBusqueda(
				url = i["url"], 
				evaluacion = i["evalucion"],
				busqueda = Busqueda.objects.get(id=b2.id)
			)
			b3.save()
			print(b3.id)

		
		#form_post = BusquedaForm(request.POST)
		#form_post.save()
		f = open("paises.yml", "r")
		lista_paises = {}
		for x in f:
			pais = x.split()
			lista_paises[pais[0]] = pais[1].lower()

		dataResponse = {
			'status': "success",
			'code': 200,
		}
		dataResponse = json.dumps(dataResponse)
		#print(dataResponse)
		return HttpResponse(dataResponse, content_type='application/json')


