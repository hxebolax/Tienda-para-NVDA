# -*- coding: utf-8 -*-
# actualizadorRecursos.py
#
# Módulo reutilizable para actualizar traducciones y/o documentación
# de un complemento NVDA desde GitHub, sin publicar nueva release.
#
# Todo configurable: callbacks de progreso, modos de comprobación,
# filtros de idioma, repos privados, respaldos, mensajes, etc.
#
# Licencia: GPL v2

import os
import json
import hashlib
import ssl
import zipfile
import shutil
import threading
import tempfile
from io import BytesIO
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

try:
	import addonHandler
	import languageHandler
	from logHandler import log
	import ui
	import wx
	_EN_NVDA = True
except ImportError:
	_EN_NVDA = False
	import logging
	log = logging.getLogger(__name__)


class ActualizadorRecursos:
	"""
	Gestor configurable de actualización de traducciones y documentación
	para complementos NVDA. Todo se personaliza vía **kwargs.
	
	Callbacks disponibles (se invocan desde hilo secundario,
	usar wx.CallAfter si se actualiza la interfaz):
		callback_progreso(descargados, total, etapa)
		callback_finalizado(exito, resultado)
		callback_error(excepcion)
		callback_pre_actualizacion() -> bool (False cancela)
	"""
	
	_VALORES_DEFECTO = {
		# ── GitHub ──
		"rama": "main",
		"tag_release": "recursos-latest",
		"timeout_http": 30,
		"token_github": None,
		
		# ── Qué actualizar ──
		"actualizar_idiomas": True,
		"actualizar_documentacion": True,
		
		# ── Rutas relativas a la raíz del addon ──
		"directorio_idiomas": "locale",
		"directorio_documentacion": "doc",
		
		# ── Extensiones ──
		"extensiones_idiomas": [".mo", ".po", ".ini"],
		"extensiones_documentacion": [".html", ".md", ".txt", ".css"],
		
		# ── Modo de comprobación ──
		# "inicio"    → solo al cargar el complemento (respeta intervalo_horas)
		# "periodico" → comprueba cada intervalo_horas con timer en segundo plano
		# "manual"    → solo cuando se llama a comprobarActualizacion()/forzarActualizacion()
		"modo_comprobacion": "inicio",
		"intervalo_horas": 24,
		
		# ── Notificaciones ──
		"notificar_usuario": False,
		"notificar_sin_cambios": False,
		"mensaje_exito": "Recursos del complemento actualizados. Reinicie NVDA para aplicar todos los cambios.",
		"mensaje_sin_cambios": "Los recursos ya están actualizados.",
		"mensaje_error": "Error al actualizar los recursos del complemento.",
		"mensaje_comprobando": "Comprobando actualizaciones de recursos...",
		
		# ── Callbacks del desarrollador ──
		# callback_progreso(descargados: int, total: int, etapa: str)
		#   etapa puede ser: "descargando", "instalando_idiomas", "instalando_docs"
		# callback_finalizado(exito: bool, resultado: dict)
		# callback_error(excepcion: Exception)
		# callback_pre_actualizacion() -> bool  (retornar False cancela)
		"callback_progreso": None,
		"callback_finalizado": None,
		"callback_error": None,
		"callback_pre_actualizacion": None,
		
		# ── Filtros de idioma ──
		"solo_idioma_actual": False,
		"idiomas_incluidos": None,
		"idiomas_excluidos": None,
		
		# ── Respaldo ──
		"hacer_respaldo": False,
		"directorio_respaldo": "respaldo_recursos",
		
		# ── Avanzado ──
		"tamaño_bloque_descarga": 8192,
		"archivo_estado": "recursos_estado.json",
		"archivo_info_remoto": "recursos_info.json",
	}
	
	def __init__(self, usuario_github: str, nombre_repositorio: str, **opciones):
		"""
		Args:
			usuario_github: Usuario u organización en GitHub.
			nombre_repositorio: Nombre del repositorio.
			**opciones: Ver _VALORES_DEFECTO para todas las opciones.
		"""
		self.usuario_github = usuario_github
		self.nombre_repositorio = nombre_repositorio
		
		# Fusionar opciones
		self._config = dict(self._VALORES_DEFECTO)
		for clave, valor in opciones.items():
			if clave not in self._VALORES_DEFECTO:
				log.warning(f"ActualizadorRecursos: opción desconocida '{clave}'")
			else:
				self._config[clave] = valor
		
		# Rutas
		self._ruta_complemento = self._obtenerRutaComplemento()
		self._ruta_idiomas = os.path.join(self._ruta_complemento, self._config["directorio_idiomas"])
		self._ruta_docs = os.path.join(self._ruta_complemento, self._config["directorio_documentacion"])
		self._ruta_estado = os.path.join(self._ruta_complemento, self._config["archivo_estado"])
		self._url_api = f"https://api.github.com/repos/{usuario_github}/{nombre_repositorio}"
		
		# Control de hilos
		self._hilo = None
		self._timer = None
		self._detenido = threading.Event()
		self._nombre_cache = None
		
		# Encabezados HTTP (con token opcional para repos privados)
		self._encabezados = {
			"User-Agent": "NVDA-AddonResourceUpdater/2.0",
			"Accept": "application/vnd.github.v3+json",
		}
		if self._config["token_github"]:
			self._encabezados["Authorization"] = f"token {self._config['token_github']}"
		
		log.debug(
			f"ActualizadorRecursos: {usuario_github}/{nombre_repositorio}, "
			f"modo={self._config['modo_comprobacion']}, "
			f"idiomas={self._config['actualizar_idiomas']}, "
			f"docs={self._config['actualizar_documentacion']}"
		)
		
		# Contexto SSL robusto (resuelve problemas de certificados en NVDA)
		self._contexto_ssl = self._crearContextoSSL()
		
		# Arrancar según el modo
		modo = self._config["modo_comprobacion"]
		if modo == "inicio":
			self.comprobarActualizacion()
		elif modo == "periodico":
			self.comprobarActualizacion()
			self._iniciarTimer()
	
	# ══════════════════════════════════════════════════════════════
	# API PÚBLICA
	# ══════════════════════════════════════════════════════════════
	
	def comprobarActualizacion(self):
		"""Inicia comprobación en segundo plano. No bloquea. Ignora si ya hay una en curso."""
		if self._hilo and self._hilo.is_alive():
			log.debug("ActualizadorRecursos: comprobación ya en curso")
			return
		self._hilo = threading.Thread(
			target=self._ejecutarComprobacion,
			name=f"ActRecursos_{self._obtenerNombre()}",
			daemon=True,
		)
		self._hilo.start()
	
	def forzarActualizacion(self):
		"""Fuerza comprobación ignorando intervalo. Ideal para botones/gestos."""
		estado = self._cargarEstado()
		estado["fecha_comprobacion"] = ""
		self._guardarEstado(estado)
		self.comprobarActualizacion()
	
	def detener(self):
		"""Detiene todo. Llamar en terminate() del complemento."""
		self._detenido.set()
		if self._timer:
			self._timer.cancel()
			self._timer = None
		if self._hilo and self._hilo.is_alive():
			self._hilo.join(timeout=5)
		log.debug("ActualizadorRecursos detenido")
	
	def obtenerEstado(self) -> dict:
		"""Devuelve estado completo con idiomas/docs instalados y configuración."""
		estado = self._cargarEstado()
		estado["idiomas_instalados"] = self._listarRecursos(self._ruta_idiomas, "LC_MESSAGES")
		estado["documentacion_instalada"] = self._listarRecursos(self._ruta_docs)
		estado["configuracion"] = dict(self._config)
		return estado
	
	def obtenerConfiguracion(self) -> dict:
		"""Devuelve copia de la configuración activa."""
		return dict(self._config)
	
	# ══════════════════════════════════════════════════════════════
	# LÓGICA DE COMPROBACIÓN Y DESCARGA
	# ══════════════════════════════════════════════════════════════
	
	def _ejecutarComprobacion(self):
		"""Proceso completo en hilo secundario.
		
		Manejo de errores de red:
		- Si no hay conexión o la API falla, NO se actualiza fecha_comprobacion
		  para que reintente en el próximo inicio de NVDA.
		- Los errores de red se registran con log.info (visibles para diagnóstico).
		- Solo los errores inesperados (no de red) se notifican al usuario.
		"""
		resultado = {"exito": False, "instalados": 0, "idiomas": [], "docs": []}
		try:
			if not self._debeComprobar():
				self._invocarCallback("callback_finalizado", True, resultado)
				return
			
			log.info("ActualizadorRecursos: comprobando actualizaciones...")
			self._invocarCallback("callback_progreso", 0, 0, "comprobando")
			
			from datetime import datetime, timezone
			
			# Asegurar que el archivo de estado siempre existe
			estado = self._cargarEstado()
			if not os.path.exists(self._ruta_estado):
				self._guardarEstado(estado)
			
			# Obtener info de la release (incluye hash del body)
			# Si falla por red, NO guardamos fecha_comprobacion → reintenta después
			try:
				info = self._obtenerInfoRelease()
			except (URLError, HTTPError, OSError) as e:
				# Sin conexión o error de red → no molestar, reintentará
				log.info(f"ActualizadorRecursos: sin conexión o error de red, reintentará: {e}")
				self._invocarCallback("callback_finalizado", True, resultado)
				return
			except Exception as e:
				log.warning(f"ActualizadorRecursos: sin release de recursos: {e}")
				self._invocarCallback("callback_finalizado", True, resultado)
				return
			
			# La API respondió correctamente → ahora sí guardar fecha de comprobación
			estado = self._cargarEstado()
			estado["fecha_comprobacion"] = datetime.now(timezone.utc).isoformat()
			self._guardarEstado(estado)
			
			# Comparar hash de la release con el local
			hash_remoto = info.get("hash_remoto", "")
			hash_local = estado.get("hash_combinado", "")
			
			log.info(
				f"ActualizadorRecursos: hash_remoto={hash_remoto[:16] if hash_remoto else '(vacío)'}, "
				f"hash_local={hash_local[:16] if hash_local else '(vacío)'}"
			)
			
			if hash_remoto and hash_local and hash_remoto == hash_local:
				log.info("ActualizadorRecursos: recursos actualizados, sin cambios")
				if self._config["notificar_sin_cambios"]:
					self._notificar(self._config["mensaje_sin_cambios"])
				resultado["exito"] = True
				self._invocarCallback("callback_finalizado", True, resultado)
				return
			
			# Callback pre-actualización (puede cancelar)
			cb_pre = self._config["callback_pre_actualizacion"]
			if cb_pre and callable(cb_pre):
				if not cb_pre():
					log.info("ActualizadorRecursos: actualización cancelada por callback")
					self._invocarCallback("callback_finalizado", False, resultado)
					return
			
			# Descargar con progreso
			try:
				datos = self._descargarConProgreso(info["url_descarga"])
			except (URLError, HTTPError, OSError) as e:
				log.info(f"ActualizadorRecursos: error de red en descarga, reintentará: {e}")
				self._invocarCallback("callback_finalizado", True, resultado)
				return
			
			if not datos:
				self._invocarCallback("callback_error", Exception("Descarga fallida"))
				return
			
			# Extraer hash del recursos_info.json dentro del ZIP
			hash_zip = self._extraerHashDelZip(datos)
			if hash_zip and hash_local and hash_zip == hash_local:
				log.info("ActualizadorRecursos: ZIP verificado, sin cambios reales")
				if self._config["notificar_sin_cambios"]:
					self._notificar(self._config["mensaje_sin_cambios"])
				resultado["exito"] = True
				# Guardar el hash del ZIP como referencia
				estado = self._cargarEstado()
				estado["hash_combinado"] = hash_zip
				self._guardarEstado(estado)
				self._invocarCallback("callback_finalizado", True, resultado)
				return
			
			# Respaldo si está configurado
			if self._config["hacer_respaldo"]:
				self._crearRespaldo()
			
			# Instalar
			resultado = self._instalarRecursos(datos)
			
			if resultado["instalados"] > 0:
				estado = self._cargarEstado()
				# Usar el hash del ZIP si está disponible (fuente de verdad),
				# sino calcular localmente
				estado["hash_combinado"] = hash_zip if hash_zip else self._calcularHashCombinado()
				estado["fecha_actualizacion"] = datetime.now(timezone.utc).isoformat()
				estado["ultimo_resultado"] = {
					"idiomas": resultado["idiomas"],
					"docs": resultado["docs"],
					"total": resultado["instalados"],
				}
				self._guardarEstado(estado)
				
				if resultado["idiomas"]:
					self._recargarTraducciones()
				
				resultado["exito"] = True
				log.info(
					f"ActualizadorRecursos: actualización completada, "
					f"hash={estado['hash_combinado'][:16]}..."
				)
				if self._config["notificar_usuario"]:
					self._notificar(self._config["mensaje_exito"])
			else:
				log.info("ActualizadorRecursos: 0 archivos instalados del paquete")
				# Aun así guardar el hash del ZIP para no re-descargar
				if hash_zip:
					estado = self._cargarEstado()
					estado["hash_combinado"] = hash_zip
					self._guardarEstado(estado)
				resultado["exito"] = True
			
			self._invocarCallback("callback_finalizado", resultado["exito"], resultado)
		
		except (URLError, HTTPError, OSError) as e:
			# Error de red genérico no capturado antes
			log.info(f"ActualizadorRecursos: error de red: {e}")
			self._invocarCallback("callback_finalizado", False, resultado)
		except Exception as e:
			log.error(f"ActualizadorRecursos: {e}", exc_info=True)
			if self._config["notificar_usuario"]:
				self._notificar(self._config["mensaje_error"])
			self._invocarCallback("callback_error", e)
			self._invocarCallback("callback_finalizado", False, resultado)
	
	def _descargarConProgreso(self, url: str) -> bytes:
		"""Descarga con reporte de progreso vía callback."""
		log.info(f"ActualizadorRecursos: descargando {url}")
		req = Request(url, headers=self._encabezados)
		
		with urlopen(req, timeout=self._config["timeout_http"], context=self._contexto_ssl) as resp:
			total = int(resp.headers.get("Content-Length", 0))
			descargados = 0
			bloques = []
			tam_bloque = self._config["tamaño_bloque_descarga"]
			
			while True:
				if self._detenido.is_set():
					log.info("ActualizadorRecursos: descarga cancelada")
					return None
				
				bloque = resp.read(tam_bloque)
				if not bloque:
					break
				
				bloques.append(bloque)
				descargados += len(bloque)
				self._invocarCallback("callback_progreso", descargados, total, "descargando")
			
			return b"".join(bloques)
	
	def _instalarRecursos(self, datos_zip: bytes) -> dict:
		"""Extrae e instala recursos filtrados según configuración."""
		resultado = {"instalados": 0, "idiomas": [], "docs": []}
		dir_temp = tempfile.mkdtemp(prefix="nvda_recursos_")
		
		try:
			with zipfile.ZipFile(BytesIO(datos_zip)) as zf:
				for nombre in zf.namelist():
					if nombre.startswith("/") or ".." in nombre:
						log.error(f"Ruta peligrosa: {nombre}")
						return resultado
				zf.extractall(dir_temp)
			
			# Determinar filtro de idiomas
			filtro = self._construirFiltroIdiomas()
			
			# Instalar traducciones
			if self._config["actualizar_idiomas"]:
				src = os.path.join(dir_temp, self._config["directorio_idiomas"])
				if os.path.isdir(src):
					self._invocarCallback("callback_progreso", 0, 0, "instalando_idiomas")
					n, langs = self._copiarRecursos(
						src, self._ruta_idiomas,
						self._config["extensiones_idiomas"], filtro,
					)
					resultado["instalados"] += n
					resultado["idiomas"] = langs
			
			# Instalar documentación
			if self._config["actualizar_documentacion"]:
				src = os.path.join(dir_temp, self._config["directorio_documentacion"])
				if os.path.isdir(src):
					self._invocarCallback("callback_progreso", 0, 0, "instalando_docs")
					n, langs = self._copiarRecursos(
						src, self._ruta_docs,
						self._config["extensiones_documentacion"], filtro,
					)
					resultado["instalados"] += n
					resultado["docs"] = langs
			
			log.info(
				f"ActualizadorRecursos: {resultado['instalados']} archivos "
				f"(idiomas: {resultado['idiomas']}, docs: {resultado['docs']})"
			)
		except zipfile.BadZipFile:
			log.error("ZIP inválido")
		except Exception as e:
			log.error(f"Error instalando: {e}", exc_info=True)
		finally:
			shutil.rmtree(dir_temp, ignore_errors=True)
		
		return resultado
	
	def _copiarRecursos(self, origen, destino, extensiones, filtro_idiomas) -> tuple:
		"""Copia archivos filtrados por extensión y filtro de idiomas."""
		copiados = 0
		idiomas = []
		total_archivos = sum(
			1 for r, _, fs in os.walk(origen)
			for f in fs if any(f.endswith(e) for e in extensiones)
		)
		procesados = 0
		
		for raiz, _, archivos in os.walk(origen):
			for archivo in archivos:
				if not any(archivo.endswith(e) for e in extensiones):
					continue
				
				ruta_origen = os.path.join(raiz, archivo)
				ruta_rel = os.path.relpath(ruta_origen, origen)
				
				# Aplicar filtro de idiomas
				codigo_idioma = ruta_rel.split(os.sep)[0] if os.sep in ruta_rel else ruta_rel.split("/")[0]
				if filtro_idiomas and codigo_idioma not in filtro_idiomas:
					continue
				
				ruta_destino = os.path.join(destino, ruta_rel)
				os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)
				shutil.copy2(ruta_origen, ruta_destino)
				copiados += 1
				procesados += 1
				
				if codigo_idioma not in idiomas:
					idiomas.append(codigo_idioma)
				
				# Progreso de instalación
				if total_archivos > 0:
					self._invocarCallback(
						"callback_progreso", procesados, total_archivos, "instalando"
					)
		
		return copiados, idiomas
	
	def _construirFiltroIdiomas(self) -> set:
		"""Construye el conjunto de idiomas permitidos según la configuración."""
		filtro = None
		
		# Solo idioma actual de NVDA
		if self._config["solo_idioma_actual"] and _EN_NVDA:
			idioma = languageHandler.getLanguage()
			filtro = {idioma}
			if "_" in idioma:
				filtro.add(idioma.split("_")[0])
			filtro.add("en")  # Siempre incluir inglés como fallback
		
		# Lista explícita de idiomas incluidos
		if self._config["idiomas_incluidos"]:
			incluidos = set(self._config["idiomas_incluidos"])
			filtro = incluidos if filtro is None else filtro & incluidos
		
		# Excluir idiomas
		if self._config["idiomas_excluidos"] and filtro:
			filtro -= set(self._config["idiomas_excluidos"])
		elif self._config["idiomas_excluidos"]:
			# Sin filtro previo, hay que recorrer todo y excluir después
			# Devolvemos None y filtramos en _copiarRecursos
			pass
		
		return filtro
	
	# ══════════════════════════════════════════════════════════════
	# TIMER PERIÓDICO
	# ══════════════════════════════════════════════════════════════
	
	def _iniciarTimer(self):
		"""Inicia un timer que comprueba cada intervalo_horas."""
		if self._detenido.is_set():
			return
		intervalo_seg = self._config["intervalo_horas"] * 3600
		self._timer = threading.Timer(intervalo_seg, self._tickTimer)
		self._timer.daemon = True
		self._timer.start()
	
	def _tickTimer(self):
		"""Ejecuta la comprobación periódica y reprograma el timer."""
		if not self._detenido.is_set():
			self.comprobarActualizacion()
			self._iniciarTimer()
	
	# ══════════════════════════════════════════════════════════════
	# RESPALDO
	# ══════════════════════════════════════════════════════════════
	
	def _crearRespaldo(self):
		"""Crea respaldo de los recursos actuales antes de sobreescribir."""
		dir_respaldo = os.path.join(
			self._ruta_complemento, self._config["directorio_respaldo"]
		)
		try:
			from datetime import datetime
			ts = datetime.now().strftime("%Y%m%d_%H%M%S")
			
			for nombre, ruta in [("locale", self._ruta_idiomas), ("doc", self._ruta_docs)]:
				if os.path.isdir(ruta):
					destino = os.path.join(dir_respaldo, f"{nombre}_{ts}")
					shutil.copytree(ruta, destino)
					log.info(f"Respaldo creado: {destino}")
		except Exception as e:
			log.warning(f"Error creando respaldo: {e}")
	
	# ══════════════════════════════════════════════════════════════
	# UTILIDADES INTERNAS
	# ══════════════════════════════════════════════════════════════
	
	def _invocarCallback(self, nombre_cb: str, *args):
		"""Invoca un callback del desarrollador si está configurado."""
		cb = self._config.get(nombre_cb)
		if cb and callable(cb):
			try:
				cb(*args)
			except Exception as e:
				log.warning(f"Error en callback {nombre_cb}: {e}")
	
	def _obtenerRutaComplemento(self) -> str:
		directorio = os.path.dirname(os.path.abspath(__file__))
		for _ in range(6):
			if os.path.exists(os.path.join(directorio, "manifest.ini")):
				return directorio
			padre = os.path.dirname(directorio)
			if padre == directorio:
				break
			directorio = padre
		if _EN_NVDA:
			try:
				return addonHandler.getCodeAddon(frameDist=3).path
			except Exception:
				pass
		raise FileNotFoundError("No se encontró manifest.ini del complemento")
	
	def _obtenerNombre(self) -> str:
		if self._nombre_cache:
			return self._nombre_cache
		ruta = os.path.join(self._ruta_complemento, "manifest.ini")
		try:
			with open(ruta, "r", encoding="utf-8") as f:
				for linea in f:
					if linea.strip().startswith("name"):
						p = linea.split("=", 1)
						if len(p) == 2:
							self._nombre_cache = p[1].strip().strip('"\'')
							return self._nombre_cache
		except Exception:
			pass
		self._nombre_cache = os.path.basename(self._ruta_complemento)
		return self._nombre_cache
	
	def _obtenerInfoRelease(self) -> dict:
		"""Obtiene URL de descarga y hash remoto desde la release de GitHub.
		
		El hash se extrae del body de la release (línea **Hash:** `xxx`).
		Esto es más fiable que depender de un archivo en el repositorio.
		"""
		url = f"{self._url_api}/releases/tags/{self._config['tag_release']}"
		datos = self._peticionHTTP(url)
		
		# Buscar el asset del paquete de recursos
		url_descarga = None
		for asset in datos.get("assets", []):
			if asset.get("name", "").endswith("_recursos.zip"):
				url_descarga = asset["browser_download_url"]
				break
		
		if not url_descarga:
			raise Exception("Paquete de recursos no encontrado en la release")
		
		# Extraer hash del body de la release
		hash_remoto = ""
		body = datos.get("body", "")
		if body:
			import re
			# Buscar patrón: **Hash:** `hash_hex`
			m = re.search(r'\*\*Hash:\*\*\s*`([a-fA-F0-9]{64})`', body)
			if m:
				hash_remoto = m.group(1)
				log.debug(f"ActualizadorRecursos: hash de release={hash_remoto[:16]}...")
		
		return {"url_descarga": url_descarga, "hash_remoto": hash_remoto}
	
	def _extraerHashDelZip(self, datos_zip: bytes) -> str:
		"""Extrae el hash_combinado del recursos_info.json dentro del ZIP.
		
		Esta es la fuente de verdad más fiable para el hash, ya que el
		archivo se genera en el mismo workflow que crea el ZIP.
		"""
		try:
			with zipfile.ZipFile(BytesIO(datos_zip)) as zf:
				nombre_info = self._config["archivo_info_remoto"]
				if nombre_info in zf.namelist():
					info = json.loads(zf.read(nombre_info).decode("utf-8"))
					hash_val = info.get("hash_combinado", "")
					if hash_val:
						log.debug(f"ActualizadorRecursos: hash del ZIP={hash_val[:16]}...")
					return hash_val
		except Exception as e:
			log.warning(f"ActualizadorRecursos: no se pudo leer hash del ZIP: {e}")
		return ""
	
	def _calcularHashCombinado(self) -> str:
		"""Calcula hash combinado local con formato idéntico al workflow.
		
		IMPORTANTE: Las rutas en los hashes deben incluir el prefijo
		'locale/' o 'doc/' para coincidir con el formato del workflow
		de GitHub Actions.
		"""
		hashes = []
		if self._config["actualizar_idiomas"] and os.path.isdir(self._ruta_idiomas):
			hashes.extend(self._hashDir(
				self._ruta_idiomas,
				self._config["extensiones_idiomas"],
				prefijo=self._config["directorio_idiomas"],
			))
		if self._config["actualizar_documentacion"] and os.path.isdir(self._ruta_docs):
			hashes.extend(self._hashDir(
				self._ruta_docs,
				self._config["extensiones_documentacion"],
				prefijo=self._config["directorio_documentacion"],
			))
		if not hashes:
			return ""
		return hashlib.sha256("\n".join(sorted(hashes)).encode()).hexdigest()
	
	def _hashDir(self, directorio, extensiones, prefijo="") -> list:
		"""Genera lista de hashes de archivos en formato 'hash  prefijo/ruta'."""
		r = []
		for raiz, _, archivos in os.walk(directorio):
			for f in sorted(archivos):
				if any(f.endswith(e) for e in extensiones):
					ruta = os.path.join(raiz, f)
					with open(ruta, "rb") as fh:
						h = hashlib.sha256(fh.read()).hexdigest()
					rel = os.path.relpath(ruta, directorio).replace(os.sep, "/")
					# Incluir prefijo para coincidir con formato del workflow
					if prefijo:
						rel = f"{prefijo}/{rel}"
					r.append(f"{h}  {rel}")
		return r
	
	def _listarRecursos(self, directorio, subcarpeta=None) -> list:
		"""Lista códigos de idioma que tienen recursos instalados."""
		if not os.path.isdir(directorio):
			return []
		resultado = []
		for entrada in os.listdir(directorio):
			ruta = os.path.join(directorio, entrada)
			if not os.path.isdir(ruta):
				continue
			if subcarpeta:
				ruta = os.path.join(ruta, subcarpeta)
			if os.path.isdir(ruta) and os.listdir(ruta):
				resultado.append(entrada)
			elif not subcarpeta and os.listdir(os.path.join(directorio, entrada)):
				resultado.append(entrada)
		return sorted(resultado)
	
	def _cargarEstado(self) -> dict:
		try:
			if os.path.exists(self._ruta_estado):
				with open(self._ruta_estado, "r", encoding="utf-8") as f:
					return json.load(f)
		except Exception:
			pass
		return {"hash_combinado": "", "fecha_actualizacion": "", "fecha_comprobacion": ""}
	
	def _guardarEstado(self, estado):
		try:
			with open(self._ruta_estado, "w", encoding="utf-8") as f:
				json.dump(estado, f, ensure_ascii=False, indent="\t")
		except Exception as e:
			log.error(f"Error guardando estado: {e}")
	
	def _debeComprobar(self) -> bool:
		estado = self._cargarEstado()
		ultima = estado.get("fecha_comprobacion", "")
		if not ultima:
			return True
		try:
			from datetime import datetime, timezone
			dt = datetime.fromisoformat(ultima.replace("Z", "+00:00"))
			h = (datetime.now(timezone.utc) - dt).total_seconds() / 3600
			if h < self._config["intervalo_horas"]:
				log.debug(f"Comprobación omitida: {h:.1f}h < {self._config['intervalo_horas']}h")
				return False
		except Exception:
			pass
		return True
	
	def _peticionHTTP(self, url, binario=False):
		req = Request(url, headers=self._encabezados)
		with urlopen(req, timeout=self._config["timeout_http"], context=self._contexto_ssl) as resp:
			datos = resp.read()
			return datos if binario else json.loads(datos.decode("utf-8"))
	
	@staticmethod
	def _crearContextoSSL() -> ssl.SSLContext:
		"""Crea un contexto SSL robusto probando múltiples fuentes de certificados.
		
		Orden de prioridad:
		1. certifi (si está instalado como dependencia)
		2. Certificados del sistema operativo (Windows/macOS/Linux)
		3. Contexto sin verificación (último recurso, con advertencia)
		
		Esto resuelve el error SSL_CERTIFICATE_VERIFY_FAILED que ocurre
		en Python embebido (como NVDA) cuando no tiene acceso al almacén
		de certificados del sistema.
		"""
		# 1. Intentar con certifi
		try:
			import certifi
			ctx = ssl.create_default_context(cafile=certifi.where())
			log.debug("ActualizadorRecursos: SSL usando certifi")
			return ctx
		except (ImportError, Exception):
			pass
		
		# 2. Intentar con certificados del sistema
		try:
			ctx = ssl.create_default_context()
			# En Windows, cargar desde el almacén del sistema
			if hasattr(ctx, 'load_default_certs'):
				ctx.load_default_certs()
			# Verificar que funciona con una conexión de prueba
			import urllib.request
			req = urllib.request.Request(
				"https://api.github.com",
				method="HEAD",
				headers={"User-Agent": "NVDA-SSL-Test"}
			)
			with urlopen(req, timeout=10, context=ctx) as resp:
				pass
			log.debug("ActualizadorRecursos: SSL usando certificados del sistema")
			return ctx
		except Exception:
			pass
		
		# 3. Último recurso: sin verificación (con advertencia)
		log.warning(
			"ActualizadorRecursos: no se encontraron certificados SSL válidos. "
			"Usando conexión sin verificación de certificados."
		)
		ctx = ssl.create_default_context()
		ctx.check_hostname = False
		ctx.verify_mode = ssl.CERT_NONE
		return ctx
	
	def _recargarTraducciones(self):
		if not _EN_NVDA:
			return
		try:
			import gettext as _gt
			if hasattr(_gt, '_translations'):
				claves = [
					k for k in _gt._translations
					if isinstance(k, tuple) and any(
						self._ruta_idiomas in str(p) for p in k if isinstance(p, str)
					)
				]
				for k in claves:
					del _gt._translations[k]
			log.info(
				"ActualizadorRecursos: caché de traducciones limpiada, "
				"los nuevos archivos .mo se cargarán en el próximo reinicio de NVDA"
			)
		except Exception as e:
			log.warning(f"No se pudo recargar: {e}")
	
	def _notificar(self, mensaje):
		"""Registra el mensaje en el log. Si notificar_usuario=True, también lo habla."""
		log.info(f"ActualizadorRecursos: {mensaje}")
		if not _EN_NVDA:
			return
		if self._config["notificar_usuario"]:
			try:
				wx.CallAfter(ui.message, mensaje)
			except Exception:
				pass
