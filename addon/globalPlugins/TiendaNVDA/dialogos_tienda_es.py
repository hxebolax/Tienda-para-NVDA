# -*- coding: utf-8 -*-
# Copyright (C) 2021-2025 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.
#
# Diálogo de la tienda NVDA.ES
#

import addonHandler
import gui
from gui import addonGui
import ui
import core
from logHandler import log
from tones import beep
import wx
import winsound
import os
import traceback

from . import ajustes
from . import basedatos
from . import version_utils
from .addon_manager import AddonManager
from .dialogos_comunes import (
	ID_FILTRO_TODOS, ID_FILTRO_2026, ID_FILTRO_2025, ID_FILTRO_2024, ID_FILTRO_2023,
	ID_FILTRO_AUTOR, ID_FILTRO_DOWNLOADS,
	ID_MENU_COPIAR_INFO, ID_MENU_COPIAR_URL, ID_MENU_FICHA_TRANS,
	ID_MENU_COPIAR_DOWNLOAD, ID_MENU_COPIAR_ENLACE_ES,
	copiar_al_portapapeles, construir_url_descarga_es, construir_menu_gestion, preguntar_reinicio,
)

addonHandler.initTranslation()


class TiendaApp(wx.Dialog):
	"""Ventana principal de la tienda NVDA.ES"""

	def __init__(self, parent, dataServidor):
		super().__init__(parent, title=ajustes.titulo, size=(1200, 700))
		ajustes.IS_WinON = True
		self.datos = dataServidor
		self.indiceFiltro = ajustes.indiceFiltro
		self.temporal = []
		self.snapshotInicial = AddonManager.getSnapshot()
		AddonManager.refreshCache()
		self._createUI()
		self.CenterOnScreen()
		wx.CallAfter(self.onCargaFiltro, self.indiceFiltro)
		self.onLisbox(None)

	def _createUI(self):
		panel = wx.Panel(self)
		mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		leftSizer = wx.BoxSizer(wx.VERTICAL)
		rightSizer = wx.BoxSizer(wx.VERTICAL)

		leftSizer.Add(wx.StaticText(panel, label=_("&Buscar:")), 0, wx.ALL, 5)
		self.textoBusqueda = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
		self.textoBusqueda.Bind(wx.EVT_TEXT_ENTER, self.onBusqueda)
		leftSizer.Add(self.textoBusqueda, 0, wx.EXPAND | wx.ALL, 5)
		self.buscarBtn = wx.Button(panel, label=_("B&uscar"))
		self.buscarBtn.Bind(wx.EVT_BUTTON, self.onBusqueda)
		leftSizer.Add(self.buscarBtn, 0, wx.EXPAND | wx.ALL, 5)

		leftSizer.Add(wx.StaticText(panel, label=_("&Lista complementos:")), 0, wx.ALL, 5)
		self.listboxComplementos = wx.ListBox(panel, style=wx.LB_SINGLE)
		self.listboxComplementos.Bind(wx.EVT_KEY_UP, self.onLisbox)
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
		self.servidorBtn = wx.Button(panel, label=_("&Cambiar servidor"))
		self.salirBtn = wx.Button(panel, label=_("&Salir"))
		btnSizer.Add(self.instalacionBtn, 1, wx.ALL, 5)
		btnSizer.Add(self.descargarBtn, 1, wx.ALL, 5)
		btnSizer.Add(self.webBtn, 1, wx.ALL, 5)
		btnSizer.Add(self.servidorBtn, 1, wx.ALL, 5)
		btnSizer.Add(self.salirBtn, 1, wx.ALL, 5)
		rightSizer.Add(btnSizer, 0, wx.EXPAND)

		mainSizer.Add(leftSizer, 1, wx.EXPAND | wx.ALL, 5)
		mainSizer.Add(rightSizer, 2, wx.EXPAND | wx.ALL, 5)
		panel.SetSizer(mainSizer)

		self.instalacionBtn.Bind(wx.EVT_BUTTON, self.onInstalarDirecto)
		self.descargarBtn.Bind(wx.EVT_BUTTON, self.onDescargar)
		self.webBtn.Bind(wx.EVT_BUTTON, self.onWeb)
		self.servidorBtn.Bind(wx.EVT_BUTTON, self.onCambiarServidor)
		self.salirBtn.Bind(wx.EVT_BUTTON, self.onSalir)
		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)
		self.Bind(wx.EVT_CLOSE, self.onSalir)

	def _getIndicatorForAddon(self, addon, installedDict):
		"""Obtiene el mejor indicador de estado para un addon ES"""
		indicator = ""
		for link in addon['links']:
			ind = AddonManager.getAddonStatusIndicator(
				addon['name'], link['version'], link.get('minimum'), link.get('lasttested'),
				installedDict=installedDict
			)
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

	def onCargaFiltro(self, event):
		try:
			indice = event.GetId() if hasattr(event, 'GetId') else event
		except:
			indice = event

		self.indiceFiltro = indice
		ajustes.indiceFiltro = indice
		self.temporal.clear()
		self.listboxComplementos.Clear()
		self.textoBusqueda.Clear()

		if not self.datos.dataServidor:
			return

		installedDict = AddonManager.getInstalledAddonsDict()
		titles = {
			ID_FILTRO_TODOS: _(" - Todos los complementos"),
			ID_FILTRO_2026: _(" - Complementos API 2026"),
			ID_FILTRO_2025: _(" - Complementos API 2025"),
			ID_FILTRO_2024: _(" - Complementos API 2024"),
			ID_FILTRO_2023: _(" - Complementos API 2023"),
			ID_FILTRO_AUTOR: _(" - Por autor"),
			ID_FILTRO_DOWNLOADS: _(" - Por descargas"),
		}
		self.SetTitle(ajustes.titulo + titles.get(indice, ""))

		year_filters = {
			ID_FILTRO_2026: "2026", ID_FILTRO_2025: "2025",
			ID_FILTRO_2024: "2024", ID_FILTRO_2023: "2023",
		}

		addons_to_show = self.datos.dataServidor
		if indice in year_filters:
			year = year_filters[indice]
			addons_to_show = [a for a in addons_to_show if any(l.get('lasttested', '').startswith(year) for l in a['links'])]
		elif indice == ID_FILTRO_AUTOR:
			addons_to_show = sorted(addons_to_show, key=lambda k: (k.get('author', '').lower(), k.get('summary', '').lower()))
		elif indice == ID_FILTRO_DOWNLOADS:
			addons_to_show = sorted(addons_to_show, key=lambda k: k['links'][0].get('downloads', 0), reverse=True)

		for addon in addons_to_show:
			indicator = self._getIndicatorForAddon(addon, installedDict)
			self.temporal.append(f"{addon['name']} - {addon['summary']} {indicator}")

		if indice in [ID_FILTRO_TODOS, ID_FILTRO_2026, ID_FILTRO_2025, ID_FILTRO_2024, ID_FILTRO_2023] and ajustes.tempOrden:
			self.listboxComplementos.AppendItems(sorted(self.temporal, key=str.lower))
		else:
			self.listboxComplementos.AppendItems(self.temporal)

		if self.listboxComplementos.GetCount() > 0:
			self.listboxComplementos.SetSelection(0)
			self.listboxComplementos.SetFocus()
			self.onLisbox(None)

	def onBusqueda(self, event):
		buscar = self.textoBusqueda.GetValue().strip()
		self.listboxComplementos.Clear()
		if not buscar:
			items = sorted(self.temporal, key=str.lower) if ajustes.tempOrden else self.temporal
			self.listboxComplementos.AppendItems(items)
		else:
			filtro = [item for item in self.temporal if buscar.lower() in item.lower()]
			if not filtro:
				self.listboxComplementos.Append(_("No se encontraron resultados"))
			else:
				items = sorted(filtro, key=str.lower) if ajustes.tempOrden else filtro
				self.listboxComplementos.AppendItems(items)
		if self.listboxComplementos.GetCount() > 0:
			self.listboxComplementos.SetSelection(0)
			self.listboxComplementos.SetFocus()

	def _getCleanName(self):
		sel = self.listboxComplementos.GetSelection()
		if sel == -1:
			return None
		nombre = self.listboxComplementos.GetString(sel)
		if nombre == _("No se encontraron resultados"):
			return None
		if " - " in nombre:
			return nombre.split(" - ", 1)[0].strip()
		return nombre

	def _explicarIndicador(self):
		nombre = self._getCleanName()
		if not nombre:
			return
		idx = self.datos.indiceName(nombre)
		if idx is None:
			return
		addon = self.datos.dataServidor[idx]
		installedDict = AddonManager.getInstalledAddonsDict()
		indicator = self._getIndicatorForAddon(addon, installedDict)
		explanation = AddonManager.getIndicatorExplanation(indicator)
		msg = _("Indicador: {indicator}\nFuente: [ES] Tienda NVDA.ES\n{explanation}").format(
			indicator=indicator if indicator else _("Sin indicador"),
			explanation=explanation
		)
		ui.message(msg)

	def onLisbox(self, event):
		sel = self.listboxComplementos.GetSelection()
		if sel == -1:
			return
		nombre = self.listboxComplementos.GetString(sel)
		if "[U]" in nombre or "[U-I]" in nombre:
			self.instalacionBtn.SetLabel(_("&Actualizar"))
		else:
			self.instalacionBtn.SetLabel(_("&Instalar"))
		if nombre == _("No se encontraron resultados"):
			self.txtResultado.Clear()
			return

		tecla = None
		if event:
			try:
				tecla = event.GetKeyCode()
			except:
				pass

		if tecla == wx.WXK_F1:
			if event and event.ControlDown():
				self._explicarIndicador()
			else:
				ui.message(_("Complemento {} de {}").format(sel + 1, self.listboxComplementos.GetCount()))
		elif tecla == wx.WXK_F2:
			ui.message(self.txtResultado.GetValue())
		elif tecla == wx.WXK_F3:
			self.onFichaTrans()
		else:
			self.onFicha()

		if any(ind in nombre for ind in ["[I]", "[D]", "[R]", "[I-I]"]) and "[U]" not in nombre and "[U-I]" not in nombre:
			self.instalacionBtn.Disable()
		else:
			self.instalacionBtn.Enable()

	def onFicha(self):
		nombre = self._getCleanName()
		if not nombre:
			return
		indice = self.datos.indiceName(nombre)
		if indice is None:
			return
		datos = self.datos.dataServidor[indice]
		installed = AddonManager.getInstalledAddonsDict()
		local_info = ""
		name_id = datos['name'].lower()
		if name_id in installed:
			addon = installed[name_id]
			estado = _("Activo")
			if addon.get('isBlocked', False):
				estado = _("Deshabilitado (incompatible)") if not addon.get('overrideIncompatibility', False) else _("Habilitado (compatibilidad anulada)")
			elif addon['isDisabled']:
				estado = _("Deshabilitado")
			if addon['isPendingRemove']:
				estado = _("Marcado para eliminar")
			if addon['isPendingInstall']:
				estado = _("Pendiente de instalar")
			local_info = _("\n--- INFORMACIÓN DE INSTALACIÓN LOCAL ---\n")
			local_info += _("Estado actual: {}\n").format(estado)
			local_info += _("Versión instalada: {}\n").format(addon['version'])
			if addon['obj'].requiresRestart:
				local_info += _("AVISO: Cambios pendientes. Reinicie NVDA.\n")
			if not addon['obj'].isCompatible:
				local_info += _("ADVERTENCIA: Complemento incompatible con este NVDA.\n")

		ficha = _("RESUMEN DEL COMPLEMENTO\n")
		ficha += "========================================\n"
		ficha += _("Nombre: {}\n").format(datos['summary'])
		ficha += _("ID (Nombre interno): {}\n").format(datos['name'])
		ficha += _("Autor: {}\n").format(datos['author'])
		ficha += _("Página web: {}\n").format(datos['url'])
		ficha += _("Desarrollo: {}\n").format(_("Con soporte") if datos['legacy'] == 0 else _("Sin soporte"))
		ficha += local_info
		ficha += "\n" + _("DESCRIPCIÓN:") + "\n"
		ficha += "----------------------------------------\n"
		ficha += (datos['description'] or _("Sin descripción disponible.")) + "\n"
		ficha += "\n" + _("CANALES DE DESCARGA:") + "\n"
		ficha += "----------------------------------------\n"
		self.txtResultado.SetValue(ficha)
		for link in datos['links']:
			fichaEnlaces = _("Canal: {}\nVersión: {}\nMínimo NVDA: {}\nÚltima prueba: {}\nDescargas: {}\n").format(
				link['channel'], link['version'], link['minimum'], link['lasttested'], link['downloads']
			)
			self.txtResultado.AppendText(fichaEnlaces + "---\n")
		self.txtResultado.SetInsertionPoint(0)

	def onFichaTrans(self):
		if not ajustes.tempTrans:
			ui.message(_("Active la traducción en opciones de la tienda."))
			return
		nombre = self._getCleanName()
		if not nombre:
			return
		indice = self.datos.indiceName(nombre)
		if indice is None:
			return
		datos = self.datos.dataServidor[indice]
		target_lang = ajustes.langDict.get(ajustes.tempLang)
		from .cache_manager import CacheManager
		cache = CacheManager(ajustes.dirDatos, ajustes.tiempoDict, lambda: ajustes.tempCacheInterval, lambda: ajustes.tempServerCache, lambda: ajustes.tempUseTranslationCache)
		traduccion = cache.getTranslation(datos['description'], target_lang)
		if not traduccion:
			beep(400, 150)
			try:
				from . import traductor
				traduccion = traductor.translate(datos['description'], target_lang)
				cache.saveTranslation(datos['description'], traduccion, target_lang)
			except:
				traduccion = datos['description']
				ui.message(_("No se pudo traducir"))

		installed = AddonManager.getInstalledAddonsDict()
		local_info = ""
		if datos['name'].lower() in installed:
			addon = installed[datos['name'].lower()]
			estado = _("Activo")
			if addon.get('isBlocked', False):
				estado = _("Deshabilitado (incompatible)")
			elif addon['isDisabled']:
				estado = _("Deshabilitado")
			local_info = _("\n--- INFORMACIÓN DE INSTALACIÓN LOCAL ---\n")
			local_info += _("Estado: {}\n").format(estado)
			local_info += _("Versión: {}\n").format(addon['version'])

		ficha = _("RESUMEN (TRADUCIDO)\n")
		ficha += "========================================\n"
		ficha += _("Nombre: {}\n").format(datos['summary'])
		ficha += _("ID: {}\n").format(datos['name'])
		ficha += _("Autor: {}\n").format(datos['author'])
		ficha += local_info
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
		# Submenú Filtros
		filtroMenu = wx.Menu()
		filtroMenu.Append(ID_FILTRO_TODOS, _("Mostrar todos"))
		filtroMenu.Append(ID_FILTRO_2026, _("API 2026"))
		filtroMenu.Append(ID_FILTRO_2025, _("API 2025"))
		filtroMenu.Append(ID_FILTRO_2024, _("API 2024"))
		filtroMenu.Append(ID_FILTRO_2023, _("API 2023"))
		filtroMenu.Append(ID_FILTRO_AUTOR, _("Por autor"))
		filtroMenu.Append(ID_FILTRO_DOWNLOADS, _("Por descargas"))
		menu.AppendSubMenu(filtroMenu, _("&Filtros"))
		for item in filtroMenu.GetMenuItems():
			self.Bind(wx.EVT_MENU, self.onCargaFiltro, item)

		sel = self.listboxComplementos.GetSelection()
		if sel != -1:
			nombre = self._getCleanName()
			if nombre:
				indice = self.datos.indiceName(nombre)
				if indice is not None:
					datos = self.datos.dataServidor[indice]
					# Submenú Copiar
					copiarMenu = wx.Menu()
					copiarMenu.Append(ID_MENU_COPIAR_INFO, _("Copiar información"))
					copiarMenu.Append(ID_MENU_COPIAR_URL, _("Copiar URL página"))
					# Copiar enlace interno NVDA.ES
					it_es = copiarMenu.Append(ID_MENU_COPIAR_ENLACE_ES, _("Copiar enlace interno NVDA.ES"))
					self.Bind(wx.EVT_MENU, lambda e, n=datos['links'][0]['file']: copiar_al_portapapeles(construir_url_descarga_es(n)), it_es)
					# Copiar enlace de descarga
					if len(datos['links']) > 1:
						descargasSubMenu = wx.Menu()
						for link in datos['links']:
							item_link = descargasSubMenu.Append(wx.ID_ANY, _("Canal {}").format(link['channel']))
							self.Bind(wx.EVT_MENU, lambda e, url=link['link']: copiar_al_portapapeles(url), item_link)
						copiarMenu.AppendSubMenu(descargasSubMenu, _("Copiar enlace de descarga"))
					else:
						copiarMenu.Append(ID_MENU_COPIAR_DOWNLOAD, _("Copiar enlace de descarga"))
						self.Bind(wx.EVT_MENU, lambda e: copiar_al_portapapeles(datos['links'][0]['link']), id=ID_MENU_COPIAR_DOWNLOAD)
					menu.AppendSeparator()
					menu.AppendSubMenu(copiarMenu, _("&Copiar"))
					self.Bind(wx.EVT_MENU, lambda e: copiar_al_portapapeles(self.txtResultado.GetValue()), id=ID_MENU_COPIAR_INFO)
					self.Bind(wx.EVT_MENU, lambda e: copiar_al_portapapeles(datos['url']), id=ID_MENU_COPIAR_URL)

					# Gestión instalado (con empaquetador y documentación)
					installed = AddonManager.getInstalledAddonsDict()
					gestionMenu = construir_menu_gestion(self, datos['name'], installed)
					if gestionMenu:
						menu.AppendSubMenu(gestionMenu, _("&Gestión instalado"))

		if event and event.GetEventObject() == self.accionBtn:
			self.PopupMenu(menu, self.accionBtn.GetPosition())
		else:
			self.PopupMenu(menu)

	def onInstalarDirecto(self, event):
		sel = self.listboxComplementos.GetSelection()
		if sel == -1:
			return
		name = self._getCleanName()
		if not name:
			return
		idx = self.datos.indiceName(name)
		if idx is None:
			return
		addon = self.datos.dataServidor[idx]
		minNVDA = addon['links'][0].get('minimum')
		lastTested = addon['links'][0].get('lasttested')
		if minNVDA and lastTested:
			try:
				if not version_utils.isAddonCompatible(
					version_utils.getAPIVersionTupleFromString(minNVDA),
					version_utils.getAPIVersionTupleFromString(lastTested)
				):
					if not ajustes.tempAllowIncompatible:
						gui.messageBox(_("Este complemento no es compatible con su versión de NVDA."), _("Incompatible"), wx.ICON_ERROR)
						return
					else:
						if gui.messageBox(_("Este complemento no es compatible. ¿Desea intentar instalarlo de todos modos?"), _("Advertencia"), wx.YES_NO | wx.ICON_WARNING) == wx.NO:
							return
			except:
				pass
		url = self.datos.urlBase + addon['links'][0]['file']
		path_temp = os.path.join(ajustes.dirDatos, "temp_install.nvda-addon")
		isSilent = ajustes.tempSilentInstall
		from .dialogos_actualizaciones import DescargaDialogo
		dlg = DescargaDialogo(self, _("Preparando instalación de %s...") % addon['summary'], url, path_temp, 15, isInstaller=True)
		if dlg.ShowModal() == ajustes.ID_TRUE:
			if AddonManager.installAddon(path_temp, silent=isSilent):
				if isSilent:
					ui.message(_("Instalación de %s completada.") % addon['summary'])
					if gui.messageBox(_("Instalación completada. ¿Desea reiniciar NVDA ahora?"), _("Reiniciar"), wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
						core.restart()
			wx.CallLater(5000, lambda: self._borrarTemp(path_temp))
		dlg.Destroy()

	def _borrarTemp(self, path):
		try:
			if os.path.exists(path):
				os.remove(path)
		except:
			pass

	def onDescargar(self, event):
		if self.listboxComplementos.GetSelection() == -1:
			return
		nombre = self._getCleanName()
		if not nombre:
			return
		indice = self.datos.indiceName(nombre)
		if indice is None:
			return
		datos = self.datos.dataServidor[indice]
		if len(datos['links']) == 1:
			self._iniciarDescarga(0)
		else:
			menu = wx.Menu()
			for i, link in enumerate(datos['links']):
				item = menu.Append(i, _("Canal {}").format(link['channel']))
				self.Bind(wx.EVT_MENU, lambda e, idx=i: self._iniciarDescarga(idx), item)
			self.PopupMenu(menu, self.descargarBtn.GetPosition())

	def _iniciarDescarga(self, canalIdx):
		if ajustes.IS_Download:
			ui.message(_("Ya hay una descarga en progreso"))
			return
		nombre = self._getCleanName()
		if not nombre:
			return
		indice = self.datos.indiceName(nombre)
		if indice is None:
			return
		datos = self.datos.dataServidor[indice]
		url = self.datos.urlBase + datos['links'][canalIdx]['file']
		nombreFile = self.datos.GetFilenameDownload(datos['links'][canalIdx]['file'])
		if not nombreFile or nombreFile == "downloads":
			wx.LaunchDefaultBrowser(datos['links'][canalIdx]['link'])
			return
		wildcard = _("Complemento de NVDA (*.nvda-addon)|*.nvda-addon")
		dlg = wx.FileDialog(self, message=_("Guardar en..."), defaultDir=os.environ.get('USERPROFILE', ''), defaultFile=nombreFile, wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			dlg.Destroy()
			ajustes.IS_Download = True
			self.TrueDescarga(os.path.basename(path), url, path)
		else:
			dlg.Destroy()
			self.FalseDescarga()

	def TrueDescarga(self, fichero_final, url, path):
		from .dialogos_actualizaciones import DescargaDialogo
		dlg = DescargaDialogo(self, _("Descargando %s...") % fichero_final, url, path, 15)
		result = dlg.ShowModal()
		if result == ajustes.ID_TRUE:
			if ajustes.tempInstall:
				addonGui.handleRemoteAddonInstall(path)
		ajustes.IS_Download = False
		dlg.Destroy()

	def FalseDescarga(self):
		ajustes.IS_Download = False

	def onWeb(self, event):
		if self.listboxComplementos.GetSelection() == -1:
			return
		nombre = self._getCleanName()
		if not nombre:
			return
		indice = self.datos.indiceName(nombre)
		if indice is not None:
			wx.LaunchDefaultBrowser(self.datos.dataServidor[indice]['url'])

	def onCambiarServidor(self, event):
		menu = wx.Menu()
		for i, srv in enumerate(ajustes.listaServidores):
			item = menu.Append(i, srv[0], "", wx.ITEM_CHECK)
			if i == ajustes.selectSRV:
				menu.Check(i, True)
		menu.Bind(wx.EVT_MENU_RANGE, self._cambiarSrv, id=0, id2=len(ajustes.listaServidores) - 1)
		self.PopupMenu(menu, self.servidorBtn.GetPosition())

	def _cambiarSrv(self, event):
		ajustes.selectSRV = event.GetId()
		ajustes.urlServidor = ajustes.listaServidores[ajustes.selectSRV][1]
		ajustes.setConfig("urlServidor", ajustes.urlServidor)
		ajustes.setConfig("selectSRV", ajustes.selectSRV)
		ajustes.listaAddonsSave = basedatos.libreriaLocal(ajustes.listaServidores[ajustes.selectSRV][2]).fileJsonAddon(2)
		ajustes.IS_WinON = False
		self.Destroy()
		gui.mainFrame.postPopup()
		from .hilos import HiloComplemento
		HiloComplemento(1, "nvda_es").start()

	def onSalir(self, event):
		if not ajustes.IS_Download:
			ajustes.IS_WinON = False
		ajustes.focoActual = "listboxComplementos"
		preguntar_reinicio(self.snapshotInicial)
		self.Destroy()
		gui.mainFrame.postPopup()

	def onKeyPress(self, event):
		keyCode = event.GetKeyCode()
		if keyCode == wx.WXK_ESCAPE:
			self.onSalir(None)
		elif keyCode == wx.WXK_F3:
			self.onFichaTrans()
		else:
			event.Skip()
