#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 19:42:48 2018

@author: maxime

Ce fichier regroupe l'ensemble des fonctions méteos et d'appels à l'API openweathermap
"""
import requests
import json

#retourne le contenu d'une page web sour la forme de texte brut ou d'un objet 
def getContent(url, isJson = True):
    if isJson:
        return json.loads(requests.get(url).text)
    else:
        return requests.get(url).text

#pleut il ?
def isItRainy(id, meteoReference):
    if id == meteoReference["light_rain"]:
        return 1
    elif id <= meteoReference["rain"]["max"] and id != meteoReference["light_rain"]:
        return 2
    elif id >= meteoReference["clear"]["min"]:
        return 0

#retourne le nombre d'heure avant la prochaine pluie... retourne 7*24 si aucune pluie n'est prévue
def nextRain(object, meteoReference, sensibility = 1):
    list_rain = object["list"]
    for prevision in list_rain:
        id_rain = prevision["weather"][0]["id"]
        if isItRainy(id_rain, meteoReference) >= sensibility:
            return list_rain.index(prevision)*3
        else:
            pass
            #print(prevision["weather"][0]["description"] + "\n")
    return 24*7 #Par défaut, et pour ne pas "se mouiller" (HAHA) on part du principe qu'il pleut dans au minimum 7 jours
     