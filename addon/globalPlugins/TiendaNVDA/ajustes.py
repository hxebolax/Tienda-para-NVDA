# -*- coding: utf-8 -*-
# Copyright (C) 2021-2025 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.
#
# Módulo de ajustes para TiendaNVDA_Modern
#

import globalVars
import addonHandler
import config
import wx
import os
import shutil

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
		"oficialChk": "boolean(default=True)",
		"allowIncompatibleChk": "boolean(default=False)",
		"chkOfficialUpdates": "boolean(default=True)",
		"useTranslationCache": "boolean(default=True)",
		"listCacheEnabled": "boolean(default=True)",
		"autoBackupOnExit": "boolean(default=True)",
		"silentInstall": "boolean(default=False)",
		"serverCache": "boolean(default=True)",
		"cacheInterval": "integer(default=3, min=0, max=6)",
	}
	config.conf.spec['TiendaNVDA_Modern'] = confspec


def getConfig(key):
	return config.conf["TiendaNVDA_Modern"][key]


def setConfig(key, value):
	try:
		config.conf.profiles[0]["TiendaNVDA_Modern"][key] = value
	except:
		config.conf["TiendaNVDA_Modern"][key] = value


# Variables temporales
tempChk = None
tempTimer = None
tempOrden = None
tempInstall = None
tempTrans = None
tempLang = None
dirDatos = None
listaAddonsSave = None
listaAddonsInstalados = None

# Variables para tienda oficial
tempOficial = None
tempAllowIncompatible = None
tempChkOfficial = None

# Variables de caché y backup
tempUseTranslationCache = None
tempListCacheEnabled = None
tempAutoBackupOnExit = None
tempSilentInstall = None
tempServerCache = None
tempCacheInterval = None

# Valores para servidores
urlServidor = None
selectSRV = None
nombreSRV_Fijo = _("Servidor comunidad hispanohablante")
urlSVR_Fijo = "https://nvda.es/files/get.php?addonslist"
fileFijo = "data.json"
listaServidores = []


def setup():
	global listaAddonsSave, listaAddonsInstalados, tempInstall, dirDatos
	global tempOrden, tempChk, tempTimer, tempTrans, tempLang
	global urlServidor, selectSRV, listaServidores
	global tempOficial, tempAllowIncompatible, tempChkOfficial
	global tempUseTranslationCache, tempListCacheEnabled, tempAutoBackupOnExit
	global tempSilentInstall, tempServerCache, tempCacheInterval, IS_TEMPORAL

	from . import basedatos

	initConfiguration()
	tempChk = getConfig("autoChk")
	tempTimer = getConfig("timerChk")
	tempTrans = getConfig("autoLang")
	tempLang = getConfig("langTrans")
	tempOrden = getConfig("ordenChk")
	tempInstall = getConfig("installChk")
	urlServidor = getConfig("urlServidor")
	selectSRV = getConfig("selectSRV")
	tempOficial = getConfig("oficialChk")
	tempAllowIncompatible = getConfig("allowIncompatibleChk")
	tempChkOfficial = getConfig("chkOfficialUpdates")
	tempUseTranslationCache = getConfig("useTranslationCache")
	tempListCacheEnabled = getConfig("listCacheEnabled")
	tempAutoBackupOnExit = getConfig("autoBackupOnExit")
	tempSilentInstall = getConfig("silentInstall")
	tempServerCache = getConfig("serverCache")
	tempCacheInterval = getConfig("cacheInterval")

	dirDatos = os.path.join(globalVars.appArgs.configPath, "TiendaNVDA_Modern")
	if not os.path.exists(dirDatos):
		os.mkdir(dirDatos)
	else:
		for f in os.listdir(dirDatos):
			if f.endswith(".nvda-addon") and f.startswith("temp_install"):
				try:
					os.remove(os.path.join(dirDatos, f))
				except:
					pass
		tempPath = os.path.join(dirDatos, "temp")
		if os.path.exists(tempPath):
			try:
				shutil.rmtree(tempPath, ignore_errors=True)
			except:
				pass

	IS_TEMPORAL = True
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
	finally:
		IS_TEMPORAL = False


# Título de la aplicación
titulo = _("Tienda de Complementos NVDA")

# Estados
IS_WinON = False
IS_Download = False
IS_TEMPORAL = False
reiniciarTrue = False
focoActual = "listboxComplementos"
indiceFiltro = 100

# IDs para botones
ID_TRUE = wx.NewIdRef()
ID_FALSE = wx.NewIdRef()

# Contadores
contadorRepeticion = 0
contadorRepeticionSn = 0

# Lista tiempo chk notificaciones
tiempoChk = [
	_("15 minutos"),
	_("30 minutos"),
	_("45 minutos"),
	_("1 hora"),
	_("12 horas"),
	_("1 día"),
	_("1 semana")
]

# Lista con idiomas para las traducciones
langLST = [
	_("Alemán"),
	_("Árabe"),
	_("Croata"),
	_("Español"),
	_("Francés"),
	_("Inglés"),
	_("Italiano"),
	_("Polaco"),
	_("Portugués"),
	_("Ruso"),
	_("Turco"),
	_("Ucraniano")
]

langDict = {
	0: "de", 1: "ar", 2: "hr", 3: "es", 4: "fr", 5: "en",
	6: "it", 7: "pl", 8: "pt", 9: "ru", 10: "tr", 11: "uk",
}

id_widgets = {
	1: "Panel", 2: "textoBusqueda", 3: "listboxComplementos", 4: "txtResultado",
	201: "descargarBTN", 202: "paginaWebBTN", 203: "cambiarSrvBTN", 204: "salirBTN",
}

tiempoDict = {
	0: 900, 1: 1800, 2: 2700, 3: 3600, 4: 43200, 5: 86400, 6: 604800,
}

OFFICIAL_CHANNELS = {
	"all": _("Todos"), "stable": _("Estable"), "beta": _("Beta"),
	"dev": _("Desarrollo"), "external": _("Externo"),
}

OFFICIAL_STORE_BASE_URL = "https://addonStore.nvaccess.org"
OFFICIAL_CACHE_HASH_URL = f"{OFFICIAL_STORE_BASE_URL}/cacheHash.json"


def getOfficialStoreURL(channel: str, lang: str, apiVersion: str) -> str:
	return f"{OFFICIAL_STORE_BASE_URL}/{lang}/{channel}/{apiVersion}.json"
