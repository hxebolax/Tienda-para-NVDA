# -*- coding: utf-8 -*-
# Copyright (C) 2021-2025 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.
#
# Funciones y constantes comunes para los diálogos de tienda
#

import addonHandler
import wx

addonHandler.initTranslation()

# IDs para menús y filtros
ID_FILTRO_TODOS = 100
ID_FILTRO_2026 = 101
ID_FILTRO_2025 = 102
ID_FILTRO_2024 = 103
ID_FILTRO_2023 = 104
ID_FILTRO_AUTOR = 105
ID_FILTRO_DOWNLOADS = 106

ID_MENU_COPIAR_INFO = 150
ID_MENU_COPIAR_URL = 151
ID_MENU_FICHA_TRANS = 152
ID_MENU_COPIAR_DOWNLOAD = 153
ID_MENU_COPIAR_ENLACE_ES = 154

ID_GESTION_HABILITAR = 160
ID_GESTION_DESHABILITAR = 161
ID_GESTION_ELIMINAR = 162
ID_GESTION_EMPAQUETAR = 163
ID_GESTION_DOCUMENTACION = 164


def copiar_al_portapapeles(texto: str):
	"""Copia texto al portapapeles"""
	import ui
	if not texto:
		return
	if wx.TheClipboard.Open():
		wx.TheClipboard.SetData(wx.TextDataObject(texto))
		wx.TheClipboard.Close()
		ui.message(_("Copiado al portapapeles"))


def construir_url_descarga_es(nombre_interno: str) -> str:
	"""Construye la URL interna de descarga de nvda.es para un complemento"""
	# Formato: https://nvda.es/files/get.php?file=NombreInterno
	return f"https://nvda.es/files/get.php?file={nombre_interno}"


def gestion_addon_comun(parent, accion, name):
	"""Lógica común de gestión de complementos (habilitar/deshabilitar/desinstalar)"""
	import gui
	import ui
	import addonHandler
	import traceback
	from logHandler import log
	from . import ajustes
	from .addon_manager import AddonManager

	res = False
	try:
		if accion == "enable":
			res = AddonManager.enableAddon(name)
		elif accion == "disable":
			res = AddonManager.disableAddon(name)
		elif accion == "uninstall":
			if gui.messageBox(
				_("¿Está seguro de que desea desinstalar este complemento?"),
				_("Confirmar"), wx.YES_NO | wx.ICON_QUESTION
			) == wx.YES:
				res = AddonManager.uninstallAddon(name)
	except addonHandler.AddonError:
		if accion == "enable":
			if gui.messageBox(
				_("Este complemento no es compatible con su versión de NVDA. ¿Desea intentar habilitarlo de todos modos?"),
				_("Advertencia de compatibilidad"), wx.YES_NO | wx.ICON_WARNING
			) == wx.YES:
				res = AddonManager.enableAddon(name, override=True)
		else:
			log.error(f"Error en gestión de addon {name}: {traceback.format_exc()}")

	if res:
		ajustes.reiniciarTrue = True
		AddonManager.refreshCache()
		wx.CallAfter(ui.message, _("Operación realizada con éxito. Algunos cambios requieren reiniciar NVDA."))
	return res


def preguntar_reinicio(snapshotInicial):
	"""Pregunta si reiniciar NVDA si hay cambios pendientes"""
	import gui
	import core
	from . import ajustes
	from .addon_manager import AddonManager

	if ajustes.reiniciarTrue or AddonManager.hasChanged(snapshotInicial):
		if gui.messageBox(
			_("Se han realizado cambios en los complementos que requieren reiniciar NVDA para surtir efecto. ¿Desea reiniciar ahora?"),
			_("Reiniciar NVDA"), wx.YES_NO | wx.ICON_QUESTION
		) == wx.YES:
			ajustes.reiniciarTrue = False
			core.restart()
	ajustes.reiniciarTrue = False


def construir_menu_gestion(parent, addon_id, installed_dict):
	"""Construye el submenú de gestión para un complemento instalado.
	Incluye Empaquetador y Documentación."""
	import addonHandler
	import os

	addon_id_lower = addon_id.lower()
	if addon_id_lower not in installed_dict:
		return None

	lcl = installed_dict[addon_id_lower]
	gestionMenu = wx.Menu()

	# Habilitar/Deshabilitar
	isEffectivelyDisabled = lcl['isDisabled'] or (lcl.get('isBlocked', False) and not lcl.get('overrideIncompatibility', False))
	if isEffectivelyDisabled:
		it = gestionMenu.Append(ID_GESTION_HABILITAR, _("Habilitar complemento"))
		parent.Bind(wx.EVT_MENU, lambda e: gestion_addon_comun(parent, "enable", addon_id), it)
	else:
		it = gestionMenu.Append(ID_GESTION_DESHABILITAR, _("Deshabilitar complemento"))
		parent.Bind(wx.EVT_MENU, lambda e: gestion_addon_comun(parent, "disable", addon_id), it)

	# Desinstalar
	it2 = gestionMenu.Append(ID_GESTION_ELIMINAR, _("Desinstalar complemento"))
	parent.Bind(wx.EVT_MENU, lambda e: gestion_addon_comun(parent, "uninstall", addon_id), it2)

	gestionMenu.AppendSeparator()

	# Empaquetador de complementos
	addon_obj = lcl.get('obj')
	if addon_obj:
		it3 = gestionMenu.Append(ID_GESTION_EMPAQUETAR, _("Empaquetador de complementos"))
		parent.Bind(wx.EVT_MENU, lambda e, obj=addon_obj: _empaquetar_addon(parent, obj), it3)

		# Ver documentación
		doc_path = None
		try:
			doc_path = addonHandler.Addon(addon_obj.path).getDocFilePath()
		except:
			pass
		if doc_path and os.path.exists(doc_path):
			it4 = gestionMenu.Append(ID_GESTION_DOCUMENTACION, _("Ver documentación"))
			parent.Bind(wx.EVT_MENU, lambda e, p=doc_path: wx.LaunchDefaultBrowser('file://' + p, flags=0), it4)

	return gestionMenu


def _empaquetar_addon(parent, addon_obj):
	"""Empaqueta un complemento individual"""
	import ui
	from .empaquetador import empaquetar_complemento_individual
	dlg = wx.DirDialog(parent, _("Seleccione un directorio para guardar:"), style=wx.DD_DEFAULT_STYLE)
	if dlg.ShowModal() == wx.ID_OK:
		directorio = dlg.GetPath()
		dlg.Destroy()
		empaquetar_complemento_individual(addon_obj, directorio)
	else:
		dlg.Destroy()
