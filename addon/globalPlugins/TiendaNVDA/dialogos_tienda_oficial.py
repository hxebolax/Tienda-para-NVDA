# -*- coding: utf-8 -*-
# Copyright (C) 2021-2025 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.
#
# Diálogo de la tienda oficial de NVDA
#

import addonHandler
import gui
from gui import addonGui
import ui
import core
from logHandler import log
from tones import beep
import wx
import os
import traceback

from . import ajustes
from . import tienda_oficial
from .addon_manager import AddonManager
from .dialogos_comunes import (
	ID_FILTRO_TODOS, ID_MENU_COPIAR_INFO, ID_MENU_COPIAR_DOWNLOAD,
	copiar_al_portapapeles, construir_menu_gestion, preguntar_reinicio,
)

addonHandler.initTranslation()


class TiendaOficialApp(wx.Dialog):
	"""Ventana principal de la tienda oficial de NVDA"""

	def __init__(self, parent, addons):
		super().__init__(parent, title=_("Tienda Oficial NVDA"), size=(1200, 700))
		ajustes.IS_WinON = True
		self.addons = addons
		self.temporal = []
		self.snapshotInicial = AddonManager.getSnapshot()
		AddonManager.refreshCache()
		self._createUI()
		self.CenterOnScreen()
		self._cargarAddons()

	def _createUI(self):
		panel = wx.Panel(self)
		mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		leftSizer = wx.BoxSizer(wx.VERTICAL)
		rightSizer = wx.BoxSizer(wx.VERTICAL)

		leftSizer.Add(wx.StaticText(panel, label=_("&Buscar:")), 0, wx.ALL, 5)
		self.textoBusqueda = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
		self.textoBusqueda.Bind(wx.EVT_TEXT_ENTER, self.onBusqueda)
		leftSizer.Add(self.textoBusqueda, 0, wx.EXPAND | wx.ALL, 5)

		leftSizer.Add(wx.StaticText(panel, label=_("&Canal:")), 0, wx.ALL, 5)
		self.canalChoice = wx.Choice(panel, choices=[_("Todos"), _("Estable"), _("Beta"), _("Desarrollo")])
		self.canalChoice.SetSelection(0)
		self.canalChoice.Bind(wx.EVT_CHOICE, self.onCambiarCanal)
		leftSizer.Add(self.canalChoice, 0, wx.EXPAND | wx.ALL, 5)

		leftSizer.Add(wx.StaticText(panel, label=_("&Lista complementos:")), 0, wx.ALL, 5)
		self.listboxComplementos = wx.ListBox(panel)
		self.listboxComplementos.Bind(wx.EVT_LISTBOX, self.onSeleccion)
		self.listboxComplementos.Bind(wx.EVT_KEY_UP, self.onListboxKey)
		self.listboxComplementos.Bind(wx.EVT_CONTEXT_MENU, self.menuListBox)
		leftSizer.Add(self.listboxComplementos, 1, wx.EXPAND | wx.ALL, 5)
		self.accionBtn = wx.Button(panel, label=_("&Acción"))
		self.accionBtn.Bind(wx.EVT_BUTTON, self.menuListBox)
		leftSizer.Add(self.accionBtn, 0, wx.EXPAND | wx.ALL, 5)

		rightSizer.Add(wx.StaticText(panel, label=_("&Información:")), 0, wx.ALL, 5)
		self.txtResultado = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
		self.txtResultado.Bind(wx.EVT_KEY_UP, self.ontxtResultado)
		rightSizer.Add(self.txtResultado, 1, wx.EXPAND | wx.ALL, 5)

		btnSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.instalacionBtn = wx.Button(panel, label=_("&Instalar"))
		self.descargarBtn = wx.Button(panel, label=_("&Descargar"))
		self.webBtn = wx.Button(panel, label=_("&Página WEB"))
		self.salirBtn = wx.Button(panel, label=_("&Salir"))
		btnSizer.Add(self.instalacionBtn, 1, wx.ALL, 5)
		btnSizer.Add(self.descargarBtn, 1, wx.ALL, 5)
		btnSizer.Add(self.webBtn, 1, wx.ALL, 5)
		btnSizer.Add(self.salirBtn, 1, wx.ALL, 5)
		rightSizer.Add(btnSizer, 0, wx.EXPAND)

		mainSizer.Add(leftSizer, 1, wx.EXPAND | wx.ALL, 5)
		mainSizer.Add(rightSizer, 2, wx.EXPAND | wx.ALL, 5)
		panel.SetSizer(mainSizer)

		self.instalacionBtn.Bind(wx.EVT_BUTTON, self.onInstalarDirecto)
		self.descargarBtn.Bind(wx.EVT_BUTTON, self.onDescargar)
		self.webBtn.Bind(wx.EVT_BUTTON, self.onWeb)
		self.salirBtn.Bind(wx.EVT_BUTTON, self.onSalir)
		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)
		self.Bind(wx.EVT_CLOSE, self.onSalir)

	def _cargarAddons(self, canal=None):
		self.listboxComplementos.Clear()
		self.temporal.clear()
		self.addonsVisibles = []
		itemsArr = []
		installedDict = AddonManager.getInstalledAddonsDict()
		for addon in self.addons:
			if canal and addon.channel != canal:
				continue
			self.temporal.append(addon)
			self.addonsVisibles.append(addon)
			indicator = AddonManager.getAddonStatusIndicator(
				addon.addonId, addon.addonVersionName,
				".".join(map(str, addon.minNVDAVersion)),
				".".join(map(str, addon.lastTestedVersion)),
				installedDict=installedDict
			)
			itemsArr.append(f"{addon.addonId} - {addon.displayName} [{addon.channelDisplay}] {indicator}")
		self.listboxComplementos.AppendItems(itemsArr)
		if self.listboxComplementos.GetCount() > 0:
			self.listboxComplementos.SetSelection(0)
			self.onSeleccion(None)

	def onCambiarCanal(self, event):
		canales = [None, "stable", "beta", "dev"]
		sel = self.canalChoice.GetSelection()
		self._cargarAddons(canales[sel] if sel > 0 else None)

	def onBusqueda(self, event):
		buscar = self.textoBusqueda.GetValue().strip().lower()
		self.listboxComplementos.Clear()
		self.addonsVisibles = []
		itemsArr = []
		installedDict = AddonManager.getInstalledAddonsDict()
		source = self.temporal if not buscar else [a for a in self.temporal if buscar in a.displayName.lower() or buscar in a.description.lower() or buscar in a.addonId.lower()]
		for addon in source:
			self.addonsVisibles.append(addon)
			indicator = AddonManager.getAddonStatusIndicator(addon.addonId, addon.addonVersionName, ".".join(map(str, addon.minNVDAVersion)), ".".join(map(str, addon.lastTestedVersion)), installedDict=installedDict)
			itemsArr.append(f"{addon.addonId} - {addon.displayName} [{addon.channelDisplay}] {indicator}")
		if not itemsArr:
			self.listboxComplementos.Append(_("No se encontraron resultados"))
		else:
			self.listboxComplementos.AppendItems(itemsArr)
		if self.listboxComplementos.GetCount() > 0:
			self.listboxComplementos.SetSelection(0)
			self.onSeleccion(None)

	def _getAddon(self):
		sel = self.listboxComplementos.GetSelection()
		if sel == -1 or not hasattr(self, 'addonsVisibles') or sel >= len(self.addonsVisibles):
			return None
		return self.addonsVisibles[sel]

	def onSeleccion(self, event):
		addon = self._getAddon()
		if not addon:
			return
		indicator = AddonManager.getAddonStatusIndicator(addon.addonId, addon.addonVersionName, ".".join(map(str, addon.minNVDAVersion)), ".".join(map(str, addon.lastTestedVersion)))
		self.instalacionBtn.SetLabel(_("&Actualizar") if indicator in ["[U]", "[U-I]"] else _("&Instalar"))
		self.instalacionBtn.Enable(indicator not in ["[I]", "[D]", "[R]", "[I-I]"])

		installed = AddonManager.getInstalledAddonsDict()
		local_info = ""
		addon_id = addon.addonId.lower()
		if addon_id in installed:
			lcl = installed[addon_id]
			estado = _("Activo")
			if lcl.get('isBlocked', False):
				estado = _("Deshabilitado (incompatible)") if not lcl.get('overrideIncompatibility', False) else _("Habilitado (compatibilidad anulada)")
			elif lcl['isDisabled']:
				estado = _("Deshabilitado")
			local_info = _("\n--- INFORMACIÓN DE INSTALACIÓN LOCAL ---\n")
			local_info += _("Estado: {}\n").format(estado)
			local_info += _("Versión: {}\n").format(lcl['version'])

		ficha = _("RESUMEN DEL COMPLEMENTO (OFICIAL)\n")
		ficha += "========================================\n"
		ficha += _("Nombre: {}\n").format(addon.displayName)
		ficha += _("ID: {}\n").format(addon.addonId)
		ficha += _("Editor: {}\n").format(addon.publisher)
		ficha += _("Versión: {}\n").format(addon.addonVersionName)
		ficha += _("Canal: {}\n").format(addon.channelDisplay)
		ficha += _("Compatible: {}\n").format(_("Sí") if addon.isCompatible else _("No"))
		ficha += local_info
		ficha += "\n" + _("DESCRIPCIÓN:") + "\n"
		ficha += "----------------------------------------\n"
		ficha += (addon.description or _("Sin descripción.")) + "\n"
		self.txtResultado.SetValue(ficha)
		self.txtResultado.SetInsertionPoint(0)

	def onFichaTrans(self):
		if not ajustes.tempTrans:
			ui.message(_("Active la traducción en opciones de la tienda."))
			return
		addon = self._getAddon()
		if not addon:
			return
		target_lang = ajustes.langDict.get(ajustes.tempLang)
		from .cache_manager import CacheManager
		cache = CacheManager(ajustes.dirDatos, ajustes.tiempoDict, lambda: ajustes.tempCacheInterval, lambda: ajustes.tempServerCache, lambda: ajustes.tempUseTranslationCache)
		traduccion = cache.getTranslation(addon.description, target_lang)
		if not traduccion:
			beep(400, 150)
			try:
				from . import traductor
				traduccion = traductor.translate(addon.description, target_lang)
				cache.saveTranslation(addon.description, traduccion, target_lang)
			except:
				traduccion = addon.description
				ui.message(_("No se pudo traducir"))
		ficha = _("RESUMEN (TRADUCIDO - OFICIAL)\n")
		ficha += "========================================\n"
		ficha += _("Nombre: {}\n").format(addon.displayName)
		ficha += _("ID: {}\n").format(addon.addonId)
		ficha += _("Editor: {}\n").format(addon.publisher)
		ficha += _("Versión: {}\n").format(addon.addonVersionName)
		ficha += "\n" + _("DESCRIPCIÓN TRADUCIDA:") + "\n"
		ficha += "----------------------------------------\n"
		ficha += traduccion + "\n"
		self.txtResultado.SetValue(ficha)
		self.txtResultado.SetInsertionPoint(0)
		beep(100, 150)

	def ontxtResultado(self, event):
		if event.GetKeyCode() == wx.WXK_F3:
			self.onFichaTrans()
		else:
			event.Skip()

	def menuListBox(self, event):
		menu = wx.Menu()
		canalesMenu = wx.Menu()
		for i, c in enumerate([_("Todos"), _("Estable"), _("Beta"), _("Desarrollo")]):
			item = canalesMenu.Append(2000 + i, c)
			self.Bind(wx.EVT_MENU, lambda e, idx=i: (self.canalChoice.SetSelection(idx), self.onCambiarCanal(None)), item)
		menu.AppendSubMenu(canalesMenu, _("&Canales"))

		addon = self._getAddon()
		if addon:
			menu.AppendSeparator()
			menu.Append(ID_MENU_COPIAR_INFO, _("Copiar ficha"))
			menu.Append(ID_MENU_COPIAR_DOWNLOAD, _("Copiar enlace de descarga"))
			self.Bind(wx.EVT_MENU, lambda e: copiar_al_portapapeles(self.txtResultado.GetValue()), id=ID_MENU_COPIAR_INFO)
			self.Bind(wx.EVT_MENU, lambda e: copiar_al_portapapeles(addon.URL), id=ID_MENU_COPIAR_DOWNLOAD)

			# Gestión instalado (con empaquetador y documentación)
			installed = AddonManager.getInstalledAddonsDict()
			gestionMenu = construir_menu_gestion(self, addon.addonId, installed)
			if gestionMenu:
				menu.AppendSubMenu(gestionMenu, _("&Gestión instalado"))

		if event and event.GetEventObject() == self.accionBtn:
			self.PopupMenu(menu, self.accionBtn.GetPosition())
		else:
			self.PopupMenu(menu)

	def onListboxKey(self, event):
		keyCode = event.GetKeyCode()
		if keyCode == wx.WXK_F1:
			if event.ControlDown():
				self._explicarIndicador()
			else:
				sel = self.listboxComplementos.GetSelection()
				if sel != -1:
					ui.message(_("Complemento {} de {}").format(sel + 1, self.listboxComplementos.GetCount()))
		elif keyCode == wx.WXK_F2:
			ui.message(self.txtResultado.GetValue())
		elif keyCode == wx.WXK_F3:
			self.onFichaTrans()
		else:
			self.onSeleccion(event)
			event.Skip()

	def _explicarIndicador(self):
		addon = self._getAddon()
		if not addon:
			return
		installedDict = AddonManager.getInstalledAddonsDict()
		indicator = AddonManager.getAddonStatusIndicator(addon.addonId, addon.addonVersionName, ".".join(map(str, addon.minNVDAVersion)), ".".join(map(str, addon.lastTestedVersion)), installedDict=installedDict)
		explanation = AddonManager.getIndicatorExplanation(indicator)
		ui.message(_("Indicador: {indicator}\nFuente: [OF] Tienda Oficial NVDA\n{explanation}").format(indicator=indicator if indicator else _("Sin indicador"), explanation=explanation))

	def onInstalarDirecto(self, event):
		addon = self._getAddon()
		if not addon:
			return
		if not addon.isCompatible:
			if not ajustes.tempAllowIncompatible:
				gui.messageBox(_("Este complemento no es compatible con su versión de NVDA."), _("Incompatible"), wx.ICON_ERROR)
				return
			elif gui.messageBox(_("Este complemento no es compatible. ¿Desea intentar instalarlo de todos modos?"), _("Advertencia"), wx.YES_NO | wx.ICON_WARNING) == wx.NO:
				return
		path_temp = os.path.join(ajustes.dirDatos, "temp_install_oficial.nvda-addon")
		from .dialogos_actualizaciones import DescargaDialogo
		dlg = DescargaDialogo(self, _("Preparando instalación de %s...") % addon.displayName, addon.URL, path_temp, 60, isInstaller=True)
		if dlg.ShowModal() == ajustes.ID_TRUE:
			if tienda_oficial.verificar_checksum(path_temp, addon.sha256):
				if AddonManager.installAddon(path_temp, silent=ajustes.tempSilentInstall):
					if ajustes.tempSilentInstall:
						ui.message(_("Instalación de %s completada.") % addon.displayName)
						if gui.messageBox(_("¿Desea reiniciar NVDA ahora?"), _("Reiniciar"), wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
							core.restart()
				wx.CallLater(5000, lambda: self._borrarTemp(path_temp))
			else:
				ui.message(_("Error: El archivo descargado está corrupto"))
				self._borrarTemp(path_temp)
		dlg.Destroy()

	def _borrarTemp(self, path):
		try:
			if os.path.exists(path):
				os.remove(path)
		except:
			pass

	def onDescargar(self, event):
		addon = self._getAddon()
		if not addon:
			return
		if ajustes.IS_Download:
			ui.message(_("Ya hay una descarga en progreso"))
			return
		nombreFile = f"{addon.addonId}-{addon.addonVersionName}.nvda-addon"
		wildcard = _("Complemento de NVDA (*.nvda-addon)|*.nvda-addon")
		dlg = wx.FileDialog(self, message=_("Guardar en..."), defaultDir=os.environ.get('USERPROFILE', ''), defaultFile=nombreFile, wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			dlg.Destroy()
			ajustes.IS_Download = True
			from .dialogos_actualizaciones import DescargaDialogo
			descargaDlg = DescargaDialogo(self, _("Descargando %s...") % addon.displayName, addon.URL, path, 60)
			result = descargaDlg.ShowModal()
			if result == ajustes.ID_TRUE:
				if tienda_oficial.verificar_checksum(path, addon.sha256):
					if ajustes.tempInstall:
						addonGui.handleRemoteAddonInstall(path)
				else:
					ui.message(_("Error: El archivo descargado está corrupto"))
					try:
						os.remove(path)
					except:
						pass
			descargaDlg.Destroy()
		else:
			dlg.Destroy()
		ajustes.IS_Download = False

	def onWeb(self, event):
		addon = self._getAddon()
		if addon and addon.homepage:
			wx.LaunchDefaultBrowser(addon.homepage)

	def onSalir(self, event):
		ajustes.IS_WinON = False
		preguntar_reinicio(self.snapshotInicial)
		self.Destroy()
		gui.mainFrame.postPopup()

	def onKeyPress(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.onSalir(None)
		else:
			event.Skip()
