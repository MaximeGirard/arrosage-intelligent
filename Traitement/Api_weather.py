#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 18:22:30 2018

@author: maxime
"""

#OpenWeatherMap API key f36081df884d8d7856c4b60e9aa8df65
#Garden lat, long 43.265283, -0.206671
#https://api.openweathermap.org/data/2.5/weather?lat=43.265283&lon=-0.206671&units=metric&appid=f36081df884d8d7856c4b60e9aa8df65
#Meaning https://openweathermap.org/weather-conditions

#Données à sauvegarder : Pluie (0-> non, 1-> léger, 2-> oui), Humidité, 

import meteo as mt
import database as db


meteoReference = {
            "light_rain": 500,
            "rain": {"max":781},
            "clear": {"min":800}
        }

openWeatherMapUrl = "https://api.openweathermap.org/data/2.5/weather?"
openWeatherMapForecastUrl = "https://api.openweathermap.org/data/2.5/forecast?"
parameters = "lat=43.265283&lon=-0.206671&units=metric&appid="
apiKey = "f36081df884d8d7856c4b60e9aa8df65"

config = {
	'user':'root',
    'password':'max',
    'host':'localhost',
    'database':'ArrosageIntelligent'
}

weatherDatas = {
	"temperature1" : 0,
	"temperature2" : 0,
	"humidity"     : 0,
	"moisture"     : 0,
	"pressure"     : 0,
	"rain"         : 0,
	"nextRain"     : 0,
	"lastRain"     : 0,
	"lastWatering" : 0,
	"watered"      : 0
}
    
result = mt.getContent(openWeatherMapForecastUrl + parameters + apiKey)
print(mt.nextRain(result, meteoReference))

cnx = db.initConnexion(config)

print(db.getAllDatas(cnx))

cnx.commit()

cnx.close()