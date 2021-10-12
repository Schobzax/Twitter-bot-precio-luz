#Imports.
import tweepy
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
from datetime import date
import credenciales
import os

auth = tweepy.OAuthHandler(credenciales.con_key, credenciales.con_sec) # Authenticate
auth.set_access_token(credenciales.acc_tok, credenciales.acc_sec) # Grant Access

api = tweepy.API(auth) # connect to API

# Datos de la página web

print(os.getcwd())
os.chdir(credenciales.workdir)
print(os.getcwd())

driver = webdriver.Chrome("chromedriver.exe")

precioLuzMedio = 0; # id="spain_average";
precioLuzMaximo = 0; # id="spain_max";

driver.get("https://www.omie.es/")

time.sleep(5)

content = driver.page_source.encode('utf-8').strip()
soup = BeautifulSoup(content, "html.parser")

precioLuzMedio = soup.find(id="spain_average").getText()
precioLuzMaximo = soup.find(id="spain_max").getText()

driver.quit()

#Extracción de datos
with open('twitter_bot.json') as json_file:
    datos = json.loads(json_file.read())
fechaMax = datos["fechaMax"]
fechaMedia = datos["fechaMedia"]
numeroMax = datos["numeroMax"]
numeroMedia = datos["numeroMedia"]

#Gestión del guardado (para más adelante)
guardaFechaMax = fechaMax
guardaFechaMedia = fechaMedia
guardaNumeroMax = numeroMax
guardaNumeroMedia = numeroMedia

#Gestión fechaMax
fechaExtraidaMax = datetime.strptime(fechaMax, '%Y-%m-%d')
fechaExtraidaMax = fechaExtraidaMax.date()

ndiasMax = (date.today() - fechaExtraidaMax).days

#Gestión récord max
if(ndiasMax == 0):
    recordMax = "⚡¡Nuevo récord!⚡ (Anterior: "+str(numeroMax)+" €/mWh, ocurrido el "+fechaExtraidaMax.strftime("%d/%m/%Y")+")"
    guardaFechaMax = date.today()
    guardaNumeroMax = float(precioLuzMaximo)
else:
    recordMax = str(ndiasMax)+" días desde el último récord ("+str(numeroMax)+" €/mWh, el "+fechaExtraidaMax.strftime("%d/%m/%Y")+")"

#Gestión fechaMedia
fechaExtraidaMedia = datetime.strptime(fechaMedia, '%Y-%m-%d')
fechaExtraidaMedia = fechaExtraidaMedia.date()

ndiasMedia = (date.today() - fechaExtraidaMedia).days

#Gestión récord media
if(ndiasMedia == 0):
    recordMedia = "⚡¡Nuevo récord!⚡ (Anterior: "+str(numeroMedia)+" €/mWh, ocurrido el "+fechaExtraidaMedia.strftime("%d/%m/%Y")+")"
    guardaFechaMedia = date.today()
    guardaNumeroMedia = float(precioLuzMedio)
else:
    recordMedia = str(ndiasMedia)+" días desde el último récord ("+str(numeroMedia)+" €/mWh, el "+fechaExtraidaMedia.strftime("%d/%m/%Y")+")"


#Guardado de datos
datos = {
    "fechaMax":guardaFechaMax,
    "fechaMedia":guardaFechaMedia,
    "numeroMax":guardaNumeroMax,
    "numeroMedia":guardaNumeroMedia
}

with open('twitter_bot.json','w') as json_file:
    #Y aquí se guardan los datos actualizados.
    json.dump(datos,json_file)

#Composición del tuit
tuit_content = ("Buenos días💡 Estos son los precios de hoy día "+(date.today()).strftime("%d/%m/%Y")+" para España:\n"
               "Precio medio de España: "+precioLuzMedio+" €/mWh - "+recordMedia+"\n"
               "Precio máximo de España: "+precioLuzMaximo+" €/mWh - "+recordMax+"\n"
               "\n#PrecioLuz")

print(tuit_content)

###api.update_status(tuit_content) #-> El Tuiterino