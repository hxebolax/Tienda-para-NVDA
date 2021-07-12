# -*- coding: utf-8 -*-
# Copyright (C) 2020 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import globalVars
import addonHandler
import wx
import sys
import os
import pickle
import basedatos

# For translation
addonHandler.initTranslation()

dir = addonHandler._getDefaultAddonPaths()
dirDatos =os.path.join(globalVars.appArgs.configPath, "TiendaNVDA")
if os.path.exists(dirDatos) == False:
	os.mkdir(dirDatos)

class Configuracion():
	def __init__(self):

		self.local = basedatos.JsonNVDAes()
		self.servidor = self.local.dataServidor
		self.archivoConfig = os.path.join(dirDatos, "config.dat")
		self.version = 1
		self.checkbox = [False, False]
		self.complementosDisco = self.local.listaComplementosInstalados()
		self.complementosTemporal = self.local.listaComplementosInstalados()

	def GuardaDatos(self):
		p = open(	self.archivoConfig, "wb")
		pickle.dump(self.version, p)
		pickle.dump(self.checkbox, p)
		pickle.dump(self.complementosDisco, p)
		p.close()

	def CargaDatos(self):
		if os.path.isfile(self.archivoConfig):
			p = open(	self.archivoConfig, 'rb')
			self.version = pickle.load(p)
			if self.version == 1:	
				self.checkbox = pickle.load(p)
				self.complementosDisco = pickle.load(p)
			p.close()
		else:
			Configuracion.GuardaDatos(self)
			Configuracion.CargaDatos(self)

	def dict_compare(self, d1, d2):
		d1_keys = set(d1.keys())
		d2_keys = set(d2.keys())
		añadida = d1_keys - d2_keys
		if añadida == set():
			pass
		else:
			for i in añadida:
				for x in range(0, len(self.servidor)):
					if i.lower() == self.servidor[x]['summary'].lower():
						self.complementosDisco[i] = self.servidor[x]['links'][0]['channel']
		removida = d2_keys - d1_keys
		if removida == set():
			pass
		else:
			for i in removida:
				self.complementosDisco.pop(i, None)

### Cargamos configuración
config = Configuracion()
config.CargaDatos()
config.dict_compare(config.complementosTemporal, config.complementosDisco)


### Variables generales
IS_WinON = False # Bandera para saber si esta abierta una ventana del complemento
focoActual = "listboxComplementos"
ID_TRUE = wx.NewIdRef() # para botón aceptar
ID_FALSE = wx.NewIdRef() # para botón cancelar

### Variables CheckBox
ordenacion = config.checkbox[0] # Para ordenar la lista de complementos
installDescarga = config.checkbox[1] # Para instalar después de descargar
listaComplementos =  config.complementosDisco # diccionario con los complementos instalados y su canal de actualización

def GuardaValores():
	config.checkbox[0] = ordenacion
	config.checkbox[1] = installDescarga
	config.complementosDisco = listaComplementos
	config.GuardaDatos()

def ValoresDefecto():
	global ordenacion, installDescarga, listaComplementos
	ordenacion = config.checkbox[0]
	installDescarga =  config.checkbox[1]
	listaComplementos = config.complementosDisco

### Diccionario para el foco.
id_widgets = {
# WidGets generales
	1:"Panel",
	2:"textoBusqueda",
	3:"listboxComplementos",
	4:"txtResultado",
# Botones
	201:"descargarBTN",
	202:"paginaWebBTN",
	203:"salirBTN",
}
