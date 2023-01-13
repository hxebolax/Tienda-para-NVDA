# -*- coding: utf-8 -*-
# Copyright (C) 2021 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import addonHandler
from logHandler import log
import globalVars
import addonAPIVersion
import traceback
import json
import re
import urllib.request
import os
import sys
from threading import Timer
from .packaging import version
from . import ajustes

ADDON_API_VERSION_REGEX = re.compile(r"^(0|\d{4})\.(\d)(?:\.(\d))?$")

def getAPIVersionTupleFromString(version):
	"""Converts a string containing an NVDA version to a tuple of the form (versionYear, versionMajor, versionMinor)"""
	match = ADDON_API_VERSION_REGEX.match(version)
	if not match:
		raise ValueError(version)
	return tuple(int(i) if i is not None else 0 for i in match.groups())

def hasAddonGotRequiredSupport(addonMin, currentAPIVersion=addonAPIVersion.CURRENT):
	"""True if NVDA provides the add-on with an API version high enough to meet the add-on's minimum requirements
	"""
	return addonMin <= currentAPIVersion

def isAddonTested(addonMax, backwardsCompatToVersion=addonAPIVersion.BACK_COMPAT_TO):
	"""True if this add-on is tested for the given API version.
	By default, the current version of NVDA is evaluated.
	"""
	return addonMax >= backwardsCompatToVersion

def isAddonCompatible(
		addonMin,
		addonMax,
		currentAPIVersion=addonAPIVersion.CURRENT,
		backwardsCompatToVersion=addonAPIVersion.BACK_COMPAT_TO
):
	"""Tests if the addon is compatible.
	The compatibility is defined by having the required features in NVDA, and by having been tested / built against
	an API version that is still supported by this version of NVDA.
	"""
	return hasAddonGotRequiredSupport(addonMin, currentAPIVersion) and isAddonTested(addonMax, backwardsCompatToVersion)

def generaFichero():
	return os.path.basename(os.path.join(globalVars.appArgs.configPath, "TiendaNVDA", "data%s.json" % len(os.listdir(os.path.join(globalVars.appArgs.configPath, "TiendaNVDA")))))

def estaenlistado(listado, buscar):
	if not buscar in listado:
		return False
	return True

def chkJson(url):
	try:
		Headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
		p = urllib.request.Request(url, headers=Headers, method="GET")
		json.loads(urllib.request.urlopen(p).read().decode("utf-8"))
		return True
	except:
		return False

def obtenFile(url):
	req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	p = urllib.request.urlopen(req).geturl()
	fichero = p.headers.get_filename()
	nombreFile = os.path.splitext(fichero)[0]
	return nombreFile

def obtenFileAlt(url):
	req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}, method="GET")
	p = urllib.request.urlopen(req).geturl()
	fichero = p.headers.get_filename()
	nombreFile = os.path.splitext(fichero)[0]
	return nombreFile

def ultimoAlternativo(url):
	try:
		req = urllib.request.Request(url, method='HEAD')
		p = urllib.request.urlopen(req)
	except:
		req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}, method="GET")
		p = urllib.request.urlopen(req).geturl()
	return p.info().get_filename()

class NVDAStoreClient(object):
	def __init__(self):
		super(NVDAStoreClient, self).__init__()

		try:
			Headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
			p = urllib.request.Request(ajustes.urlServidor, headers=Headers, method="GET")
			self.dataServidor = json.loads(urllib.request.urlopen(p).read().decode("utf-8"))
			temp = ajustes.urlServidor.split("?")
			self.urlBase = temp[0] + "?file="
			self.dataLocal = list(addonHandler.getAvailableAddons())
		except (urllib.error.HTTPError, urllib.error.URLError) as http_err:
			self.dataServidor = None
			log.info(http_err)

	def GetFilenameDownload(self, valor):
		for x in range(0, len(self.dataServidor)):
			num = len(self.dataServidor[x]['links'])
			for i in range(num):
				if self.dataServidor[x]['links'][i]['file'] == valor:
					temp = self.dataServidor[x]['links'][i]['link']
					return os.path.basename(temp)

	def GetLinkDownload(self, valor):
		for x in range(0, len(self.dataServidor)):
			num = len(self.dataServidor[x]['links'])
			for i in range(num):
				if self.dataServidor[x]['links'][i]['file'] == valor:
					return self.dataServidor[x]['links'][i]['link']

	def indiceSummary(self, valor):
		for x in range(0, len(self.dataServidor)):
			if self.dataServidor[x]['summary'].lower() == valor.lower():
				return x
		return False

	def indiceName(self, valor):
		for x in range(0, len(self.dataServidor)):
			if self.dataServidor[x]['name'].lower() == valor.lower():
				return x
		return False

	def chkVersion(self, verServidor, verLocal):
		return version.parse(verServidor) > version.parse(verLocal)

	def chkVersionAlt(self, verServidor, verLocal):
		if (verServidor > verLocal) - (verServidor < verLocal)  == -1 or  (verServidor > verLocal) - (verServidor < verLocal)  == 0:
			return False
		else:
			return True

	def chkActualizaS(self):
		lstActualizar = []
		lstUrl = []
		lstVerServidor = []
		lstVerLocal = []
		for i in ajustes.listaAddonsSave:
			for x in range(0, len(self.dataServidor)):
				if self.dataServidor[x]['name'].lower() == i[0].lower():
					if i[1] == 9:
						pass
					else:
						for z in self.dataLocal:
							if i[0].lower() == z.manifest["name"].lower():
								if not z.isPendingRemove:
									verMinima = "2019.3.0" if self.dataServidor[x]['links'][i[1]]['minimum'] == "None" else self.dataServidor[x]['links'][i[1]]['minimum']
									if isAddonCompatible(getAPIVersionTupleFromString(verMinima), getAPIVersionTupleFromString(self.dataServidor[x]['links'][i[1]]['lasttested'])):
										if self.chkVersion(self.dataServidor[x]['links'][i[1]]['version'], z.manifest["version"]) == True:
											lstActualizar.append("{}".format(z.manifest["summary"]))
											lstUrl.append(self.urlBase + self.dataServidor[x]['links'][i[1]]['file'])
											lstVerServidor.append(self.dataServidor[x]['links'][i[1]]['version'])
											lstVerLocal.append(z.manifest["version"])
										else:
											if self.chkVersionAlt(self.dataServidor[x]['links'][i[1]]['version'], z.manifest["version"]) == True:
												lstActualizar.append("{}".format(z.manifest["summary"]))
												lstUrl.append(self.urlBase + self.dataServidor[x]['links'][i[1]]['file'])
												lstVerServidor.append(self.dataServidor[x]['links'][i[1]]['version'])
												lstVerLocal.append(z.manifest["version"])
											else:
												if len(self.dataServidor[x]['links'][i[1]]['version'].replace(".", "")) >= 8:
													if self.chkVersion(self.dataServidor[x]['links'][i[1]]['version'].replace(".", ""), z.manifest["version"].replace(".", "")):
														lstActualizar.append("{}".format(z.manifest["summary"]))
														lstUrl.append(self.urlBase + self.dataServidor[x]['links'][i[1]]['file'])
														lstVerServidor.append(self.dataServidor[x]['links'][i[1]]['version'])
														lstVerLocal.append(z.manifest["version"])


		if len(lstActualizar) == 0:
			return False, False, False
		else:
			return dict(zip(lstActualizar, lstUrl)), lstVerLocal, lstVerServidor

class libreriaLocal(object):
	def __init__(self, fileJson="data.json"):
		super(libreriaLocal, self).__init__()

		self.fileJson = fileJson
		self.file = os.path.join(globalVars.appArgs.configPath, "TiendaNVDA", self.fileJson)
		self.local = list(addonHandler.getAvailableAddons())

	def fileJsonAddon(self, opcion, lista=[]):
		if opcion == 1: # Guardar
			with open(self.file, "w") as fp:
				json.dump(lista, fp)
		elif opcion == 2: # Cargar
			if os.path.isfile(self.file):
				with open(self.file, "r") as fp:
					try:
						data = json.load(fp)
						return data
					except json.decoder.JSONDecodeError:
						self.servidor = NVDAStoreClient().dataServidor
						lista = []
						for i in self.local:
							for x in range(0, len(self.servidor)):
								if i.manifest["name"].lower() == self.servidor[x]['name'].lower():
									lista.append([i.manifest['name'], 0])
						self.fileJsonAddon(1, lista)
						return lista
			else:
				self.servidor = NVDAStoreClient().dataServidor
				lista = []
				for i in self.local:
					for x in range(0, len(self.servidor)):
						if i.manifest["name"].lower() == self.servidor[x]['name'].lower():
							lista.append([i.manifest['name'], 0])
				self.fileJsonAddon(1, lista)
				return lista

	def addonsInstalados(self):
		self.servidor = NVDAStoreClient().dataServidor
		lista = []
		for i in self.local:
			for x in range(0, len(self.servidor)):
				if i.manifest["name"].lower() == self.servidor[x]['name'].lower():
					lista.append([i.manifest['name'], 0])
		return lista

	def returnNotMatches(self, a, b):
		"""Pasar dos listas, a lista guardada, b lista cargada
Devuelve 2 listas: lista1 borrar, lista2 copiar a lista1."""
		temp1 = []
		temp2 = []
		for i in range(0, len(a)):
			temp1.append(a[i][0])
		for i in range(0, len(b)):
			temp2.append(b[i][0])
		return [[x for x in temp1 if x not in temp2], [x for x in temp2 if x not in temp1]]

	def GetPos(self, lista, valor):
		temp = []
		for x in range(0, len(lista)):
			temp.append(lista[x][0])
		return temp.index(valor)

	def ordenaLista(self, lista):
		return sorted(lista, key = lambda x:(x[0], x[0]))

	def actualizaJson(self):
		p = self.returnNotMatches(ajustes.listaAddonsSave, ajustes.listaAddonsInstalados)
		if len(p[0]) == 0:
			pass # Sin items para eliminar
		else:
			temp = []
			for x in range(0, len(p[0])):
				temp.append(p[0][x])
				z = self.GetPos(ajustes.listaAddonsSave, p[0][x])
				del ajustes.listaAddonsSave[z]
		if len(p[1]) == 0:
			pass # Sin items para añadir
		else:
			temp = []
			for x in range(0, len(p[1])):
				temp.append(p[1][x])
				z = self.GetPos(ajustes.listaAddonsInstalados, p[1][x])
				ajustes.listaAddonsSave.append(ajustes.listaAddonsInstalados[z])
		self.fileJsonAddon(1, self.ordenaLista(ajustes.listaAddonsSave))

class ServidoresComplementos(object):
	def __init__(self):
		super(ServidoresComplementos, self).__init__()

		self.file = os.path.join(globalVars.appArgs.configPath, "TiendaNVDA", "servers.json")

	def fileJsonAddon(self, opcion, lista=[]):
		if opcion == 1: # Guardar
			with open(self.file, "w") as fp:
				json.dump(lista, fp)
		elif opcion == 2: # Cargar
			if os.path.isfile(self.file):
				with open(self.file, "r") as fp:
					return json.load(fp)
			else:
				lista = [[ajustes.nombreSRV_Fijo, ajustes.urlSVR_Fijo, ajustes.fileFijo]]
				self.fileJsonAddon(1, lista)
				return lista

class busquedas(object):
	def __init__(self):

		super(busquedas, self).__init__()

		self.base = NVDAStoreClient().dataServidor
		self.author = []
		self.name = []
		self.summary = []
		self.lasttested = []
		for x in range(0, len(self.base)):
			self.author.append(self.base[x]['author'])
			self.name.append(self.base[x]['name'])
			self.summary.append(self.base[x]['summary'])
			self.lasttested.append(self.base[x]['links'][0]['lasttested'])

	def indice(self, variable, busqueda):
		"""Devuelve una lista con los indices encontrados. Podemos buscar por author, name, summary, lasttested"""
		#print(busqueda().indice("lasttested", "2020"))
		return [i for i, s in enumerate(			eval("self.{}".format(variable))) if busqueda in s]

	def strBusqueda(self, variable, busqueda):
		"""Devuelve una lista con los strings encontrados. Podemos buscar por author, name, summary, lasttested"""
		# Ejemplo: print(busquedas().strBusqueda("summary", "Tienda"))
		return [item for item in eval("self.{}".format(variable)) if busqueda.lower() in item.lower()]

	def completeRetSearch(self, variable, busqueda):
		"""Devuelbe json con todos los valores tomados del servidor, aquellos que coincidan con la busqueda"""
		# Ejemplo: print(busquedas().completeRetSearch("['links'][0]['lasttested'].split('.')[0]", "2021"))
		return [x for x in self.base if eval("x{}".format(variable)) == busqueda]

class RepeatTimer(object):
	def __init__(self, interval, function, *args, **kwargs):

		self._timer     = None
		self.interval   = interval
		self.function   = function
		self.args       = args
		self.kwargs     = kwargs
		self.is_running = False

		self.daemon = True
		self.start()

	def _run(self):
		self.is_running = False
		self.start()
		self.function(*self.args, **self.kwargs)

	def start(self):
		if not self.is_running:
			self._timer = Timer(self.interval, self._run)
			self._timer.start()
			self.is_running = True

	def stop(self):
		self._timer.cancel()
		self.is_running = False

