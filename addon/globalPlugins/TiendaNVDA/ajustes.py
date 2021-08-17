# -*- coding: utf-8 -*-
# Copyright (C) 2021 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import globalVars
import addonHandler
import config
import wx
import os
import sys
import shutil
import basedatos

# For translation
addonHandler.initTranslation()

def initConfiguration():
	confspec = {
		"autoChk": "boolean(default=False)",
		"timerChk": "integer(default=1, min=0, max=3)",
		"ordenChk": "boolean(default=False)",
		"installChk": "boolean(default=False)",
	}
	config.conf.spec['TiendaES'] = confspec

def getConfig(key):
	value = config.conf["TiendaES"][key]
	return value

def setConfig(key, value):
	try:
		config.conf.profiles[0]["TiendaES"][key] = value
	except:
		config.conf["TiendaES"][key] = value

initConfiguration()
tempChk = getConfig("autoChk")
tempTimer = getConfig("timerChk")
tempOrden = getConfig("ordenChk")
tempInstall = getConfig("installChk")

dirDatos =os.path.join(globalVars.appArgs.configPath, "TiendaNVDA")
if os.path.exists(dirDatos) == False:
	os.mkdir(dirDatos)
else:
	if os.path.exists(os.path.join(dirDatos, "temp")) == True:
		try:
			shutil.rmtree(os.path.join(dirDatos, "temp"), ignore_errors=True)
		except:
			pass

IS_WinON = False
IS_Download = False
reiniciarTrue = False
focoActual = "listboxComplementos"
ID_TRUE = wx.NewIdRef() # para botón aceptar
ID_FALSE = wx.NewIdRef() # para botón cancelar
contadorRepeticion = 0
contadorRepeticionSn = 0
listaAddonsSave = basedatos.libreriaLocal().fileJsonAddon(2)
listaAddonsInstalados = basedatos.libreriaLocal().addonsInstalados()
basedatos.libreriaLocal().actualizaJson()

# Lista tiempo chk notificaciones
tiempoChk = [_("15 minutos"), _("30 minutos"), _("45 minutos"), _("1 hora")]

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

tiempoDict = {
	0:900,
	1:1800,
	2:2700,
	3:3600,
}
