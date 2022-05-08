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


options = Options()
#options.add_argument("--headless") #para que se abra el navegador 
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
browser.execute_script("document.getElementById('result_slider').setAttribute('aria-valuenow', '20')")
print(browser.execute_script("document.getElementById('result_slider').getAttribute('aria-valuenow')"))
configuracion = browser.find_element(by=By.CSS_SELECTOR, value="#result_slider")
configuracion.click()

configuracion = browser.find_element(by=By.XPATH, value="//div[@class='jfk-radiobutton' and @data-value='UY']")
configuracion.click()
browser.implicitly_wait(2)
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
browser.implicitly_wait(1)
configuracion = browser.find_element(by=By.XPATH, value="/html/body/div[4]/form/div/div[2]/div[2]/div/div[1]")
configuracion.click()
browser.implicitly_wait(2)
configuracion = browser.find_element(by=By.XPATH, value="/html/body/div[4]/div[2]/form/div[1]/div[1]/div[2]/div/div[2]/input").clear() #el search
configuracion = browser.find_element(by=By.XPATH, value="/html/body/div[4]/div[2]/form/div[1]/div[1]/div[2]/div/div[2]/input") #
configuracion.send_keys('lacalle pou') #search lacalle pou
configuracion = browser.find_element(by=By.XPATH, value="/html/body/div[4]/div[2]/form/div[1]/div[1]/div[2]/button").click() #en el boton de busqueda
try:
    noticias_destacadas = browser.find_element(by=By.XPATH, value="/html/body/div[7]/div/div[10]/div[1]/div[2]/div[2]/div/div/div[1]/g-section-with-header/div[1]/div/title-with-lhs-icon/div[2]/h3").text
    if noticias_destacadas == "Noticias destacadas":
        print(noticias_destacadas)
    else: print("no es noticias destacada")
except: print("no es noticias destacada")


primer_link = browser.find_elements(by=By.XPATH, value="/html/body/div[7]/div/div[10]/div/div[2]/div[2]/div/div/div[1]")
print(" ")
#print(primer_link[0])
for c in primer_link: pass
    #print(c.tag_name)
    #print(c.text)
#texto = browser.find_elements(by=By.XPATH, value="/html/body/div[7]/div/div[10]/div/div[2]/div[2]/div/div/div[1]/div/div[1]/div[1]/div/a/h3")
texto = browser.find_elements(by=By.CSS_SELECTOR, value=".g")
datos = []
lista_url = []
for c in texto:
    #print(c.get_attribute('innerHTML'))
    #print(" ")
    #if noticias_destacadas == "Noticias destacadas": continue
    #print(c.text)
    lista = c.find_elements(by=By.TAG_NAME, value="a")
    count,coun = 0,0
    di = {}
    for d in lista:
        print(d.get_attribute('innerHTML'))
        url = d.get_attribute("href")
        try:
            if "https://webcache" not in url and "https://translate" not in url and "http://webcache" not in url:
                #print("url")
                #print(url)
                #print(" ")
                try: x = di["url"]
                except:
                    if url not in lista_url: 
                        
                        di["url"] = url
                        di["texto"] = c.text
                        datos.append(di)
                        lista_url.append(url)
                count += 1
                
                #if count == 20: break
        except: print(traceback.format_exc())
    coun += 1
    #if coun == 20: break

for a in datos:
    print(a["texto"])
    print(a["url"])
    print(" ")
print(" ")
print(lista_url)

#driver.FindElement(By.CssSelector("#rightbar > .menu > li:nth-of-type(3) > h5"));
browser.implicitly_wait(55)

