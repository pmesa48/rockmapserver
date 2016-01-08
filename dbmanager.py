from pymongo import MongoClient
from bson import json_util
import json
import re

NOMBRE = 'nombre'
IMAGEN = 'imagen'
ALTURA = 'altura'
ZONA = 'zona'
PARQUE = 'parque'
PUNTO1 = 'punto1'
PUNTO2 = 'punto2'
PUNTO3 = 'punto3'
PUNTO4 = 'punto4'
PAIS = 'pais'
DIFICULTAD = 'dificultad'

class DbManager(object):

	client = None
	db = None

	def __init__(self,address,port):
		self.serverAddress = address
		self.port = port
		global client
		client = MongoClient(address,int(port))
		global db
		db = client.rock_map


	def agregar_ruta(self,imagen,nombre,altura,zona,parque,p1,p2,p3,p4,pais,dificultad):
		print 'Agregando la ruta de nombre ' + nombre
		try:
			global db
			ruta = {NOMBRE:nombre,IMAGEN:imagen,ALTURA:altura,ZONA:zona,PARQUE:parque,PUNTO1:p1,PUNTO2:p2,PUNTO3:p3,PUNTO4:p4,PAIS:pais,DIFICULTAD:dificultad}
			db.rutas.insert(ruta)
			print 'insert en bd completado'
			print ruta
			return True
		except Exception, e:
			print 'No fue posible agregar la ruta con nombre ' + nombre
			print  e
			return False

	def rutas_por_pais(self,pais):
		print 'Buscando las rutas del pais ' +  pais
		regx = re.compile("^"+pais, re.IGNORECASE)
		global db
		resultado = db.rutas.find({PAIS:regx}) 
		lista = list(resultado)
		print lista
		return json.dumps(lista,default=json_util.default)

	def agregar_parque(self,pais,nombre,p1,p2):
		global db
		try:
			parque ={NOMBRE:nombre,PAIS:pais,PUNTO1:p1,PUNTO2:p2}
			db.paises.insert(parque)
			print 'Agregando parque'
			return True
		except Exception, e:
			print e
			return False


	def parques_por_pais(self,pais):
		regx = re.compile("^"+pais, re.IGNORECASE)
		global db
		resultado = db.paises.find({PAIS:regx})
		lista = list(resultado)
		return json.dumps(lista,default=json_util.default)


