# -*- coding: utf-8 -*-
# Copyright (C) 2021-2025 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.
#
# Diálogo de la tienda unificada (NVDA.ES + Oficial)
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
from . import basedatos
from . import tienda_oficial
from . import version_utils
from .addon_manager import AddonManager
from .dialogos_comunes import (
	ID_FILTRO_TODOS, ID_MENU_COPIAR_INFO, ID_MENU_COPIAR_DOWNLOAD, ID_MENU_COPIAR_ENLACE_ES,
	copiar_al_portapapeles, construir_url_descarga_es, construir_menu_gestion, preguntar_reinicio,
)

addonHandler.initTranslation()


class TiendaUnificadaApp(wx.Dialog):
	"""Ventana unificada con todas las fuentes de complementos"""

	def __init__(self, parent, datosES, addonsOficial):
		super().__init__(parent, title=_("Tienda Unificada de Complementos"), size=(1300, 750))
		ajustes.IS_WinON = True
		self.datosES = datosES
		self.addonsOficial = addonsOficial
		self.todosAddons = []
		self.snapshotInicial = AddonManager.getSnapshot()
		AddonManager.refreshCache()
		self._createUI()
		self.CenterOnScreen()
		self._cargarTodos()

	def _createUI(self):
		panel = wx.Panel(self)
		mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		leftSizer = wx.BoxSizer(wx.VERTICAL)
		rightSizer = wx.BoxSizer(wx.VERTICAL)

		leftSizer.Add(wx.StaticText(panel, label=_("&Buscar:")), 0, wx.ALL, 5)
		self.textoBusqueda = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
		self.textoBusqueda.Bind(wx.EVT_TEXT_ENTER, self.onBusqueda)
		leftSizer.Add(self.textoBusqueda, 0, wx.EXPAND | wx.ALL, 5)

		leftSizer.Add(wx.StaticText(panel, label=_("&Fuente:")), 0, wx.ALL, 5)
		self.fuenteChoice = wx.Choice(panel, choices=[_("Todas las fuentes"), _("NVDA.ES"), _("Tienda Oficial")])
		self.fuenteChoice.SetSelection(0)
		self.fuenteChoice.Bind(wx.EVT_CHOICE, self.onCambiarFuente)
		leftSizer.Add(self.fuenteChoice, 0, wx.EXPAND | wx.ALL, 5)

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
		self.salirBtn = wx.Button(panel, label=_("&Salir"))
		btnSizer.Add(self.instalacionBtn, 1, wx.ALL, 5)
		btnSizer.Add(self.descargarBtn, 1, wx.ALL, 5)
		btnSizer.Add(self.salirBtn, 1, wx.ALL, 5)
		rightSizer.Add(btnSizer, 0, wx.EXPAND)

		mainSizer.Add(leftSizer, 1, wx.EXPAND | wx.ALL, 5)
		mainSizer.Add(rightSizer, 2, wx.EXPAND | wx.ALL, 5)
		panel.SetSizer(mainSizer)

		self.instalacionBtn.Bind(wx.EVT_BUTTON, self.onInstalarDirecto)
		self.descargarBtn.Bind(wx.EVT_BUTTON, self.onDescargar)
		self.salirBtn.Bind(wx.EVT_BUTTON, self.onSalir)
		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)
		self.Bind(wx.EVT_CLOSE, self.onSalir)

	def _getIndicatorES(self, addon, installedDict):
		indicator = ""
		for link in addon['links']:
			ind = AddonManager.getAddonStatusIndicator(addon['name'], link['version'], link.get('minimum'), link.get('lasttested'), installedDict=installedDict)
			if ind in ["[U]", "[U-I]"]:
				indicator = ind
				break
			if ind in ["[I]", "[I-I]", "[X]"]:
				indicator = ind
			if not indicator and ind in ["[D]", "[R]"]:
				indicator = ind
		if not indicator and addon['name'].lower() in installedDict:
			indicator = "[I]"
		return indicator

	def _cargarTodos(self, fuente=None):
		self.listboxComplementos.Clear()
		self.todosAddons.clear()
		self.addonsVisibles = []
		poolES = self.datosES.dataServidor if self.datosES and self.datosES.dataServidor else []
		poolOF = self.addonsOficial if self.addonsOficial else []
		itemsArr = []
		installedDict = AddonManager.getInstalledAddonsDict()

		if fuente in [None, "nvda_es"]:
			for addon in poolES:
				self.todosAddons.append(("nvda_es", addon))
				self.addonsVisibles.append(("nvda_es", addon))
				indicator = self._getIndicatorES(addon, installedDict)
				itemsArr.append(f"{addon['name']} - {addon['summary']} [ES] {indicator}")

		if fuente in [None, "oficial"]:
			for addon in poolOF:
				self.todosAddons.append(("oficial", addon))
				self.addonsVisibles.append(("oficial", addon))
				indicator = AddonManager.getAddonStatusIndicator(addon.addonId, addon.addonVersionName, ".".join(map(str, addon.minNVDAVersion)), ".".join(map(str, addon.lastTestedVersion)), installedDict=installedDict)
				itemsArr.append(f"{addon.addonId} - {addon.displayName} [OF] {indicator}")

		self.listboxComplementos.AppendItems(itemsArr)
		if self.listboxComplementos.GetCount() > 0:
			self.listboxComplementos.SetSelection(0)
			self.onSeleccion(None)

	def onCambiarFuente(self, event):
		fuentes = [None, "nvda_es", "oficial"]
		self._cargarTodos(fuentes[self.fuenteChoice.GetSelection()])

	def onBusqueda(self, event):
		buscar = self.textoBusqueda.GetValue().strip().lower()
		self.listboxComplementos.Clear()
		self.addonsVisibles = []
		itemsArr = []
		installedDict = AddonManager.getInstalledAddonsDict()
		for fuente, addon in self.todosAddons:
			match = True
			if buscar:
				if fuente == "nvda_es":
					match = buscar in addon['summary'].lower() or buscar in addon.get('description', '').lower() or buscar in addon['name'].lower()
				else:
					match = buscar in addon.displayName.lower() or buscar in addon.description.lower() or buscar in addon.addonId.lower()
			if match:
				self.addonsVisibles.append((fuente, addon))
				if fuente == "nvda_es":
					indicator = self._getIndicatorES(addon, installedDict)
					itemsArr.append(f"{addon['name']} - {addon['summary']} [ES] {indicator}")
				else:
					indicator = AddonManager.getAddonStatusIndicator(addon.addonId, addon.addonVersionName, ".".join(map(str, addon.minNVDAVersion)), ".".join(map(str, addon.lastTestedVersion)), installedDict=installedDict)
					itemsArr.append(f"{addon.addonId} - {addon.displayName} [OF] {indicator}")
		if not itemsArr:
			self.listboxComplementos.Append(_("No se encontraron resultados"))
		else:
			self.listboxComplementos.AppendItems(itemsArr)
		if self.listboxComplementos.GetCount() > 0:
			self.listboxComplementos.SetSelection(0)
			self.onSeleccion(None)

	def _getVisible(self):
		sel = self.listboxComplementos.GetSelection()
		if sel == -1 or not hasattr(self, 'addonsVisibles') or sel >= len(self.addonsVisibles):
			return None, None
		return self.addonsVisibles[sel]

	def onSeleccion(self, event):
		fuente, addon = self._getVisible()
		if not addon:
			return
		if fuente == "nvda_es":
			indicator = self._getIndicatorES(addon, AddonManager.getInstalledAddonsDict())
		else:
			indicator = AddonManager.getAddonStatusIndicator(addon.addonId, addon.addonVersionName, ".".join(map(str, addon.minNVDAVersion)), ".".join(map(str, addon.lastTestedVersion)))
		self.instalacionBtn.SetLabel(_("&Actualizar") if indicator in ["[U]", "[U-I]"] else _("&Instalar"))
		self.instalacionBtn.Enable(indicator not in ["[I]", "[D]", "[R]", "[I-I]"])

		installed = AddonManager.getInstalledAddonsDict()
		local_info = ""
		addon_id = (addon['name'] if fuente == "nvda_es" else addon.addonId).lower()
		if addon_id in installed:
			lcl = installed[addon_id]
			estado = _("Activo")
			if lcl.get('isBlocked', False):
				estado = _("Deshabilitado (incompatible)") if not lcl.get('overrideIncompatibility', False) else _("Habilitado (compatibilidad anulada)")
			elif lcl['isDisabled']:
				estado = _("Deshabilitado")
			local_info = _("\nESTADO LOCAL: {} (v{})\n").format(estado, lcl['version'])

		if fuente == "nvda_es":
			ficha = _("RESUMEN DEL COMPLEMENTO [NVDA.ES]\n")
			ficha += "========================================\n"
			ficha += _("Nombre: {}\n").format(addon['summary'])
			ficha += _("ID: {}\n").format(addon['name'])
			ficha += _("Autor: {}\n").format(addon['author'])
			ficha += _("Web: {}\n").format(addon.get('url', _('No disponible')))
			ficha += local_info
			ficha += "\n" + _("DESCRIPCIÓN:") + "\n"
			ficha += "----------------------------------------\n"
			ficha += (addon['description'] or _("Sin descripción.")) + "\n"
			ficha += "\n" + _("ENLACES:") + "\n"
			for link in addon['links']:
				ficha += _("Canal {}: v{} (Min NVDA: {})\n").format(link['channel'], link['version'], link['minimum'])
		else:
			ficha = _("RESUMEN DEL COMPLEMENTO [OFICIAL]\n")
			ficha += "========================================\n"
			ficha += _("Nombre: {}\n").format(addon.displayName)
			ficha += _("ID: {}\n").format(addon.addonId)
			ficha += _("Editor: {}\n").format(addon.publisher)
			ficha += _("Versión: {}\n").format(addon.addonVersionName)
			ficha += _("Canal: {}\n").format(addon.channelDisplay)
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
		fuente, addon = self._getVisible()
		if not addon:
			return
		beep(400, 150)
		desc = addon['description'] if fuente == "nvda_es" else addon.description
		target_lang = ajustes.langDict.get(ajustes.tempLang)
		from .cache_manager import CacheManager
		cache = CacheManager(ajustes.dirDatos, ajustes.tiempoDict, lambda: ajustes.tempCacheInterval, lambda: ajustes.tempServerCache, lambda: ajustes.tempUseTranslationCache)
		traduccion = cache.getTranslation(desc, target_lang)
		if not traduccion:
			try:
				from . import traductor
				traduccion = traductor.translate(desc, target_lang)
				cache.saveTranslation(desc, traduccion, target_lang)
			except:
				traduccion = desc
				ui.message(_("No se pudo traducir"))
		if fuente == "nvda_es":
			ficha = _("RESUMEN (TRADUCIDO - NVDA.ES)\n")
			ficha += "========================================\n"
			ficha += _("Nombre: {}\n").format(addon['summary'])
			ficha += _("ID: {}\n").format(addon['name'])
			ficha += "\n" + _("DESCRIPCIÓN TRADUCIDA:") + "\n"
			ficha += "----------------------------------------\n"
			ficha += traduccion + "\n"
		else:
			ficha = _("RESUMEN (TRADUCIDO - OFICIAL)\n")
			ficha += "========================================\n"
			ficha += _("Nombre: {}\n").format(addon.displayName)
			ficha += _("ID: {}\n").format(addon.addonId)
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
		fuente, addon = self._getVisible()
		if addon:
			menu.Append(ID_MENU_COPIAR_INFO, _("Copiar ficha"))
			self.Bind(wx.EVT_MENU, lambda e: copiar_al_portapapeles(self.txtResultado.GetValue()), id=ID_MENU_COPIAR_INFO)

			if fuente == "nvda_es":
				# Copiar enlace interno NVDA.ES
				it_es = menu.Append(ID_MENU_COPIAR_ENLACE_ES, _("Copiar enlace interno NVDA.ES"))
				self.Bind(wx.EVT_MENU, lambda e, n=addon['links'][0]['file']: copiar_al_portapapeles(construir_url_descarga_es(n)), it_es)
				if len(addon['links']) > 1:
					descargasSubMenu = wx.Menu()
					for link in addon['links']:
						item_link = descargasSubMenu.Append(wx.ID_ANY, _("Canal {}").format(link['channel']))
						self.Bind(wx.EVT_MENU, lambda e, url=link['link']: copiar_al_portapapeles(url), item_link)
					menu.AppendSubMenu(descargasSubMenu, _("Copiar enlace de descarga"))
				else:
					menu.Append(ID_MENU_COPIAR_DOWNLOAD, _("Copiar enlace de descarga"))
					self.Bind(wx.EVT_MENU, lambda e: copiar_al_portapapeles(addon['links'][0]['link']), id=ID_MENU_COPIAR_DOWNLOAD)
			else:
				menu.Append(ID_MENU_COPIAR_DOWNLOAD, _("Copiar enlace de descarga"))
				self.Bind(wx.EVT_MENU, lambda e: copiar_al_portapapeles(addon.URL), id=ID_MENU_COPIAR_DOWNLOAD)

			# Gestión instalado (con empaquetador y documentación)
			installed = AddonManager.getInstalledAddonsDict()
			addon_id = addon['name'] if fuente == "nvda_es" else addon.addonId
			gestionMenu = construir_menu_gestion(self, addon_id, installed)
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
		fuente, addon = self._getVisible()
		if not addon:
			return
		installedDict = AddonManager.getInstalledAddonsDict()
		if fuente == "nvda_es":
			indicator = self._getIndicatorES(addon, installedDict)
			source_label = "[ES] Tienda NVDA.ES"
		else:
			indicator = AddonManager.getAddonStatusIndicator(addon.addonId, addon.addonVersionName, ".".join(map(str, addon.minNVDAVersion)), ".".join(map(str, addon.lastTestedVersion)), installedDict=installedDict)
			source_label = "[OF] Tienda Oficial NVDA"
		explanation = AddonManager.getIndicatorExplanation(indicator)
		ui.message(_("Indicador: {indicator}\nFuente: {source}\n{explanation}").format(indicator=indicator if indicator else _("Sin indicador"), source=source_label, explanation=explanation))

	def onInstalarDirecto(self, event):
		fuente, addon = self._getVisible()
		if not addon:
			return
		if fuente == "nvda_es":
			url = self.datosES.urlBase + addon['links'][0]['file']
			summary = addon['summary']
			sha256 = None
			compatible = True
			minNVDA = addon['links'][0].get('minimum')
			lastTested = addon['links'][0].get('lasttested')
			if minNVDA and lastTested:
				try:
					compatible = version_utils.isAddonCompatible(version_utils.getAPIVersionTupleFromString(minNVDA), version_utils.getAPIVersionTupleFromString(lastTested))
				except:
					pass
		else:
			url = addon.URL
			summary = addon.displayName
			sha256 = addon.sha256
			compatible = addon.isCompatible

		if not compatible:
			if not ajustes.tempAllowIncompatible:
				gui.messageBox(_("Este complemento no es compatible con su versión de NVDA."), _("Incompatible"), wx.ICON_ERROR)
				return
			elif gui.messageBox(_("Este complemento no es compatible. ¿Desea intentar instalarlo de todos modos?"), _("Advertencia"), wx.YES_NO | wx.ICON_WARNING) == wx.NO:
				return

		path_temp = os.path.join(ajustes.dirDatos, "temp_install_unified.nvda-addon")
		from .dialogos_actualizaciones import DescargaDialogo
		dlg = DescargaDialogo(self, _("Preparando instalación de %s...") % summary, url, path_temp, 30, isInstaller=True)
		if dlg.ShowModal() == ajustes.ID_TRUE:
			valid = True
			if sha256:
				valid = tienda_oficial.verificar_checksum(path_temp, sha256)
			if valid:
				if AddonManager.installAddon(path_temp, silent=ajustes.tempSilentInstall):
					if ajustes.tempSilentInstall:
						ui.message(_("Instalación de %s completada.") % summary)
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
		fuente, addon = self._getVisible()
		if not addon:
			return
		if ajustes.IS_Download:
			ui.message(_("Ya hay una descarga en progreso"))
			return
		if fuente == "nvda_es":
			indice = self.datosES.indiceName(addon['name'])
			if indice is not None:
				datos = self.datosES.dataServidor[indice]
				if len(datos['links']) == 1:
					self._iniciarDescargaES(indice, 0)
				else:
					menu = wx.Menu()
					for i, link in enumerate(datos['links']):
						item = menu.Append(i, _("Canal {}").format(link['channel']))
						self.Bind(wx.EVT_MENU, lambda e, idx=i, idy=indice: self._iniciarDescargaES(idy, idx), item)
					self.PopupMenu(menu, self.descargarBtn.GetPosition())
		else:
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

	def _iniciarDescargaES(self, indice, canalIdx):
		datos = self.datosES.dataServidor[indice]
		url = self.datosES.urlBase + datos['links'][canalIdx]['file']
		nombreFile = self.datosES.GetFilenameDownload(datos['links'][canalIdx]['file'])
		if not nombreFile or nombreFile == "downloads":
			wx.LaunchDefaultBrowser(datos['links'][canalIdx]['link'])
			return
		wildcard = _("Complemento de NVDA (*.nvda-addon)|*.nvda-addon")
		dlg = wx.FileDialog(self, message=_("Guardar en..."), defaultDir=os.environ.get('USERPROFILE', ''), defaultFile=nombreFile, wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			dlg.Destroy()
			ajustes.IS_Download = True
			from .dialogos_actualizaciones import DescargaDialogo
			dlgP = DescargaDialogo(self, _("Descargando %s...") % os.path.basename(path), url, path, 15)
			result = dlgP.ShowModal()
			if result == ajustes.ID_TRUE:
				if ajustes.tempInstall:
					addonGui.handleRemoteAddonInstall(path)
			ajustes.IS_Download = False
			dlgP.Destroy()
		else:
			dlg.Destroy()

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
