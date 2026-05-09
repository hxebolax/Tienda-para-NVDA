# -*- coding: utf-8 -*-
# Copyright (C) 2021-2025 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.
#
# Módulo empaquetador - Funcionalidad extraída de addonPackager
# Permite empaquetar complementos individuales y ver documentación
#

import addonHandler
import wx
import os
import zipfile
from threading import Thread
from logHandler import log

addonHandler.initTranslation()


def zipfolder(foldername, target_dir, addon=True):
	"""Empaqueta un directorio como .nvda-addon"""
	ext = '.nvda-addon' if addon else ''
	zipobj = zipfile.ZipFile(foldername + ext, 'w', zipfile.ZIP_DEFLATED)
	rootlen = len(target_dir) + 1
	for base, dirs, files in os.walk(target_dir):
		if addon and '__pycache__' in dirs:
			dirs.remove('__pycache__')
		for fname in files:
			fn = os.path.join(base, fname)
			zipobj.write(fn, fn[rootlen:])
	zipobj.close()


def empaquetar_complemento_individual(addon_obj, directorio):
	"""Empaqueta un complemento individual en el directorio dado.
	
	Args:
		addon_obj: Objeto addon de NVDA (addonHandler.Addon)
		directorio: Directorio destino donde guardar el .nvda-addon
	"""
	import ui
	try:
		name = addon_obj.manifest["name"]
		version = addon_obj.manifest["version"].replace(":", "_")
		addonSave = os.path.join(directorio, f"{name}_{version}_Gen")
		zipfolder(addonSave, addon_obj.path)
		wx.CallAfter(ui.message, _("Complemento empaquetado correctamente en: {}").format(addonSave + ".nvda-addon"))
	except Exception as e:
		log.error(f"Error al empaquetar complemento: {e}")
		wx.CallAfter(ui.message, _("Error al empaquetar el complemento: {}").format(e))
