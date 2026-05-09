# -*- coding: utf-8 -*-
# Copyright (C) 2021-2025 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.
#
# Módulo de gestión de caché - Traducciones y listas de tienda
#

import os
import json
import time
import hashlib
from threading import Lock
from typing import Optional, List, Dict, Tuple
from logHandler import log

_cache_lock = Lock()


class CacheManager:
	"""Maneja la caché con persistencia en memoria para máximo rendimiento"""

	_memCache = {}
	_transCache = None

	def __init__(self, dirDatos: str, tiempoDict: dict, getCacheInterval, getServerCache, getUseTranslationCache):
		self.dirCache = os.path.join(dirDatos, "cache")
		self.dirListCache = os.path.join(self.dirCache, "lists")
		self._tiempoDict = tiempoDict
		self._getCacheInterval = getCacheInterval
		self._getServerCache = getServerCache
		self._getUseTranslationCache = getUseTranslationCache
		for d in [self.dirCache, self.dirListCache]:
			if not os.path.exists(d):
				try:
					os.makedirs(d, exist_ok=True)
				except Exception as e:
					log.debug(f"No se pudo crear el directorio: {d} - {e}")
		self.translationCacheFile = os.path.join(self.dirCache, "translations.json")

	def _getSourceFile(self, source: str) -> str:
		filename = hashlib.md5(source.encode('utf-8')).hexdigest() + ".json"
		return os.path.join(self.dirListCache, filename)

	# --- Caché de traducciones ---

	def getTranslation(self, text: str, targetLang: str) -> Optional[str]:
		if not self._getUseTranslationCache() or not text or not targetLang:
			return None
		if CacheManager._transCache is None:
			with _cache_lock:
				if os.path.exists(self.translationCacheFile):
					try:
						with open(self.translationCacheFile, "r", encoding="utf-8") as f:
							CacheManager._transCache = json.load(f)
					except:
						CacheManager._transCache = {}
				else:
					CacheManager._transCache = {}
		text_key = hashlib.md5(text.encode('utf-8')).hexdigest()
		return CacheManager._transCache.get(str(targetLang), {}).get(text_key)

	def saveTranslation(self, text: str, translatedText: str, targetLang: str):
		if not self._getUseTranslationCache() or not text or not translatedText or not targetLang:
			return
		text_key = hashlib.md5(text.encode('utf-8')).hexdigest()
		lang_key = str(targetLang)
		with _cache_lock:
			if CacheManager._transCache is None:
				CacheManager._transCache = {}
			if lang_key not in CacheManager._transCache:
				CacheManager._transCache[lang_key] = {}
			CacheManager._transCache[lang_key][text_key] = translatedText
			try:
				with open(self.translationCacheFile, "w", encoding="utf-8") as f:
					json.dump(CacheManager._transCache, f, ensure_ascii=False, indent=2)
			except Exception as e:
				log.error(f"Error al guardar caché de traducción: {e}")

	# --- Caché de listas de tienda ---

	def getStoreCache(self, source: str, ignore_ttl: bool = False) -> Tuple[Optional[List[Dict]], float]:
		if not self._getServerCache() or not source:
			return None, 0
		cacheFile = self._getSourceFile(source)
		# Memoria primero
		if cacheFile in CacheManager._memCache:
			entry = CacheManager._memCache[cacheFile]
			cached_time = entry.get("timestamp", 0)
			if ignore_ttl:
				return entry.get("data"), cached_time
			interval = self._tiempoDict.get(self._getCacheInterval(), 3600)
			if (time.time() - cached_time) < interval:
				return entry.get("data"), cached_time
		# Disco
		if not os.path.exists(cacheFile):
			return None, 0
		with _cache_lock:
			try:
				with open(cacheFile, "r", encoding="utf-8") as f:
					entry = json.load(f)
					if entry:
						CacheManager._memCache[cacheFile] = entry
						cached_time = entry.get("timestamp", 0)
						if ignore_ttl:
							return entry.get("data"), cached_time
						interval = self._tiempoDict.get(self._getCacheInterval(), 3600)
						if (time.time() - cached_time) < interval:
							return entry.get("data"), cached_time
			except Exception as e:
				log.debug(f"Error al leer caché de {source}: {e}")
				if isinstance(e, json.JSONDecodeError):
					try:
						os.remove(cacheFile)
					except:
						pass
		return None, 0

	def saveStoreCache(self, source: str, data: List[Dict]):
		if not self._getServerCache() or not source or data is None:
			return
		cacheFile = self._getSourceFile(source)
		with _cache_lock:
			try:
				entry = {"timestamp": time.time(), "url": source, "data": data}
				CacheManager._memCache[cacheFile] = entry
				with open(cacheFile, "w", encoding="utf-8") as f:
					json.dump(entry, f, ensure_ascii=False, indent=2)
			except Exception as e:
				log.error(f"Error al guardar caché de tienda: {e}")
