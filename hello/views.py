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
import random
import string


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
from datetime import datetime


#from .models import Greeting
from django.conf import settings
from .forms import BusquedaForm

from hello.models import Busqueda, ResultadoBusqueda

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import traceback
from fake_useragent import UserAgent
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
		f = open("paisesdos.yml", "r")
		form = BusquedaForm()
		lista_paises = {}
		for x in f:
			pais = x.split()
			lista_paises[pais[0]] = pais[1].lower()

		return TemplateResponse(request, 'nueva-busqueda.html', {'lista_paises': lista_paises, 'form': form})

	def post(self, request):
		form = BusquedaForm()
		dataPost = request.body.decode('utf-8')
		proyecto = (self.request.POST['proyecto']).lower()
		busqueda = (self.request.POST['busqueda']).lower()
		tipobusqueda = self.request.POST['tipobusqueda']
		paises = self.request.POST['paises']
		paisesUpper = paises.upper()

		if not paises: paises = "com"
		
		options = Options()
		options.add_argument("--headless") #para que se no abra el navegador 
		options.add_argument("window-size=1400,600")
		options.add_argument("--enable-javascript")
		#options.add_argument("javascript.enabled", True)
		#options.add_argument("user-agent=[Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0]")
		options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"')
		options.add_argument('user-agent={"Mozilla/5.0 (Linux; Android 8.1.0; Pixel Build/OPM4.171019.021.D1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.109 Mobile Safari/537.36 EdgA/42.0.0.2057"}')
		ua = UserAgent()
		options.binary_location = '/usr/bin/firefox'
		#options.binary_location = '/usr/local/firefox/firefox' #server
		browser = webdriver.Firefox(options=options,executable_path="/usr/local/bin/geckodriver")
		#browser = webdriver.Firefox(options=options,executable_path="/home/ec2-user/django-search/geckodriver") #server
		print(browser.execute_script("return navigator.userAgent;"))
		browser.get('https://www.google.com/preferences?hl=es&prev=https://www.google.com/search?q%3Da%26source%3Dhp%26ei%3DQdhyYtPzCNid5OUPgPaIOA%26iflsig%3DAJiK0e8AAAAAYnLmUXUEeDCkQUeO5LXbRMb41uPPQYC9%26ved%3D0ahUKEwiTmKCizsb3AhXYDrkGHQA7AgcQ4dUDCAY%26uact%3D5%26oq%3Da%26gs_lcp%3DCgdnd3Mtd2l6EAMyDgguEIAEELEDEMcBEKMCMhEILhCABBCxAxCDARDHARDRAzILCAAQgAQQsQMQgwEyCAgAELEDEIMBMggIABCABBCxAzIOCC4QgAQQsQMQxwEQ0QMyCAguELEDEIMBMg4ILhCABBCxAxDHARDRAzIICAAQgAQQsQMyBQguEIAEUABYAGCJBWgAcAB4AIABjwGIAY8BkgEDMC4xmAEAoAEB%26sclient%3Dgws-wiz')
		browser.implicitly_wait(2)
		configuracion = browser.find_element(By.ID, "regionanchormore")
		configuracion.click()
		browser.implicitly_wait(2)
		browser.execute_script("document.getElementById('result_slider').setAttribute('aria-valuenow', '40')")
		print(browser.execute_script("document.getElementById('result_slider').getAttribute('aria-valuenow')"))
		
		configuracion = browser.find_element(by=By.CSS_SELECTOR, value="#result_slider")
		configuracion.click()
		browser.implicitly_wait(2)
		configuracion = browser.find_element(by=By.XPATH, value="//div[@class='jfk-radiobutton' and @data-value='{}']".format(paisesUpper))
		configuracion.click()
		
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		browser.implicitly_wait(1)
		configuracion = browser.find_element(by=By.XPATH, value="/html/body/div[4]/form/div/div[2]/div[2]/div/div[1]")
		configuracion.click()
		browser.implicitly_wait(2)
		configuracion = browser.find_element(by=By.XPATH, value="/html/body/div[4]/div[2]/form/div[1]/div[1]/div[2]/div/div[2]/input").clear() #el search
		configuracion = browser.find_element(by=By.XPATH, value="/html/body/div[4]/div[2]/form/div[1]/div[1]/div[2]/div/div[2]/input") #
		configuracion.send_keys(busqueda) #search lacalle pou
		configuracion = browser.find_element(by=By.XPATH, value="/html/body/div[4]/div[2]/form/div[1]/div[1]/div[2]/button").click() #en el boton de busqueda
		noticias_destacadas = ""
		try:
			noticias_destacadas = browser.find_element(by=By.XPATH, value="/html/body/div[7]/div/div[10]/div[1]/div[2]/div[2]/div/div/div[1]/g-section-with-header/div[1]/div/title-with-lhs-icon/div[2]/h3").text
			if noticias_destacadas == "Noticias destacadas":
				print(noticias_destacadas)
				try:
					lista = browser.find_elements(by=By.TAG_NAME, value="g-section-with-header")
					for i in lista: pass
						#print(i.get_attribute('innerHTML'))
				except: print(traceback.format_exc())
			else: print("no es noticias destacada")
		except: print("no es noticias destacada")
		try:
			video = browser.find_elements(by=By.CSS_SELECTOR, value=".iJ1Kvb")
			for i in video:
				#print(i.text)
				if i.text == "Videos": print("Videos")	
		except: print(traceback.format_exc())
		try:
			posicion_video = browser.find_elements(by=By.CSS_SELECTOR, value="#rso")
			print("posicion video")
			for i in posicion_video:
				#print(i.get_attribute('innerHTML'))
				videos_url = i.find_elements(by=By.TAG_NAME, value="div")
				#for e in videos_url:
				#	print(e.get_attribute('innerHTML'))
				#	print(" ")
		except: print(traceback.format_exc())

		#primer_link = browser.find_elements(by=By.XPATH, value="/html/body/div[7]/div/div[10]/div/div[2]/div[2]/div/div/div[1]")
		#print(" ")
		#print(primer_link[0])
		#for c in primer_link: pass
			#print(c.tag_name)
			#print(c.text)
		#texto = browser.find_elements(by=By.XPATH, value="/html/body/div[7]/div/div[10]/div/div[2]/div[2]/div/div/div[1]/div/div[1]/div[1]/div/a/h3")
		texto = browser.find_elements(by=By.CSS_SELECTOR, value=".g")
		datos = []
		lista_url = []
		for c in texto:
			#print(c.get_attribute('innerHTML'))
			#print(" ")
			#print(c.text)
			lista = c.find_elements(by=By.TAG_NAME, value="a")
			count,coun = 0,0
			
			for d in lista:
				url = d.get_attribute("href")
				try:
					if "https://webcache" not in url and "https://translate" not in url and "http://webcache" not in url and "https://www.google.com" not in url:
						#print("url")
						#print(url)
						#print(c.text)
						#print(lista_url)
						#print(" ")
						#try: x = di["url"]
						#except:
						if url not in lista_url: 
							di = {}
							di["url"] = url
							di["texto"] = c.text
							datos.append(di)
							lista_url.append(url)
						count += 1
				except: print(traceback.format_exc())
			coun += 1

		print("noticias destacadas")
		print(noticias_destacadas)
		if noticias_destacadas == "Noticias destacadas":
			di = {}
			di["url"] = "http://noticiasdestacadas.com"
			di["texto"] = "Noticias destacadas"
			datos.insert(0,di)
		print(" ")
		print(lista_url)
		f = open("paisesdos.yml", "r")
		lista_paises = {}
		for x in f:
			pais = x.split()
			lista_paises[pais[0]] = pais[1].lower()
		# try:
		# 	datos_resultado_busqueda = ""
		# 	datos_busqueda = Busqueda.objects.filter(
		# 		busqueda__exact = busqueda,
		# 		proyecto__exact = proyecto
		# 	)
		# 	print(" ")
		# 	print("datos_busqueda")
		# 	print(datos_busqueda.count())
		# 	if datos_busqueda.count() > 0:
		# 		datos_busqueda = Busqueda.objects.get(busqueda__exact = busqueda, proyecto__exact = proyecto)
		# 		datos_resultado_busqueda = ResultadoBusqueda.objects.filter(busqueda__pk = datos_busqueda.id)
		# except: 
		# 	print("error")
		# 	print(traceback.format_exc())
		# 	datos_busqueda = ""
		
		try:
			datos_resultado_busqueda = ""
			datos_busqueda = Busqueda.objects.filter(
				busqueda__exact = busqueda,
				proyecto__exact = proyecto
			)
			#print(" ")
			#print("datos_busqueda")
			#print(datos_busqueda.count())
			if datos_busqueda.count() > 0:
				datos_busqueda = Busqueda.objects.get(busqueda__exact = busqueda)
				datos_resultado_busqueda = ResultadoBusqueda.objects.raw('SELECT  fecha_modificacion, MAX(id) as id FROM hello_resultadobusqueda where busqueda_id = {} GROUP BY fecha_modificacion order by fecha_modificacion desc limit 1'.format(datos_busqueda.id))
				for i in datos_resultado_busqueda:
					idstringg = i.idstring
				datos_resultado_busqueda = ResultadoBusqueda.objects.filter(idstring = idstringg)

		except: 
			print("error datos busqueda")
			print(traceback.format_exc())
			datos_busqueda = ""
		
		return TemplateResponse(request, 'nueva-busqueda.html', {
			'results': datos, 
			'lista_paises': lista_paises, 
			'pais_post': paises,
			'form': form,
			'proyecto': proyecto,
			'busqueda': busqueda,
			'datos_busqueda': datos_resultado_busqueda
		})



class GuardarResultadosBusquedaClass(View):
	"""docstring for MainClass"""
	def post(self, request):
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode) 
		
		#print(body["busqueda"])
		#print(body["datos"])
		busqueda = json.loads(body["busqueda"]) 
		datos = json.loads(body["datos"]) 
		#print(datos[0])

		datos_busqueda = Busqueda.objects.filter(
			busqueda__exact = busqueda["busqueda"],
			proyecto__exact = busqueda["proyecto"]
		)
		if datos_busqueda.count() == 0:
			b2 = Busqueda(
				proyecto = (busqueda["proyecto"]).lower(), 
				busqueda = (busqueda["busqueda"]).lower(),
				tipobusqueda = busqueda["tipobusqueda"],
				pais = busqueda["pais"]
			)
			b2.save()
			id_resultados = b2.id
		else:
			datos_busqueda = Busqueda.objects.get(
				busqueda__exact = busqueda["busqueda"],
				proyecto__exact = busqueda["proyecto"]
			)
			id_resultados = datos_busqueda.id
		print(" ")
		count = 1
		letters = string.ascii_lowercase
		result_str = ''.join(random.choice(letters) for i in range(10))
		for i in datos:
			if count == 1: puntaje = 0.095
			if count == 2: puntaje = 0.090
			if count == 3: puntaje = 0.086
			if count == 4: puntaje = 0.081
			if count == 5: puntaje = 0.076
			if count == 6: puntaje = 0.071
			if count == 7: puntaje = 0.067
			if count == 8: puntaje = 0.062
			if count == 9: puntaje = 0.057
			if count == 10: puntaje = 0.052
			if count == 11: puntaje = 0.048
			if count == 12: puntaje = 0.043
			if count == 13: puntaje = 0.038
			if count == 14: puntaje = 0.033
			if count == 15: puntaje = 0.029
			if count == 16: puntaje = 0.024
			if count == 17: puntaje = 0.019
			if count == 18: puntaje = 0.014
			if count == 19: puntaje = 0.010
			if count == 20: puntaje = 0.0005

			now = datetime.now()
			now = now.strftime("%d-%m-%Y %H:%M")
			tiempo = datetime.strptime(now, '%d-%m-%Y %H:%M')
			try: titulo = i["titulo"]
			except: titulo = ""
			try: descripcion = i["descripcion"]
			except: descripcion = ""

			
			b3 = ResultadoBusqueda(
				url = i["url"], 
				evaluacion = i["evalucion"],
				busqueda = Busqueda.objects.get(id=id_resultados),
				puntaje = puntaje,
				posicion = count,
				fecha_modificacion = tiempo,
				idstring = result_str,
				titulo = titulo,
				descripcion = descripcion
			)
			b3.save()
			count += 1

		f = open("paises.yml", "r")
		lista_paises = {}
		for x in f:
			pais = x.split()
			lista_paises[pais[0]] = pais[1].lower()

		dataResponse = {
			'status': "success",
			'code': 200,
			'idstring':b3.idstring
		}
		dataResponse = json.dumps(dataResponse)
		return HttpResponse(dataResponse, content_type='application/json')


class PreVerhistoricosClass(View):
	"""docstring for MainClass"""
	def get(self, request, id):
		#print(id)
		#datos = ResultadoBusqueda.objects.raw('SELECT  fecha_modificacion, url, evaluacion, puntaje, posicion, id FROM hello_resultadobusqueda where busqueda_id = {} GROUP BY busqueda_id'.format(id))
		#datos = ResultadoBusqueda.objects.raw('SELECT  fecha_modificacion, MAX(id) as id FROM hello_resultadobusqueda where busqueda_id = {} GROUP BY fecha_modificacion order by fecha_modificacion desc limit 1'.format(id))
		datos = ResultadoBusqueda.objects.raw('SELECT  fecha_modificacion, MAX(id) as id FROM hello_resultadobusqueda where busqueda_id = {} GROUP BY fecha_modificacion'.format(id))
		#for i in datos:
		#	print(i.fecha_modificacion.strftime("%m-%d-%Y %H:%M"))
		dataResponse = {
			'status': "success",
			'code': 200,
		}
		dataResponse = json.dumps(dataResponse)
		return TemplateResponse(request, 'historicos.html', {'datos': datos})


class VerhistoricosClass(View):
	"""docstring for MainClass"""
	def get(self, request, id):
		#print(id)
		datos = ResultadoBusqueda.objects.filter(idstring = id).order_by('posicion')
		dataResponse = {
			'status': "success",
			'code': 200,
		}
		dataResponse = json.dumps(dataResponse)
		return TemplateResponse(request, 'ver-historicos.html', {'datos': datos})


class ReEvaluarClass(View):
	"""docstring for MainClass"""
	def get(self, request, id):
		USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
		headers = {"user-agent" : USER_AGENT}
		datos = Busqueda.objects.get(id = id)
		query = datos.busqueda
		busqueda = datos.busqueda.lower()
		proyecto = datos.proyecto.lower()
		tipobusqueda = datos.tipobusqueda
		paises = datos.pais
		if tipobusqueda == "busqueda":
			if paises != "com":
				URL = f"https://google.com.{paises}/search?q={query}&oq={query}&num=30&hl=es&gl={paises}&ie=UTF-8" #&lr=lang_es
			else:
				URL = f"https://google.com/search?q={query}&oq={query}&num=30&hl=es&gl={paises}&ie=UTF-8" #&lr=lang_es
		if tipobusqueda == "imagen":
			URL = f"https://images.google.com/search?q={query}&num=30"
		if tipobusqueda == "video":
			URL = f"https://www.google.com/search?tbm=vid&hl=es-UY&source=hp&biw=&bih=&q={query}&num=30&cr=country{paises}"
		try:
			resp = requests.get(URL, headers=headers)
		except:
			URL = f"https://google.com/search?q={query}&oq={query}&num=30&hl=es&gl={paises}&ie=UTF-8" #&lr=lang_es
			resp = requests.get(URL, headers=headers)

		soup = BeautifulSoup(resp.text, "html.parser")
		count = 1
		if resp.status_code == 200:
			soup = BeautifulSoup(resp.content, "html.parser")
			results = []
			lista_url = []
			for g in soup.find_all('div', class_='g'):
				anchors = g.find_all('a')
				for data in g.find_all('span'):
					description = data.get_text()
				for data in g.find_all('h3'):
					title_search = data.get_text()
				print(" a ")
				print(anchors)
				if anchors:
					try:
						link = anchors[0]['href']
						for i in anchors:
							if i.h3:
								if i['href'] not in lista_url:
									description = i.h3.get_text()
									for data in i.find_all('span'):
										description = data.get_text()
									for data in i.find_all('h3'):
										title_search = data.get_text()
									
									d = {"title": title_search,"url":i['href'],"description":description}
									if count < 21:
										results.append(d)
										lista_url.append(i['href'])
									count += 1
							try:
								if i.h3['class'][0] == "LC20lb": pass
							except: pass
					except: 
						print(" ")
						print("line 201 error ")
						print(traceback.format_exc())
		
		f = open("paisesdos.yml", "r")
		lista_paises = {}
		for x in f:
			pais = x.split()
			lista_paises[pais[0]] = pais[1].lower()
		try:
			datos_resultado_busqueda = ""
			datos_busqueda = Busqueda.objects.filter(
				busqueda__exact = busqueda,
				proyecto__exact = proyecto
			)
			#print(" ")
			#print("datos_busqueda")
			#print(datos_busqueda.count())
			if datos_busqueda.count() > 0:
				datos_busqueda = Busqueda.objects.get(busqueda__exact = busqueda)
				datos_resultado_busqueda = ResultadoBusqueda.objects.raw('SELECT  fecha_modificacion, MAX(id) as id FROM hello_resultadobusqueda where busqueda_id = {} GROUP BY fecha_modificacion order by fecha_modificacion desc limit 1'.format(datos_busqueda.id))
				for i in datos_resultado_busqueda:
					idstringg = i.idstring
				datos_resultado_busqueda = ResultadoBusqueda.objects.filter(idstring = idstringg)

		except: 
			print("error")
			print(traceback.format_exc())
			datos_busqueda = ""
		
		return TemplateResponse(request, 're-evaluar.html', {
			'results': results, 
			'lista_paises': lista_paises, 
			'pais_post': paises,
			'proyecto': proyecto,
			'busqueda': busqueda,
			'datos_busqueda': datos_resultado_busqueda
		})

