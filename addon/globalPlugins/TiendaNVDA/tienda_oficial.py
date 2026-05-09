# -*- coding: utf-8 -*-
# Copyright (C) 2021-2025 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.
#
# Módulo para integrar la tienda oficial de NVDA (Add-on Store)
#

import addonHandler
from logHandler import log
import addonAPIVersion
import languageHandler
import json
import os
import hashlib
import time
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum
from threading import Lock
from . import red
from . import version_utils

addonHandler.initTranslation()

OFFICIAL_STORE_BASE_URL = "https://addonStore.nvaccess.org"
OFFICIAL_CACHE_HASH_URL = f"{OFFICIAL_STORE_BASE_URL}/cacheHash.json"
FETCH_TIMEOUT = 60
LATEST_API_VER = "latest"


class Channel(Enum):
	ALL = "all"
	STABLE = "stable"
	BETA = "beta"
	DEV = "dev"
	EXTERNAL = "external"

	@property
	def displayName(self) -> str:
		labels = {
			Channel.ALL: _("Todos"), Channel.STABLE: _("Estable"),
			Channel.BETA: _("Beta"), Channel.DEV: _("Desarrollo"),
			Channel.EXTERNAL: _("Externo"),
		}
		return labels.get(self, self.value)


@dataclass
class OfficialAddon:
	addonId: str
	displayName: str
	description: str
	publisher: str
	addonVersionName: str
	channel: str
	homepage: Optional[str]
	license: str
	licenseURL: Optional[str]
	sourceURL: str
	URL: str
	sha256: str
	minNVDAVersion: Tuple[int, int, int]
	lastTestedVersion: Tuple[int, int, int]
	reviewURL: Optional[str] = None
	legacy: bool = False
	changelog: Optional[str] = None
	submissionTime: Optional[int] = None

	@property
	def isCompatible(self) -> bool:
		return (
			self.minNVDAVersion <= addonAPIVersion.CURRENT and
			self.lastTestedVersion >= addonAPIVersion.BACK_COMPAT_TO
		)

	@property
	def channelDisplay(self) -> str:
		channels = {
			"stable": _("Estable"), "beta": _("Beta"),
			"dev": _("Desarrollo"), "external": _("Externo"),
		}
		return channels.get(self.channel, self.channel)

	def toDict(self) -> Dict[str, Any]:
		return {
			'addonId': self.addonId, 'displayName': self.displayName,
			'description': self.description, 'publisher': self.publisher,
			'addonVersionName': self.addonVersionName, 'channel': self.channel,
			'homepage': self.homepage, 'license': self.license,
			'licenseURL': self.licenseURL, 'sourceURL': self.sourceURL,
			'URL': self.URL, 'sha256': self.sha256,
			'minNVDAVersion': self.minNVDAVersion,
			'lastTestedVersion': self.lastTestedVersion,
			'reviewURL': self.reviewURL, 'legacy': self.legacy,
			'changelog': self.changelog, 'submissionTime': self.submissionTime,
		}


class OfficialStoreClient:
	_instance = None
	_lock = Lock()

	def __new__(cls):
		with cls._lock:
			if cls._instance is None:
				cls._instance = super().__new__(cls)
				cls._instance._initialized = False
			return cls._instance

	def __init__(self):
		if self._initialized:
			return
		self._initialized = True
		self._lang = languageHandler.getLanguage().split('_')[0]
		self._preferredChannel = Channel.ALL
		self._addonsCache: Dict[str, List[OfficialAddon]] = {}

	def _getCurrentApiVersion(self) -> str:
		year, major, minor = addonAPIVersion.CURRENT
		return f"{year}.{major}.{minor}"

	def _getStoreURL(self, channel: Channel = None, apiVersion: str = None) -> str:
		if channel is None:
			channel = self._preferredChannel
		if apiVersion is None:
			apiVersion = self._getCurrentApiVersion()
		return f"{OFFICIAL_STORE_BASE_URL}/{self._lang}/{channel.value}/{apiVersion}.json"

	def fetchAddons(
		self, channel: Channel = None,
		includeIncompatible: bool = False,
		forceRefresh: bool = False
	) -> List[OfficialAddon]:
		from . import ajustes
		from .cache_manager import CacheManager

		if channel is None:
			channel = self._preferredChannel
		apiVersion = LATEST_API_VER if includeIncompatible else self._getCurrentApiVersion()
		url = self._getStoreURL(channel, apiVersion)

		# Memoria
		if not forceRefresh and url in self._addonsCache:
			addons, timestamp = self._addonsCache[url]
			interval = ajustes.tiempoDict.get(ajustes.tempCacheInterval, 3600)
			if (time.time() - timestamp) < interval:
				return addons

		# Disco
		cacheMgr = CacheManager(
			ajustes.dirDatos, ajustes.tiempoDict,
			lambda: ajustes.tempCacheInterval,
			lambda: ajustes.tempServerCache,
			lambda: ajustes.tempUseTranslationCache,
		)
		ignore_ttl = not forceRefresh and ajustes.IS_TEMPORAL
		cached_data, timestamp = cacheMgr.getStoreCache(url, ignore_ttl=ignore_ttl)

		if not forceRefresh and cached_data:
			addons = [a for a in (self._parseAddonData(d) for d in cached_data) if a]
			self._addonsCache[url] = (addons, timestamp)
			return addons

		try:
			cache_buster_url = f"{url}?t={int(time.time())}"
			data = red.get_json(cache_buster_url, timeout=FETCH_TIMEOUT, headers=red.HEADERS_NVDA)
			if not data:
				if ajustes.tempListCacheEnabled:
					cached_data, timestamp = cacheMgr.getStoreCache(url, ignore_ttl=True)
					if cached_data:
						return [a for a in (self._parseAddonData(d) for d in cached_data) if a]
				return []

			cacheMgr.saveStoreCache(url, data)
			addons = [a for a in (self._parseAddonData(d) for d in data) if a]
			self._addonsCache[url] = (addons, time.time())
			return addons
		except Exception as e:
			log.debug(f"Error al obtener complementos oficiales: {e}")
			return []

	def _parseAddonData(self, data: Dict[str, Any]) -> Optional[OfficialAddon]:
		try:
			minV = data.get('minNVDAVersion', {})
			lastV = data.get('lastTestedVersion', {})
			return OfficialAddon(
				addonId=data.get('addonId', ''),
				displayName=data.get('displayName', ''),
				description=data.get('description', ''),
				publisher=data.get('publisher', ''),
				addonVersionName=data.get('addonVersionName', ''),
				channel=data.get('channel', 'stable'),
				homepage=data.get('homepage'),
				license=data.get('license', ''),
				licenseURL=data.get('licenseURL'),
				sourceURL=data.get('sourceURL', ''),
				URL=data.get('URL', ''),
				sha256=data.get('sha256', ''),
				minNVDAVersion=(minV.get('major', 2019), minV.get('minor', 3), minV.get('patch', 0)),
				lastTestedVersion=(lastV.get('major', 2024), lastV.get('minor', 1), lastV.get('patch', 0)),
				reviewURL=data.get('reviewUrl'),
				legacy=data.get('legacy', False),
				changelog=data.get('changelog'),
				submissionTime=data.get('submissionTime'),
			)
		except Exception as e:
			log.debug(f"Error al parsear addon: {e}")
			return None

	def checkUpdates(self, includeIncompatible: bool = False) -> List[Tuple[OfficialAddon, Any]]:
		updates = []
		try:
			storeAddons = self.fetchAddons(includeIncompatible=includeIncompatible)
			installedAddons = list(addonHandler.getAvailableAddons())
			storeAddonsDict: Dict[str, OfficialAddon] = {}
			for addon in storeAddons:
				addonId = addon.addonId.lower()
				if addonId not in storeAddonsDict:
					storeAddonsDict[addonId] = addon
				else:
					try:
						if version_utils.parse(addon.addonVersionName) > version_utils.parse(storeAddonsDict[addonId].addonVersionName):
							storeAddonsDict[addonId] = addon
					except:
						pass
			for installed in installedAddons:
				if installed.isPendingRemove:
					continue
				installedId = installed.name.lower()
				if installedId in storeAddonsDict:
					storeAddon = storeAddonsDict[installedId]
					if not includeIncompatible and not storeAddon.isCompatible:
						continue
					try:
						if version_utils.parse(storeAddon.addonVersionName) > version_utils.parse(installed.version):
							updates.append((storeAddon, installed))
					except:
						if storeAddon.addonVersionName > installed.version:
							updates.append((storeAddon, installed))
			return updates
		except Exception as e:
			log.debug(f"Error al buscar actualizaciones oficiales: {e}")
			return []


def buscar_actualizaciones_oficiales(force_refresh: bool = False) -> List[Tuple[OfficialAddon, Any]]:
	from . import ajustes
	client = OfficialStoreClient()
	return client.checkUpdates(includeIncompatible=ajustes.tempAllowIncompatible)


def obtener_complementos_oficiales(
	includeIncompatible: bool = False,
	channel: Channel = None,
	force_refresh: bool = False
) -> List[OfficialAddon]:
	client = OfficialStoreClient()
	return client.fetchAddons(channel=channel, includeIncompatible=includeIncompatible, forceRefresh=force_refresh)


def verificar_checksum(archivo: str, sha256_esperado: str) -> bool:
	try:
		sha256 = hashlib.sha256()
		with open(archivo, 'rb') as f:
			for chunk in iter(lambda: f.read(8192), b''):
				sha256.update(chunk)
		return sha256.hexdigest().lower() == sha256_esperado.lower()
	except Exception as e:
		log.debug(f"Error al verificar checksum: {e}")
		return False
