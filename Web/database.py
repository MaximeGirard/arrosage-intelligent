#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 17:22:36 2018

@author: maxime
Ce fichier regroupe l'ensemble des fonctions de connexions à la base de données mysql
"""

import mysql.connector
from mysql.connector import errorcode
import random, datetime

#retourne un objet "connecteur" à la base de données
def initConnexion(config):
	try:
		cnx = mysql.connector.connect(**config)
	except mysql.connector.Error as err:
	  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
	    print("Something is wrong with your user name or password")
	  elif err.errno == errorcode.ER_BAD_DB_ERROR:
	    print("Database does not exist")
	  else:
	    print(err)

	return cnx

#ajoute une entrée à la base de données
def addDataToDatabase(cnx, datas):
	cursor = cnx.cursor()
	addWeatherDatas = ("INSERT INTO weatherDatas "
					   "(temperature1, temperature2, humidity, moisture, pressure, rain, nextRain, lastRain, lastWatering, watered) "
					   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
	weatherDatas = (datas["temperature1"], datas["temperature2"], datas["humidity"], datas["moisture"], datas["pressure"],
					datas["rain"], datas["nextRain"], datas["lastRain"], datas["lastWatering"], datas["watered"])
	cursor.execute(addWeatherDatas, weatherDatas)
	id = cursor.lastrowid
	cursor.close()
	return id

def getAllDatas(cnx):
	cursor = cnx.cursor()
	query = ("SELECT * FROM weatherDatas ORDER BY id")
	cursor.execute(query)
	datas = cursor.fetchall()
	return datas

#retourne le nombre d'heure depuis la dernière pluie
def getLastRain(cnx):
	cursor = cnx.cursor()
	query = ("SELECT date FROM weatherDatas "
			 "WHERE rain = 1 ORDER by date DESC LIMIT 1 ")
	cursor.execute(query)

	dr = cursor.fetchone()[0]
	dn = datetime.datetime.now()
	dd = dn-dr
	hours = dd.total_seconds()//3600

	return hours

def getLastWatering(cnx):
	cursor = cnx.cursor()
	query = ("SELECT date FROM weatherDatas "
			 "WHERE watered = 1 ORDER by date DESC LIMIT 1 ")
	cursor.execute(query)

	dr = cursor.fetchone()[0]
	dn = datetime.datetime.now()
	dd = dn-dr
	hours = dd.total_seconds()//3600

	return hours

#TEST UNIQUEMENT ! Ajoute des données aleatoire à la base de donnée
def addRandomValues(cnx, n = 1):
	for i in range(0, n):
		datas = {
			"temperature1" : random.randint(15,30),
			"temperature2" : random.randint(15,30),
			"humidity"     : random.randint(0,100),
			"moisture"     : random.randint(0,100),
			"pressure"     : random.randint(990,1020),
			"rain"         : random.randint(0,1),
			"nextRain"     : random.randint(0,200),
			"lastRain"     : random.randint(0,200),
			"lastWatering" : random.randint(0,200),
			"watered"      : random.randint(0,1)
			}
		addDataToDatabase(cnx, datas)

"""
config = {
	'user':'root',
    'password':'max',
    'host':'localhost',
    'database':'ArrosageIntelligent'
}

cnx = initConnexion(config)

print(getAllDatas(cnx))

cnx.commit()
cnx.close()
"""