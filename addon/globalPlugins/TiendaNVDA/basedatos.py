# -*- coding: utf-8 -*-
# Copyright (C) 2021-2025 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.
#
# Módulo de base de datos para TiendaNVDA_Modern
# Maneja la conexión con servidores NVDA.ES y datos locales
#

import addonHandler
from logHandler import log
import globalVars
import json
import os
import time
from threading import Timer
from typing import Optional, List, Dict, Tuple
from . import ajustes
from . import red
from . import version_utils
from .cache_manager import CacheManager

addonHandler.initTranslation()


def _get_cache_manager():
	"""Obtiene una instancia de CacheManager con la configuración actual"""
	return CacheManager(
		ajustes.dirDatos,
		ajustes.tiempoDict,
		lambda: ajustes.tempCacheInterval,
		lambda: ajustes.tempServerCache,
		lambda: ajustes.tempUseTranslationCache,
	)


class NVDAStoreClient:
	"""Cliente para la tienda NVDA.ES con caché en memoria"""

	_isOffline = {}

	def __init__(self, useCache: bool = True, forceRefresh: bool = False):
		super().__init__()
		self.dataServidor = None
		self.urlBase = None
		self.dataLocal = None
		self.isOffline = False
		self.cacheMgr = _get_cache_manager()

		try:
			ignore_ttl = not forceRefresh and ajustes.IS_TEMPORAL
			cached_data, timestamp = self.cacheMgr.getStoreCache(ajustes.urlServidor, ignore_ttl=ignore_ttl)

			if not forceRefresh and cached_data:
				self.dataServidor = cached_data
				self.isOffline = NVDAStoreClient._isOffline.get(ajustes.urlServidor, False)
				self._refreshLocalInfo()
				return

			data = red.get_json(ajustes.urlServidor, timeout=20)
			if data is not None:
				self.dataServidor = data
				NVDAStoreClient._isOffline[ajustes.urlServidor] = False
				self.cacheMgr.saveStoreCache(ajustes.urlServidor, self.dataServidor)
				self._refreshLocalInfo()
			else:
				raise ConnectionError("No se pudo conectar")
		except Exception as e:
			if useCache and ajustes.tempListCacheEnabled:
				cached_data, timestamp = self.cacheMgr.getStoreCache(ajustes.urlServidor, ignore_ttl=True)
				if cached_data:
					self.dataServidor = cached_data
					NVDAStoreClient._isOffline[ajustes.urlServidor] = True
					self.isOffline = True
					self._refreshLocalInfo()
				else:
					self.dataServidor = None
			else:
				self.dataServidor = None

	def _refreshLocalInfo(self):
		if not ajustes.urlServidor:
			return
		temp = ajustes.urlServidor.split("?")
		self.urlBase = temp[0] + "?file="
		self.dataLocal = list(addonHandler.getAvailableAddons())

	def GetFilenameDownload(self, valor: str) -> Optional[str]:
		if not self.dataServidor:
			return None
		for x in range(len(self.dataServidor)):
			for i in range(len(self.dataServidor[x]['links'])):
				if self.dataServidor[x]['links'][i]['file'] == valor:
					return os.path.basename(self.dataServidor[x]['links'][i]['link'])
		return None

	def GetLinkDownload(self, valor: str) -> Optional[str]:
		if not self.dataServidor:
			return None
		for x in range(len(self.dataServidor)):
			for i in range(len(self.dataServidor[x]['links'])):
				if self.dataServidor[x]['links'][i]['file'] == valor:
					return self.dataServidor[x]['links'][i]['link']
		return None

	def indiceSummary(self, valor: str) -> Optional[int]:
		if not self.dataServidor:
			return None
		for x in range(len(self.dataServidor)):
			if self.dataServidor[x]['summary'].lower() == valor.lower():
				return x
		return None

	def indiceName(self, valor: str) -> Optional[int]:
		if not self.dataServidor:
			return None
		for x in range(len(self.dataServidor)):
			if self.dataServidor[x]['name'].lower() == valor.lower():
				return x
		return None

	def chkVersion(self, verServidor: str, verLocal: str) -> bool:
		try:
			return version_utils.parse(verServidor) > version_utils.parse(verLocal)
		except:
			return self.chkVersionAlt(verServidor, verLocal)

	def chkVersionAlt(self, verServidor: str, verLocal: str) -> bool:
		try:
			return (verServidor > verLocal) - (verServidor < verLocal) == 1
		except:
			return False

	def chkActualizaS(self, includeIncompatible: bool = False) -> Tuple[Optional[Dict], Optional[List], Optional[List]]:
		lstActualizar = []
		lstUrl = []
		lstVerServidor = []
		lstVerLocal = []

		if not self.dataServidor:
			return None, None, None
		if not self.dataLocal:
			self.dataLocal = list(addonHandler.getAvailableAddons())

		for installedAddon in self.dataLocal:
			if installedAddon.isPendingRemove:
				continue
			addonName = installedAddon.manifest["name"].lower()
			verLocal = installedAddon.manifest["version"]

			for x in range(len(self.dataServidor)):
				if self.dataServidor[x]['name'].lower() == addonName:
					canalIdx = 0
					for savedAddon in ajustes.listaAddonsSave:
						if savedAddon[0].lower() == addonName:
							if savedAddon[1] == 9:
								canalIdx = -1
							else:
								canalIdx = int(savedAddon[1])
							break
					if canalIdx == -1:
						break
					if canalIdx >= len(self.dataServidor[x]['links']):
						canalIdx = 0
					link = self.dataServidor[x]['links'][canalIdx]
					verServidor = link['version']
					verMinima = "2019.3.0" if link.get('minimum') == "None" else link.get('minimum', "2019.3.0")
					try:
						compatible = True
						if not includeIncompatible:
							compatible = version_utils.isAddonCompatible(
								version_utils.getAPIVersionTupleFromString(verMinima),
								version_utils.getAPIVersionTupleFromString(link['lasttested'])
							)
						if compatible and self.chkVersion(verServidor, verLocal):
							lstActualizar.append(f"{addonName} - {installedAddon.manifest['summary']}")
							lstUrl.append(self.urlBase + link['file'])
							lstVerServidor.append(verServidor)
							lstVerLocal.append(verLocal)
					except Exception as e:
						log.debug(f"Error al comprobar compatibilidad de {addonName}: {e}")
						continue
					break

		if len(lstActualizar) == 0:
			return None, None, None
		return dict(zip(lstActualizar, lstUrl)), lstVerLocal, lstVerServidor


class libreriaLocal:
	"""Maneja la base de datos local de complementos"""

	def __init__(self, fileJson: str = "data.json"):
		self.fileJson = fileJson
		self.file = os.path.join(globalVars.appArgs.configPath, "TiendaNVDA_Modern", self.fileJson)
		self.local = list(addonHandler.getAvailableAddons())

	def fileJsonAddon(self, opcion: int, lista: List = None) -> Optional[List]:
		if lista is None:
			lista = []
		if opcion == 1:
			with open(self.file, "w", encoding="utf-8") as fp:
				json.dump(lista, fp, ensure_ascii=False)
			return None
		elif opcion == 2:
			if os.path.isfile(self.file):
				try:
					with open(self.file, "r", encoding="utf-8") as fp:
						return json.load(fp)
				except json.decoder.JSONDecodeError:
					self.servidor = NVDAStoreClient().dataServidor
					lista = []
					if self.servidor:
						for i in self.local:
							for x in range(len(self.servidor)):
								if i.manifest["name"].lower() == self.servidor[x]['name'].lower():
									lista.append([i.manifest['name'], 0])
					self.fileJsonAddon(1, lista)
					return lista
			else:
				self.servidor = NVDAStoreClient().dataServidor
				lista = []
				if self.servidor:
					for i in self.local:
						for x in range(len(self.servidor)):
							if i.manifest["name"].lower() == self.servidor[x]['name'].lower():
								lista.append([i.manifest['name'], 0])
				self.fileJsonAddon(1, lista)
				return lista
		return None

	def addonsInstalados(self) -> List:
		self.servidor = NVDAStoreClient().dataServidor
		lista = []
		if self.servidor:
			nombres_servidor = {s['name'].lower() for s in self.servidor}
			for i in self.local:
				if i.manifest["name"].lower() in nombres_servidor:
					lista.append([i.manifest['name'], 0])
		return lista

	def returnNotMatches(self, a: List, b: List) -> List[List]:
		set_a = {item[0] for item in a}
		set_b = {item[0] for item in b}
		return [[x for x in set_a if x not in set_b], [x for x in set_b if x not in set_a]]

	def GetPos(self, lista: List, valor: str) -> int:
		for i, item in enumerate(lista):
			if item[0] == valor:
				return i
		raise ValueError(f"{valor} no está en la lista")

	def ordenaLista(self, lista: List) -> List:
		return sorted(lista, key=lambda x: (x[0].lower(), x[0].lower()))

	def actualizaJson(self):
		p = self.returnNotMatches(ajustes.listaAddonsSave, ajustes.listaAddonsInstalados)
		if len(p[0]) > 0:
			for x in range(len(p[0])):
				z = self.GetPos(ajustes.listaAddonsSave, p[0][x])
				del ajustes.listaAddonsSave[z]
		if len(p[1]) > 0:
			for x in range(len(p[1])):
				z = self.GetPos(ajustes.listaAddonsInstalados, p[1][x])
				ajustes.listaAddonsSave.append(ajustes.listaAddonsInstalados[z])
		self.fileJsonAddon(1, self.ordenaLista(ajustes.listaAddonsSave))


class ServidoresComplementos:
	def __init__(self):
		self.file = os.path.join(globalVars.appArgs.configPath, "TiendaNVDA_Modern", "servers.json")

	def fileJsonAddon(self, opcion: int, lista: List = None) -> Optional[List]:
		if lista is None:
			lista = []
		if opcion == 1:
			with open(self.file, "w", encoding="utf-8") as fp:
				json.dump(lista, fp, ensure_ascii=False)
			return None
		elif opcion == 2:
			if os.path.isfile(self.file):
				try:
					with open(self.file, "r", encoding="utf-8") as fp:
						return json.load(fp)
				except:
					lista = [[ajustes.nombreSRV_Fijo, ajustes.urlSVR_Fijo, ajustes.fileFijo]]
					self.fileJsonAddon(1, lista)
					return lista
			else:
				lista = [[ajustes.nombreSRV_Fijo, ajustes.urlSVR_Fijo, ajustes.fileFijo]]
				self.fileJsonAddon(1, lista)
				return lista
		return None


class busquedas:
	def __init__(self):
		self.base = NVDAStoreClient().dataServidor
		self.author = []
		self.name = []
		self.summary = []
		self.lasttested = []
		if self.base:
			for x in range(len(self.base)):
				self.author.append(self.base[x].get('author', ''))
				self.name.append(self.base[x].get('name', ''))
				self.summary.append(self.base[x].get('summary', ''))
				if self.base[x].get('links') and len(self.base[x]['links']) > 0:
					self.lasttested.append(self.base[x]['links'][0].get('lasttested', ''))

	def indice(self, variable: str, busqueda: str) -> List[int]:
		data = getattr(self, variable, [])
		return [i for i, s in enumerate(data) if busqueda in s]

	def strBusqueda(self, variable: str, busqueda: str) -> List[str]:
		data = getattr(self, variable, [])
		return [item for item in data if busqueda.lower() in item.lower()]

	def completeRetSearch(self, variable: str, busqueda: str) -> List[Dict]:
		if not self.base:
			return []
		try:
			return [x for x in self.base if eval(f"x{variable}") == busqueda]
		except:
			return []


class RepeatTimer:
	def __init__(self, interval: float, function, *args, **kwargs):
		self._timer = None
		self.interval = interval
		self.function = function
		self.args = args
		self.kwargs = kwargs
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
			self._timer.daemon = True
			self._timer.start()
			self.is_running = True

	def stop(self):
		if self._timer:
			self._timer.cancel()
		self.is_running = False
