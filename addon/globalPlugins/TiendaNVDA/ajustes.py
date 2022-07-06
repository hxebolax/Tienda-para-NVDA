# -*- coding: utf-8 -*-
# Copyright (C) 2021 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import globalVars
import addonHandler
import config
import wx
import os
import shutil
from . import basedatos

# For translation
addonHandler.initTranslation()

def initConfiguration():
	confspec = {
		"autoChk": "boolean(default=False)",
		"timerChk": "integer(default=1, min=0, max=6)",
		"ordenChk": "boolean(default=False)",
		"installChk": "boolean(default=False)",
		"autoLang": "boolean(default=False)",
		"langTrans": "integer(default=5, min=0, max=11)",
		"selectSRV": "integer(default=0, min=0)",
		"urlServidor": "string(default='https://nvda.es/files/get.php?addonslist')",
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

tempChk = None
tempTimer = None
tempOrden = None
tempInstall = None
tempTrans = None
tempLang = None
dirDatos = None
listaAddonsSave = None
listaAddonsInstalados = None
# Valores para todo lo referido con los servidores
urlServidor = None
selectSRV = None
nombreSRV_Fijo = _("Servidor comunidad hispanohablante")
urlSVR_Fijo ="https://nvda.es/files/get.php?addonslist" # "https://nvda-addons.org/files/get.php?addonslist"
fileFijo = "data.json"
listaServidores = []

def setup():
	global listaAddonsSave, listaAddonsInstalados, tempInstall, dirDatos, tempOrden, tempChk, tempTimer, tempTrans, tempLang, urlServidor, selectSRV, listaServidores
	initConfiguration()
	tempChk = getConfig("autoChk")
	tempTimer = getConfig("timerChk")
	tempTrans = getConfig("autoLang")
	tempLang = getConfig("langTrans")
	tempOrden = getConfig("ordenChk")
	tempInstall = getConfig("installChk")
	urlServidor = getConfig("urlServidor")
	selectSRV = getConfig("selectSRV")
	dirDatos =os.path.join(globalVars.appArgs.configPath, "TiendaNVDA")
	if os.path.exists(dirDatos) == False:
		os.mkdir(dirDatos)
	else:
		if os.path.exists(os.path.join(dirDatos, "temp")) == True:
			try:
				shutil.rmtree(os.path.join(dirDatos, "temp"), ignore_errors=True)
			except:
				pass
	listaServidores = basedatos.ServidoresComplementos().fileJsonAddon(2)
	try:
		listaAddonsSave = basedatos.libreriaLocal(listaServidores[selectSRV][2]).fileJsonAddon(2)
		listaAddonsInstalados = basedatos.libreriaLocal().addonsInstalados()
		basedatos.libreriaLocal(listaServidores[selectSRV][2]).actualizaJson()
	except:
		urlServidor = urlSVR_Fijo
		selectSRV = 0
		listaAddonsSave = basedatos.libreriaLocal(listaServidores[selectSRV][2]).fileJsonAddon(2)
		listaAddonsInstalados = basedatos.libreriaLocal().addonsInstalados()
		basedatos.libreriaLocal(listaServidores[selectSRV][2]).actualizaJson()

titulo = _("Tienda NVDA.ES")
IS_WinON = False
IS_Download = False
IS_TEMPORAL =False
reiniciarTrue = False
focoActual = "listboxComplementos"
indiceFiltro = 6
ID_TRUE = wx.NewIdRef() # para botón aceptar
ID_FALSE = wx.NewIdRef() # para botón cancelar
contadorRepeticion = 0
contadorRepeticionSn = 0

# Lista tiempo chk notificaciones
tiempoChk = [_("15 minutos"), _("30 minutos"), _("45 minutos"), _("1 hora"), _("12 horas"), _("1 día"), _("1 semana")]
# Lista con idiomas para las traducciones
langLST = [_("Alemán"), _("Árabe"), _("Croata"), _("Español"), _("Francés"), _("Inglés"), _("Italiano"), _("Polaco"), _("Portugués"), _("Ruso"), _("Turco"), _("Ucraniano")]
# Diccionario con las abreviaturas de idioma
langDict = {
	0:"de",
	1:"ar",
	2:"hr",
	3:"es",
	4:"fr",
	5:"en",
	6:"it",
	7:"pl",
	8:"pt",
	9:"ru",
	10:"tr",
	11:"uk",
}
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
	203:"cambiarSrvBTN",
	204:"salirBTN",
}

tiempoDict = {
	0:900,
	1:1800,
	2:2700,
	3:3600,
	4:43200,
	5:86400,
	6:604800,
}
