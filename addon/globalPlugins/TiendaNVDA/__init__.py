# -*- coding: utf-8 -*-
# Copyright (C) 2021-2025 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.
#
# TiendaNVDA_Modern - Tienda Unificada de Complementos para NVDA
# Integra la tienda de NVDA.ES y la tienda oficial de NVDA
#

import globalPluginHandler
import addonHandler
import gui
import globalVars
import ui
import config
import core
from scriptHandler import script
from logHandler import log
from gui.settingsDialogs import NVDASettingsDialog, SettingsPanel
from gui import guiHelper
import wx
import wx.adv
from threading import Thread
import os
import sys
import traceback
import json
from enum import Enum

from . import ajustes
from . import basedatos
from . import tienda_oficial
from .actualizadorRecursos import ActualizadorRecursos

addonHandler.initTranslation()

# Variables globales
inicio = None
chkUpdate = None


class StoreSource(Enum):
	NVDA_ES = "nvda_es"
	OFFICIAL = "official"
	ALL = "all"


def function_ChkUpdate():
	"""Función para controlar el hilo que busca actualizaciones"""
	if ajustes.reiniciarTrue:
		msg = _("Necesita reiniciar NVDA para aplicar las actualizaciones.")
		notify = wx.adv.NotificationMessage(title=_("Información"), message=msg, parent=None, flags=wx.ICON_INFORMATION)
		notify.Show(timeout=10)
		return

	try:
		datos = basedatos.NVDAStoreClient()
		nombreUrl, verInstalada, verInstalar = datos.chkActualizaS(includeIncompatible=ajustes.tempAllowIncompatible)
		actualizaciones_oficiales = []
		if ajustes.tempChkOfficial:
			try:
				actualizaciones_oficiales = tienda_oficial.buscar_actualizaciones_oficiales()
			except Exception as e:
				log.debug(f"Error al buscar actualizaciones oficiales: {e}")

		es_updates = list(nombreUrl.keys()) if nombreUrl else []
		oficial_updates = [a[0].displayName for a in actualizaciones_oficiales]
		total_updates = len(es_updates) + len(oficial_updates)

		if total_updates == 0:
			if ajustes.contadorRepeticionSn <= 9:
				ajustes.contadorRepeticionSn += 1
			else:
				chkUpdate.stop()
		else:
			if ajustes.contadorRepeticion <= 4:
				ajustes.contadorRepeticion += 1
				msg = _("Se encontraron {} actualizaciones.").format(total_updates) if total_updates > 1 else _("Se encontró una actualización.")
				detalles = ""
				if es_updates:
					detalles += _("\n- NVDA.ES ({}): {}").format(len(es_updates), ", ".join(es_updates))
				if oficial_updates:
					detalles += _("\n- Tienda Oficial ({}): {}").format(len(oficial_updates), ", ".join(oficial_updates))
				msg += detalles + _("\n\nEjecute Buscar actualizaciones de complementos.")
				notify = wx.adv.NotificationMessage(title=_("Tienda NVDA: Actualizaciones"), message=msg, parent=None, flags=wx.ICON_INFORMATION)
				notify.Show(timeout=15)
			else:
				chkUpdate.stop()
	except Exception as e:
		log.debug(f"Error al comprobar actualizaciones automáticas: {e}")
		chkUpdate.stop()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		if hasattr(globalVars, "tienda_moderna"):
			self.postStartupHandler()
		core.postNvdaStartup.register(self.postStartupHandler)
		globalVars.tienda_moderna = None
	
		# Actualizador de traducciones y documentación desde GitHub
		self._actualizadorRecursos = ActualizadorRecursos(
			"hxebolax",
			"Tienda-para-NVDA",
			modo_comprobacion="inicio",
			intervalo_horas=24,
			actualizar_idiomas=True,
			actualizar_documentacion=True,
			notificar_usuario=True,
			notificar_sin_cambios=False,
			menuHerramientas=True,
		)

	def postStartupHandler(self):
		Thread(target=self.tareasDeRed, daemon=True).start()

	def tareasDeRed(self):
		global inicio
		try:
			ajustes.setup()
			inicio = True
		except Exception as e:
			log.info(_("No se pudieron cargar las librerías necesarias para la Tienda"))
			log.info(f"Error: {e}")
			traceback.print_exc()
			inicio = False

		if inicio:
			global chkUpdate
			if ajustes.tempChk:
				chkUpdate = basedatos.RepeatTimer(ajustes.tiempoDict.get(ajustes.tempTimer), function_ChkUpdate)
			NVDASettingsDialog.categoryClasses.append(TiendaPanel)

			self.menu = wx.Menu()
			self.tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu

			# Submenú Tienda NVDA.ES
			self.menuNVDAES = wx.Menu()
			self.tiendaComplementosES = self.menuNVDAES.Append(wx.ID_ANY, _("Listado de complementos NVDA.ES"))
			gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_menu1, self.tiendaComplementosES)
			self.tiendaActualizacionesES = self.menuNVDAES.Append(wx.ID_ANY, _("Buscar actualizaciones NVDA.ES"))
			gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_menu2, self.tiendaActualizacionesES)
			self.menu.AppendSubMenu(self.menuNVDAES, _("Tienda NVDA.ES"))

			# Submenú Tienda Oficial NVDA
			self.menuOficial = wx.Menu()
			self.tiendaComplementosOficial = self.menuOficial.Append(wx.ID_ANY, _("Listado de complementos oficiales"))
			gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_menu_oficial1, self.tiendaComplementosOficial)
			self.tiendaActualizacionesOficial = self.menuOficial.Append(wx.ID_ANY, _("Buscar actualizaciones oficiales"))
			gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_menu_oficial2, self.tiendaActualizacionesOficial)
			self.menu.AppendSubMenu(self.menuOficial, _("Tienda Oficial NVDA"))

			# Opción unificada
			self.menu.AppendSeparator()
			self.tiendaUnificada = self.menu.Append(wx.ID_ANY, _("Tienda Unificada (Todas las fuentes)"))
			gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_menu_unificada, self.tiendaUnificada)

			# Empaquetador de complementos
			self.menu.AppendSeparator()
			self.tiendaEmpaquetador = self.menu.Append(wx.ID_ANY, _("Empaquetador de complementos"))
			gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_menu_empaquetar, self.tiendaEmpaquetador)

			# Documentación
			self.tiendaDocumentacion = self.menu.Append(wx.ID_ANY, _("Documentación del complemento"))
			gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_menu3, self.tiendaDocumentacion)

			self.tiendaMenu = self.tools_menu.AppendSubMenu(self.menu, _("Tienda de Complementos NVDA"))
		else:
			log.debug(_("Inicio del complemento cancelado."))

	def terminate(self):
		global chkUpdate
		# Detener el actualizador de recursos
		if hasattr(self, '_actualizadorRecursos'):
			self._actualizadorRecursos.detener()
		try:
			self.tools_menu.Remove(self.tiendaMenu)
		except:
			pass
		try:
			if inicio:
				if chkUpdate:
					chkUpdate.stop()
				if ajustes.tempAutoBackupOnExit:
					try:
						from .addon_manager import AddonManager
						AddonManager.createBackup()
					except Exception as e:
						log.error(f"Error al crear backup automático: {e}")
				try:
					for f in os.listdir(ajustes.dirDatos):
						if f.endswith(".nvda-addon") and f.startswith("temp_install"):
							try:
								os.remove(os.path.join(ajustes.dirDatos, f))
							except:
								pass
				except:
					pass
				NVDASettingsDialog.categoryClasses.remove(TiendaPanel)
				core.postNvdaStartup.unregister(self.postStartupHandler)
			if hasattr(self, '_MainWindows') and self._MainWindows:
				self._MainWindows.Destroy()
		except (AttributeError, RuntimeError):
			pass
		super().terminate()

	def _lanzar_hilo(self, opcion, fuente):
		from .hilos import HiloComplemento
		if inicio:
			if not ajustes.IS_WinON:
				self._MainWindows = HiloComplemento(opcion, fuente)
				self._MainWindows.start()
			else:
				ui.message(_("Ya hay una instancia de la Tienda NVDA abierta."))
		else:
			self._mostrar_error_inicio()

	@script(gesture=None, description=_("Muestra la ventana con todos los complementos de NVDA.ES"), category=_("Tienda de Complementos NVDA"))
	def script_menu1(self, event):
		self._lanzar_hilo(1, StoreSource.NVDA_ES)

	@script(gesture=None, description=_("Busca actualizaciones de los complementos instalados en NVDA.ES"), category=_("Tienda de Complementos NVDA"))
	def script_menu2(self, event):
		self._lanzar_hilo(2, StoreSource.NVDA_ES)

	@script(gesture=None, description=_("Muestra la ventana con todos los complementos de la tienda oficial"), category=_("Tienda de Complementos NVDA"))
	def script_menu_oficial1(self, event):
		self._lanzar_hilo(1, StoreSource.OFFICIAL)

	@script(gesture=None, description=_("Busca actualizaciones de los complementos oficiales"), category=_("Tienda de Complementos NVDA"))
	def script_menu_oficial2(self, event):
		self._lanzar_hilo(2, StoreSource.OFFICIAL)

	@script(gesture=None, description=_("Muestra la tienda unificada con todas las fuentes de complementos"), category=_("Tienda de Complementos NVDA"))
	def script_menu_unificada(self, event):
		self._lanzar_hilo(1, StoreSource.ALL)

	def script_menu_empaquetar(self, event):
		"""Abre un diálogo para empaquetar complementos instalados"""
		if not inicio:
			self._mostrar_error_inicio()
			return
		import addonHandler as ah
		from .empaquetador import empaquetar_complemento_individual
		addons = list(ah.getAvailableAddons())
		if not addons:
			ui.message(_("No hay complementos instalados."))
			return
		choices = [f"{a.manifest['summary']} ({a.manifest['version']})" for a in addons]
		dlg = wx.SingleChoiceDialog(gui.mainFrame, _("Seleccione un complemento para empaquetar:"), _("Empaquetador de complementos"), choices)
		if dlg.ShowModal() == wx.ID_OK:
			sel = dlg.GetSelection()
			dlg.Destroy()
			dirDlg = wx.DirDialog(gui.mainFrame, _("Seleccione un directorio para guardar:"), style=wx.DD_DEFAULT_STYLE)
			if dirDlg.ShowModal() == wx.ID_OK:
				directorio = dirDlg.GetPath()
				dirDlg.Destroy()
				empaquetar_complemento_individual(addons[sel], directorio)
			else:
				dirDlg.Destroy()
		else:
			dlg.Destroy()

	def script_menu3(self, event):
		wx.LaunchDefaultBrowser(addonHandler.Addon(os.path.join(os.path.dirname(__file__), "..", "..")).getDocFilePath())

	def _mostrar_error_inicio(self):
		ui.message(_("El complemento falló al iniciar NVDA.\nReinice NVDA para intentar solucionar el problema."))


if globalVars.appArgs.secure:
	GlobalPlugin = globalPluginHandler.GlobalPlugin


class TiendaPanel(SettingsPanel):
	# Translators: title for the addon store settings category
	title = _("Tienda de Complementos NVDA")

	def makeSettings(self, sizer):
		helper = guiHelper.BoxSizerHelper(self, sizer=sizer)

		# Sección NVDA.ES
		groupNVDAES = guiHelper.BoxSizerHelper(
			self,
			sizer=wx.StaticBoxSizer(
				wx.StaticBox(self, label=_("Tienda NVDA.ES")),
				wx.VERTICAL
			)
		)

		self.choiceSRV = groupNVDAES.addLabeledControl(
			_("Seleccione un servidor de complementos"),
			wx.Choice,
			choices=[ajustes.listaServidores[i][0] for i in range(len(ajustes.listaServidores))]
		)
		self.choiceSRV.Selection = ajustes.selectSRV
		self.choiceSRV.Bind(wx.EVT_CHOICE, self.onChoiceSRV)

		self.gestionaBTN = groupNVDAES.addItem(
			wx.Button(self, label=_("&Gestionar Servidores de complementos"))
		)
		self.gestionaBTN.Bind(wx.EVT_BUTTON, self.onGestiona)

		helper.addItem(groupNVDAES)

		# Sección Tienda Oficial
		groupOficial = guiHelper.BoxSizerHelper(
			self,
			sizer=wx.StaticBoxSizer(
				wx.StaticBox(self, label=_("Tienda Oficial NVDA")),
				wx.VERTICAL
			)
		)

		self.oficialChk = groupOficial.addItem(
			wx.CheckBox(self, label=_("Habilitar tienda oficial de NVDA"))
		)
		self.oficialChk.Value = ajustes.tempOficial

		self.allowIncompatibleChk = groupOficial.addItem(
			wx.CheckBox(self, label=_("Permitir complementos incompatibles de la tienda oficial"))
		)
		self.allowIncompatibleChk.Value = ajustes.tempAllowIncompatible

		helper.addItem(groupOficial)

		# Sección Actualizaciones
		groupUpdates = guiHelper.BoxSizerHelper(
			self,
			sizer=wx.StaticBoxSizer(
				wx.StaticBox(self, label=_("Actualizaciones")),
				wx.VERTICAL
			)
		)

		self.autoChk = groupUpdates.addItem(
			wx.CheckBox(self, label=_("Activar comprobación automática de actualizaciones"))
		)
		self.autoChk.Bind(wx.EVT_CHECKBOX, self.onAutoChk)
		self.autoChk.Value = ajustes.tempChk

		self.timerPanel = wx.Panel(self)
		timerSizer = wx.BoxSizer(wx.HORIZONTAL)
		timerLabel = wx.StaticText(self.timerPanel, label=_("Tiempo para comprobar actualizaciones:"))
		self.choiceTimer = wx.Choice(self.timerPanel, choices=ajustes.tiempoChk)
		self.choiceTimer.Selection = ajustes.tempTimer
		timerSizer.Add(timerLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		timerSizer.Add(self.choiceTimer, 1, wx.EXPAND)
		self.timerPanel.SetSizer(timerSizer)
		groupUpdates.addItem(self.timerPanel)

		if not self.autoChk.Value:
			self.timerPanel.Hide()

		self.chkOfficialUpdates = groupUpdates.addItem(
			wx.CheckBox(self, label=_("Incluir actualizaciones de la tienda oficial"))
		)
		self.chkOfficialUpdates.Value = ajustes.tempChkOfficial

		helper.addItem(groupUpdates)

		# Sección Traducción
		groupTrans = guiHelper.BoxSizerHelper(
			self,
			sizer=wx.StaticBoxSizer(
				wx.StaticBox(self, label=_("Traducción")),
				wx.VERTICAL
			)
		)

		self.autoLang = groupTrans.addItem(
			wx.CheckBox(self, label=_("Activar traductor para descripciones"))
		)
		self.autoLang.Bind(wx.EVT_CHECKBOX, self.onAutoLang)
		self.autoLang.Value = ajustes.tempTrans

		self.langPanel = wx.Panel(self)
		langSizer = wx.BoxSizer(wx.HORIZONTAL)
		langLabel = wx.StaticText(self.langPanel, label=_("Idioma para traducir descripciones:"))
		self.choiceLang = wx.Choice(self.langPanel, choices=ajustes.langLST)
		self.choiceLang.Selection = ajustes.tempLang
		langSizer.Add(langLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		langSizer.Add(self.choiceLang, 1, wx.EXPAND)
		self.langPanel.SetSizer(langSizer)
		groupTrans.addItem(self.langPanel)

		if not self.autoLang.Value:
			self.langPanel.Hide()

		helper.addItem(groupTrans)

		# Sección Opciones Generales
		groupGeneral = guiHelper.BoxSizerHelper(
			self,
			sizer=wx.StaticBoxSizer(
				wx.StaticBox(self, label=_("Opciones Generales")),
				wx.VERTICAL
			)
		)

		self.ordenChk = groupGeneral.addItem(
			wx.CheckBox(self, label=_("Ordenar complementos alfabéticamente"))
		)
		self.ordenChk.Value = ajustes.tempOrden

		self.installChk = groupGeneral.addItem(
			wx.CheckBox(self, label=_("Instalar complementos después de descargar"))
		)
		self.installChk.Value = ajustes.tempInstall

		self.silentInstallChk = groupGeneral.addItem(
			wx.CheckBox(self, label=_("Instalar en silencio (pide reiniciar al finalizar)"))
		)
		self.silentInstallChk.Value = ajustes.tempSilentInstall

		self.serverCacheChk = groupGeneral.addItem(
			wx.CheckBox(self, label=_("Habilitar caché de servidores (Mejora la velocidad de carga)"))
		)
		self.serverCacheChk.Value = ajustes.tempServerCache
		self.serverCacheChk.Bind(wx.EVT_CHECKBOX, self.onServerCacheChk)

		self.cacheIntervalPanel = wx.Panel(self)
		cacheIntervalSizer = wx.BoxSizer(wx.HORIZONTAL)
		cacheIntervalLabel = wx.StaticText(self.cacheIntervalPanel, label=_("Actualizar caché cada:"))
		self.choiceCacheInterval = wx.Choice(self.cacheIntervalPanel, choices=ajustes.tiempoChk)
		self.choiceCacheInterval.Selection = ajustes.tempCacheInterval
		cacheIntervalSizer.Add(cacheIntervalLabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		cacheIntervalSizer.Add(self.choiceCacheInterval, 1, wx.EXPAND)
		self.cacheIntervalPanel.SetSizer(cacheIntervalSizer)
		groupGeneral.addItem(self.cacheIntervalPanel)

		if not self.serverCacheChk.Value:
			self.cacheIntervalPanel.Hide()

		self.useCacheChk = groupGeneral.addItem(
			wx.CheckBox(self, label=_("Usar caché para traducciones (Mejora el rendimiento)"))
		)
		self.useCacheChk.Value = ajustes.tempUseTranslationCache

		self.listCacheChk = groupGeneral.addItem(
			wx.CheckBox(self, label=_("Habilitar modo offline (Caché de listas de la tienda)"))
		)
		self.listCacheChk.Value = ajustes.tempListCacheEnabled

		btnBackupSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.backupBtn = wx.Button(self, label=_("&Crear Backup de complementos"))
		self.restoreBtn = wx.Button(self, label=_("&Restaurar desde Backup"))
		btnBackupSizer.Add(self.backupBtn, 1, wx.ALL, 5)
		btnBackupSizer.Add(self.restoreBtn, 1, wx.ALL, 5)
		groupGeneral.addItem(btnBackupSizer)

		self.backupBtn.Bind(wx.EVT_BUTTON, self.onBackup)
		self.restoreBtn.Bind(wx.EVT_BUTTON, self.onRestore)

		helper.addItem(groupGeneral)

		# Lista de complementos instalados
		self.datos = basedatos.NVDAStoreClient()
		self.datosServidor = self.datos.dataServidor
		self.listbox = helper.addLabeledControl(
			_("Complementos instalados que hay en el servidor:"),
			wx.ListBox
		)
		self._cargarListaComplementos()

		self.listbox.Bind(wx.EVT_KEY_UP, self.onListBox)

		self.listaOriginal = basedatos.libreriaLocal(
			ajustes.listaServidores[ajustes.selectSRV][2]
		).fileJsonAddon(2)
		self.listaGuarda = []

	def _cargarListaComplementos(self):
		self.listbox.Clear()
		if self.datosServidor is None:
			self.listbox.Append(_("No se pudo tener acceso al servidor"))
			return

		if len(ajustes.listaAddonsSave) == 0:
			self.listbox.Append(_("Sin complementos compatibles"))
			return

		for i in ajustes.listaAddonsSave:
			for x in range(len(self.datosServidor)):
				if self.datosServidor[x]['name'].lower() == i[0].lower():
					if i[1] == 9:
						self.listbox.Append(
							"{} -- {}".format(
								self.datosServidor[x]['summary'],
								_("Descartar actualizaciones")
							)
						)
					else:
						self.listbox.Append(
							"{} -- {}".format(
								self.datosServidor[x]['summary'],
								self.datosServidor[x]['links'][i[1]]['channel']
							)
						)

		if self.listbox.GetCount() > 0:
			self.listbox.SetSelection(0)

	def onSave(self):
		global chkUpdate
		ajustes.setConfig("urlServidor", ajustes.listaServidores[self.choiceSRV.Selection][1])
		ajustes.setConfig("selectSRV", self.choiceSRV.Selection)
		ajustes.setConfig("autoChk", self.autoChk.Value)
		ajustes.setConfig("timerChk", self.choiceTimer.Selection)
		ajustes.setConfig("autoLang", self.autoLang.Value)
		ajustes.setConfig("langTrans", self.choiceLang.Selection)
		ajustes.setConfig("ordenChk", self.ordenChk.Value)
		ajustes.setConfig("installChk", self.installChk.Value)
		ajustes.setConfig("oficialChk", self.oficialChk.Value)
		ajustes.setConfig("allowIncompatibleChk", self.allowIncompatibleChk.Value)
		ajustes.setConfig("chkOfficialUpdates", self.chkOfficialUpdates.Value)
		ajustes.setConfig("useTranslationCache", self.useCacheChk.Value)
		ajustes.setConfig("listCacheEnabled", self.listCacheChk.Value)
		ajustes.setConfig("silentInstall", self.silentInstallChk.Value)
		ajustes.setConfig("serverCache", self.serverCacheChk.Value)
		ajustes.setConfig("cacheInterval", self.choiceCacheInterval.Selection)

		ajustes.tempChk = self.autoChk.Value
		ajustes.tempTimer = self.choiceTimer.Selection
		ajustes.tempTrans = self.autoLang.Value
		ajustes.tempLang = self.choiceLang.Selection
		ajustes.tempOrden = self.ordenChk.Value
		ajustes.tempInstall = self.installChk.Value
		ajustes.tempOficial = self.oficialChk.Value
		ajustes.tempAllowIncompatible = self.allowIncompatibleChk.Value
		ajustes.tempChkOfficial = self.chkOfficialUpdates.Value
		ajustes.tempUseTranslationCache = self.useCacheChk.Value
		ajustes.tempListCacheEnabled = self.listCacheChk.Value
		ajustes.tempSilentInstall = self.silentInstallChk.Value
		ajustes.tempServerCache = self.serverCacheChk.Value
		ajustes.tempCacheInterval = self.choiceCacheInterval.Selection

		if ajustes.tempChk:
			try:
				if chkUpdate:
					chkUpdate.stop()
				ajustes.contadorRepeticion = 0
				ajustes.contadorRepeticionSn = 0
			except:
				pass
			chkUpdate = basedatos.RepeatTimer(
				ajustes.tiempoDict.get(ajustes.tempTimer),
				function_ChkUpdate
			)
			chkUpdate.start()

		if len(self.listaGuarda) > 0:
			for i in range(len(self.listaGuarda)):
				ajustes.listaAddonsSave[self.listaGuarda[i][0]][1] = self.listaGuarda[i][1]
			basedatos.libreriaLocal(
				ajustes.listaServidores[ajustes.selectSRV][2]
			).fileJsonAddon(1, basedatos.libreriaLocal().ordenaLista(ajustes.listaAddonsSave))

	def onPanelActivated(self):
		self.originalProfileName = config.conf.profiles[-1].name
		config.conf.profiles[-1].name = None
		self.Show()

	def onPanelDeactivated(self):
		config.conf.profiles[-1].name = self.originalProfileName
		self.Hide()

	def onChoiceSRV(self, event):
		try:
			ajustes.urlServidor = ajustes.listaServidores[self.choiceSRV.Selection][1]
			ajustes.selectSRV = self.choiceSRV.Selection
		except:
			ajustes.urlServidor = ajustes.listaServidores[0][1]
			ajustes.selectSRV = 0

		self.datos = basedatos.NVDAStoreClient()
		self.datosServidor = self.datos.dataServidor

		if self.datosServidor is None:
			self.listbox.Clear()
			self.listbox.Append(_("No se pudo tener acceso al servidor"))
			self.listbox.SetSelection(0)
		else:
			self.listaOriginal = basedatos.libreriaLocal(
				ajustes.listaServidores[ajustes.selectSRV][2]
			).fileJsonAddon(2)
			self.listaGuarda = []
			ajustes.listaAddonsSave = basedatos.libreriaLocal(
				ajustes.listaServidores[ajustes.selectSRV][2]
			).fileJsonAddon(2)
			self._cargarListaComplementos()

	def onAutoChk(self, event):
		chk = event.GetEventObject()
		if chk.GetValue():
			self.timerPanel.Show()
		else:
			self.timerPanel.Hide()
		self.Layout()
		self.Fit()

	def onAutoLang(self, event):
		chk = event.GetEventObject()
		if chk.GetValue():
			self.langPanel.Show()
		else:
			self.langPanel.Hide()
		self.Layout()
		self.Fit()

	def onServerCacheChk(self, event):
		chk = event.GetEventObject()
		if chk.GetValue():
			self.cacheIntervalPanel.Show()
		else:
			self.cacheIntervalPanel.Hide()
		self.Layout()
		self.Fit()

	def onListBox(self, event):
		if self.listbox.GetSelection() == -1:
			return

		selStr = self.listbox.GetString(self.listbox.GetSelection())
		if selStr == _("Sin complementos compatibles"):
			return
		if selStr == _("No se pudo tener acceso al servidor"):
			return

		if event.GetKeyCode() == 32:  # Espacio
			nombre = selStr.split(" -- ")
			nombreLocal = ajustes.listaAddonsSave[self.listbox.GetSelection()][0]
			indice = self.datos.indiceName(nombreLocal)
			datos = self.datosServidor[indice]

			self.menuDescarga = wx.Menu()
			for i in range(len(datos['links'])):
				item = self.menuDescarga.Append(i, _("Canal {}").format(datos['links'][i]['channel']))
				self.Bind(wx.EVT_MENU, self.onSelect, item)
			item = self.menuDescarga.Append(9, _("Descartar actualizaciones"))
			self.Bind(wx.EVT_MENU, self.onSelect, item)

			position = self.listbox.GetPosition()
			self.PopupMenu(self.menuDescarga, position)

	def modificaListBox(self, canalID):
		nombre = self.listbox.GetString(self.listbox.GetSelection()).split(" -- ")
		nombreLocal = ajustes.listaAddonsSave[self.listbox.GetSelection()][0]
		indice = self.datos.indiceName(nombreLocal)
		datos = self.datosServidor[indice]

		if canalID == 9:
			nombreCanal = _("Descartar actualizaciones")
		else:
			nombreCanal = datos['links'][canalID]['channel']

		nombreCompuesto = nombre[0] + " -- " + nombreCanal
		pos = self.listbox.GetSelection()
		self.listbox.Delete(pos)
		self.listbox.Insert(nombreCompuesto, pos)
		self.listbox.SetSelection(pos)
		self.listaGuarda.append([pos, canalID])

	def onSelect(self, event):
		self.modificaListBox(event.GetId())

	def onGestiona(self, event):
		from .dialogos_servidores import GestorServidores
		if ajustes.IS_WinON:
			msg = _("""Ya hay una instancia de la Tienda NVDA abierta.

Para gestionar los servidores es necesario que la Tienda este cerrada.""")
			ui.message(msg)
		else:
			dlg = GestorServidores()
			res = dlg.ShowModal()
			if res == 0:
				dlg.Destroy()
				self.onChoiceSRV(None)
				self.choiceSRV.Clear()
				self.choiceSRV.Append(
					[ajustes.listaServidores[i][0] for i in range(len(ajustes.listaServidores))]
				)
				self.choiceSRV.SetSelection(ajustes.selectSRV)
				self.choiceSRV.SetFocus()

	def onBackup(self, event):
		from .addon_manager import AddonManager
		with wx.FileDialog(
			self,
			message=_("Guardar copia de seguridad de complementos"),
			defaultDir=os.path.expanduser("~\\Documents"),
			defaultFile="mis_complementos.json",
			wildcard="Archivo JSON (*.json)|*.json",
			style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
		) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return
			path = fileDialog.GetPath()
			try:
				AddonManager.createBackup(path)
				ui.message(_("Copia de seguridad guardada con éxito en: {}").format(path))
			except Exception as e:
				ui.message(_("Error al crear la copia de seguridad: {}").format(e))

	def onRestore(self, event):
		with wx.FileDialog(
			self,
			message=_("Seleccionar archivo de copia de seguridad"),
			defaultDir=os.path.expanduser("~\\Documents"),
			wildcard="Archivo JSON (*.json)|*.json",
			style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
		) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return
			backup_file = fileDialog.GetPath()

			try:
				with open(backup_file, "r", encoding="utf-8") as f:
					backup_data = json.load(f)

				if 'addons' not in backup_data:
					ui.message(_("El archivo seleccionado no es una copia de seguridad válida."))
					return

				msg = _("¿Desea restaurar los complementos desde el archivo seleccionado? Esto abrirá el asistente de instalación por lotes.")
				if wx.MessageBox(msg, _("Restaurar"), wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
					if ajustes.IS_WinON == False:
						from .dialogos_actualizaciones import RestaurarBackupDialogo
						dlg = RestaurarBackupDialogo(gui.mainFrame, backup_data)
						gui.mainFrame.prePopup()
						dlg.ShowModal()
						dlg.Destroy()
					else:
						ui.message(_("Cierre la tienda antes de proceder con la restauración."))
			except Exception as e:
				ui.message(_("Error al cargar el backup: {}").format(e))
				log.error(f"Error en onRestore: {e}", exc_info=True)
