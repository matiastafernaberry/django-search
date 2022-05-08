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

import gtts
from playsound import playsound


options = Options()
#options.add_argument("--headless") #para que se abra el navegador 
options.add_argument("window-size=1500,900")
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
browser.get('https://app.slack.com/client/T02HHSVG2/D01FHNA0PN0')
browser.implicitly_wait(2)
#ql-editor
dominio = browser.find_element(By.CSS_SELECTOR, value="#domain")
dominio.send_keys('eyewatch.slack.com')
dominio = browser.find_element(By.CSS_SELECTOR, value=".c-button")
dominio.click()
dominio = browser.find_element(By.CSS_SELECTOR, value="#email")
dominio.send_keys('mtafernaberry@eyewatch.me')
dominio = browser.find_element(By.CSS_SELECTOR, value="#password")
dominio.send_keys('bondiola54411')
dominio = browser.find_element(By.CSS_SELECTOR, value="#signin_btn")
dominio.click()
browser.implicitly_wait(6)
try:
    dominio = browser.find_element(By.CSS_SELECTOR, value=".c-button-unstyled")
    dominio.click()
    print("si boton")
except:
    print("no boton")
    dominio = browser.find_element(By.CSS_SELECTOR, value=".p-client_desktop--ia-top-nav")
    dominio.click()
try:
    dominio = browser.find_element(By.CSS_SELECTOR, value=".c-button-unstyled")
    dominio.click()
    print("si boton")
except:
    print("no boton")

browser.implicitly_wait(1)
browser.find_element(By.CSS_SELECTOR, value=".ql-editor").clear()
dominio = browser.find_element(By.CSS_SELECTOR, value=".ql-editor")
dominio.send_keys('buenas')
try:
    dominio = browser.find_element(By.CSS_SELECTOR, value=".p-view_header__text")
    dominio.click()
except:
    dominio = browser.find_element(By.CSS_SELECTOR, value=".ReactModal__Overlay")
    dominio.click()
dominio = browser.find_element(By.CSS_SELECTOR, value=".c-wysiwyg_container__suffix")
dominio.click()

browser.implicitly_wait(55)
#browser.quit()
