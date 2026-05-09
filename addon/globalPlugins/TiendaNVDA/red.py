# -*- coding: utf-8 -*-
# Copyright (C) 2021-2025 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.
#
# Módulo de red - Centraliza todas las peticiones HTTP usando requests
# Sustituye urllib para evitar problemas de certificados SSL
#

import requests
import json
import os
import time
from typing import Optional, Callable
from logHandler import log

# Timeout por defecto
DEFAULT_TIMEOUT = 30
DOWNLOAD_TIMEOUT = 120

# Headers comunes
HEADERS_BROWSER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
HEADERS_NVDA = {'User-Agent': 'NVDA Addon Store Client'}

# Sesión reutilizable para mejor rendimiento (connection pooling)
_session = None


def _get_session() -> requests.Session:
	"""Obtiene o crea una sesión HTTP reutilizable"""
	global _session
	if _session is None:
		_session = requests.Session()
		_session.headers.update(HEADERS_BROWSER)
	return _session


def get_json(url: str, timeout: int = DEFAULT_TIMEOUT, headers: dict = None) -> Optional[list]:
	"""Descarga y parsea JSON desde una URL"""
	try:
		s = _get_session()
		h = headers or HEADERS_BROWSER
		r = s.get(url, headers=h, timeout=timeout)
		r.raise_for_status()
		return r.json()
	except Exception as e:
		log.debug(f"Error al obtener JSON de {url}: {e}")
		return None


def get_text(url: str, timeout: int = DEFAULT_TIMEOUT, headers: dict = None) -> Optional[str]:
	"""Descarga texto desde una URL"""
	try:
		s = _get_session()
		h = headers or HEADERS_BROWSER
		r = s.get(url, headers=h, timeout=timeout)
		r.raise_for_status()
		return r.text
	except Exception as e:
		log.debug(f"Error al obtener texto de {url}: {e}")
		return None


def get_bytes(url: str, timeout: int = DEFAULT_TIMEOUT, headers: dict = None) -> Optional[bytes]:
	"""Descarga bytes desde una URL"""
	try:
		s = _get_session()
		h = headers or HEADERS_BROWSER
		r = s.get(url, headers=h, timeout=timeout)
		r.raise_for_status()
		return r.content
	except Exception as e:
		log.debug(f"Error al obtener bytes de {url}: {e}")
		return None


def check_json(url: str, timeout: int = DEFAULT_TIMEOUT) -> bool:
	"""Verifica si una URL devuelve JSON válido"""
	try:
		s = _get_session()
		r = s.get(url, headers=HEADERS_BROWSER, timeout=timeout)
		r.raise_for_status()
		r.json()
		return True
	except:
		return False


def get_filename_from_url(url: str, timeout: int = DEFAULT_TIMEOUT) -> Optional[str]:
	"""Obtiene el nombre de archivo de una URL (sin extensión)"""
	try:
		s = _get_session()
		r = s.head(url, headers=HEADERS_BROWSER, timeout=timeout, allow_redirects=True)
		cd = r.headers.get('Content-Disposition', '')
		if 'filename=' in cd:
			fname = cd.split('filename=')[-1].strip('"\'')
			return os.path.splitext(fname)[0]
		# Intentar con GET si HEAD no devuelve filename
		r = s.get(url, headers=HEADERS_BROWSER, timeout=timeout, stream=True)
		cd = r.headers.get('Content-Disposition', '')
		r.close()
		if 'filename=' in cd:
			fname = cd.split('filename=')[-1].strip('"\'')
			return os.path.splitext(fname)[0]
		return None
	except:
		return None


def get_filename_full(url: str, timeout: int = DEFAULT_TIMEOUT) -> Optional[str]:
	"""Obtiene el nombre de archivo completo de una URL"""
	try:
		s = _get_session()
		r = s.head(url, headers=HEADERS_BROWSER, timeout=timeout, allow_redirects=True)
		cd = r.headers.get('Content-Disposition', '')
		if 'filename=' in cd:
			return cd.split('filename=')[-1].strip('"\'')
		# Intentar con GET
		r = s.get(url, headers=HEADERS_BROWSER, timeout=timeout, stream=True)
		cd = r.headers.get('Content-Disposition', '')
		r.close()
		if 'filename=' in cd:
			return cd.split('filename=')[-1].strip('"\'')
		return None
	except:
		return None


def download_file(
	url: str,
	dest_path: str,
	timeout: int = DOWNLOAD_TIMEOUT,
	headers: dict = None,
	progress_callback: Optional[Callable] = None,
	max_retries: int = 3
) -> bool:
	"""
	Descarga un archivo con reintentos y callback de progreso.
	
	Args:
		url: URL del archivo
		dest_path: Ruta de destino
		timeout: Timeout en segundos
		headers: Headers HTTP opcionales
		progress_callback: Función callback(percent, downloaded, total)
		max_retries: Número máximo de reintentos
	
	Returns:
		True si la descarga fue exitosa
	"""
	h = headers or HEADERS_BROWSER
	s = _get_session()

	for attempt in range(max_retries):
		try:
			r = s.get(url, headers=h, timeout=timeout, stream=True)
			r.raise_for_status()
			total_size = int(r.headers.get('Content-Length', 0))
			downloaded = 0

			with open(dest_path, 'wb') as f:
				for chunk in r.iter_content(chunk_size=8192):
					if chunk:
						f.write(chunk)
						downloaded += len(chunk)
						if progress_callback and total_size > 0:
							percent = int(downloaded * 100 / total_size)
							progress_callback(percent, downloaded, total_size)
			return True
		except Exception as e:
			log.debug(f"Error descargando {url} (intento {attempt + 1}/{max_retries}): {e}")
			if attempt < max_retries - 1:
				time.sleep(2)
			else:
				return False
	return False
