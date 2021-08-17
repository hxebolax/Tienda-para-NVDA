# -*- coding: utf-8 -*-
# Copyright (C) 2021 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.
#
# Agradecimientos:
#
# Idioma inglés: Nikola Jović
# Idioma y documentación portugués: Ângelo Miguel Abrantes
# Idiomas croata y polaco: Zvonimir Stanečić
# Idioma Ruso: comunidad rusa NVDA.RU
# Idioma y documentación francés: Rémy Ruiz
# Idioma ucraniano: Volodymyr Pyrih
#
# import the necessary modules (NVDA)
import globalPluginHandler
import addonHandler
import gui
from gui.nvdaControls import CustomCheckListBox
from gui import addonGui # update
from addonHandler import addonVersionCheck # update
import globalVars
import ui
from scriptHandler import script
import core
from logHandler import log
from gui.settingsDialogs import NVDASettingsDialog, SettingsPanel
from gui import guiHelper, nvdaControls
import wx
import wx.adv
import webbrowser
from threading import Thread
import urllib.request
import socket
import time
import winsound
import shutil
import os
import sys

# For translation
addonHandler.initTranslation()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
	import ajustes
	import basedatos
	inicio = True
except Exception as e:
	log.info(_("No se pudieron cargar las librerías necesarias para la Tienda"))
	inicio = False

def function_ChkUpdate():
	"""Función para controlar el hilo que busca con tiempo actualizaciones"""
	if ajustes.reiniciarTrue == False:
		try:
			datos = basedatos.NVDAStoreClient()
			nombreUrl, verInstalada, verInstalar = datos.chkActualizaS()
			if nombreUrl == False:
				if ajustes.contadorRepeticionSn <= 9:
					ajustes.contadorRepeticionSn = ajustes.contadorRepeticionSn + 1
					pass
				else:
					chkUpdate.stop()
			else:
				if ajustes.contadorRepeticion <= 4:
					ajustes.contadorRepeticion = ajustes.contadorRepeticion + 1
					if len(nombreUrl) == 1:
						msg = \
_("""Se encontró una actualización. 

Ejecute Buscar actualizaciones de complementos de la Tienda NVDA.ES""")
						# Translators: Title of the notification
						notify = wx.adv.NotificationMessage(title=_("Información"),
							# Translators: Notification message
							message=msg, parent=None, flags=wx.ICON_INFORMATION)
						notify.Show(timeout=10)
					else:
						msg = \
_("""Se encontraron  {} actualizaciones. 

Ejecute Buscar actualizaciones de complementos de la Tienda NVDA.ES""").format(len(nombreUrl))
						# Translators: Title of the notification
						notify = wx.adv.NotificationMessage(title=_("Información"),
							# Translators: Notification message
							message=msg, parent=None, flags=wx.ICON_INFORMATION)
						notify.Show(timeout=10)
				else:
					chkUpdate.stop()
		except Exception as e:
			log.info("Error al comprobar actualizaciones automáticas")
			chkUpdate.stop()
	else:
		msg = \
		_("""Necesita reiniciar NVDA para aplicar las actualizaciones.""")
		# Translators: Title of the notification
		notify = wx.adv.NotificationMessage(title=_("Información"),
			# Translators: Notification message
			message=msg, parent=None, flags=wx.ICON_INFORMATION)
		notify.Show(timeout=10)

if inicio == True:
	chkUpdate = basedatos.RepeatTimer(ajustes.tiempoDict.get(ajustes.tempTimer), function_ChkUpdate)
	if ajustes.tempChk == False:
		chkUpdate.stop()
else:
	log.info(_("Inicio del complemento cancelado."))

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()

		if globalVars.appArgs.secure: return

		if inicio == True:
			NVDASettingsDialog.categoryClasses.append(TiendaPanel)

			self.menu = wx.Menu()
			tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
			# Translators: Nombre del submenú para tienda de complementos
			self.tiendaComplementos = self.menu.Append(wx.ID_ANY, _("Listado de complementos"))
			gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_menu1, self.tiendaComplementos)
			# Translators: Nombre del submenú para buscar actualizaciones
			self.tiendaActualizaciones = self.menu.Append(wx.ID_ANY, _("Buscar actualizaciones de complementos"))
			gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_menu2, self.tiendaActualizaciones)
			# Translators: Nombre del menú Tienda de complementos
			self.tiendaMenu = tools_menu.AppendSubMenu(self.menu, _("Tienda NVDA.ES"))
		else:
			return

	def terminate(self):
		global chkUpdate
		try:
			if inicio == True:
				chkUpdate.stop()
				NVDASettingsDialog.categoryClasses.remove(TiendaPanel)
			if not self._MainWindows:
				self._MainWindows.Destroy()
		except (AttributeError, RuntimeError):
			pass

	@script(gesture=None, description= _("Muestra la ventana con todos los complementos y su información"), category= _("Tienda para NVDA.ES"))
	def script_menu1(self, event):
		if inicio == True:
			if ajustes.IS_WinON == False:
				self._MainWindows = HiloComplemento(1)
				self._MainWindows.start()
			else:
				ui.message(_("Ya hay una instancia de la Tienda NVDA abierta."))
		else:
			msg = \
_("""El complemento fallo al iniciar NVDA.

Una de las causas es que NVDA arrancara antes de tener conexión a internet.

Reinicie NVDA para intentar solucionar el problema.""")
			ui.message(msg)

	@script(gesture=None, description= _("Busca actualizaciones de los complementos instalados"), category= _("Tienda para NVDA.ES"))
	def script_menu2(self, event):
		if inicio == True:
			if ajustes.reiniciarTrue == False:
				if ajustes.IS_WinON == False:
					self._MainWindows = HiloComplemento(2)
					self._MainWindows.start()
				else:
					ui.message(_("Ya hay una instancia de la Tienda NVDA abierta."))
			else:
				ui.message(_("Necesita reiniciar NVDA para aplicar las actualizaciones."))
		else:
			msg = \
_("""El complemento fallo al iniciar NVDA.

Una de las causas es que NVDA arrancara antes de tener conexión a internet.

Reinicie NVDA para intentar solucionar el problema.""")
			ui.message(msg)

class TiendaPanel(SettingsPanel):
	#TRANSLATORS: title for the Update Channel settings category
	title = _("Tienda NVDA.ES")

	def makeSettings(self, sizer):
		helper=guiHelper.BoxSizerHelper(self, sizer=sizer)

		self.autoChk = helper.addItem(wx.CheckBox(self, label=_("Activar o desactivar la comprobación de actualizaciones")))
		self.autoChk.Bind(wx.EVT_CHECKBOX,self.onAutoChk)

		self.choiceTimer = helper.addLabeledControl(_("Seleccione un tiempo para comprobar si hay actualizaciones"), wx.Choice, choices=ajustes.tiempoChk)

		self.ordenChk = helper.addItem(wx.CheckBox(self, label=_("Ordenar por orden alfabético los complementos de la tienda y las búsquedas")))

		self.installChk = helper.addItem(wx.CheckBox(self, label=_("Instalar complementos después de descargar")))

		self.datos = basedatos.NVDAStoreClient()
		self.datosServidor = self.datos.dataServidor
		self.listbox = helper.addLabeledControl(_("Complementos instalados que hay en el servidor:"), wx.ListBox)
		for i in ajustes.listaAddonsSave:
			for x in range(0, len(self.datosServidor)):
				if self.datosServidor[x]['name'].lower() == i[0].lower():
					self.listbox.Append("{} -- {}".format(self.datosServidor[x]['summary'], self.datosServidor[x]['links'][i[1]]['channel']))
		self.listbox.SetSelection(0)
		self.listbox.Bind(wx.EVT_KEY_UP, self.onListBox)

		self.autoChk.Value = ajustes.tempChk
		if self.autoChk.Value == True:
			self.choiceTimer.Enable()
		else:
			self.choiceTimer.Disable()

		self.choiceTimer.Selection = ajustes.tempTimer

		self.ordenChk.Value =ajustes.tempOrden

		self.installChk.Value =ajustes.tempInstall

		self.listaGuarda = []

	def onSave(self):
		global chkUpdate
		ajustes.setConfig("autoChk", self.autoChk.Value)
		ajustes.setConfig("timerChk", self.choiceTimer.Selection)
		ajustes.setConfig("ordenChk", self.ordenChk.Value)
		ajustes.setConfig("installChk", self.installChk.Value)

		ajustes.tempChk = self.autoChk.Value
		ajustes. tempTimer= self.choiceTimer.Selection
		ajustes.tempOrden = self.ordenChk.Value
		ajustes.tempInstall = self.installChk.Value

		if ajustes.tempChk == True:
			chkUpdate = basedatos.RepeatTimer(ajustes.tiempoDict.get(ajustes.tempTimer), function_ChkUpdate)
			chkUpdate.start()
		else:
			chkUpdate.stop()
			ajustes.contadorRepeticion = 0
			ajustes.contadorRepeticionSn = 0

		if len(self.listaGuarda) == 0:
			pass
		else:
			for i in range(0, len(self.listaGuarda)):
				ajustes.listaAddonsSave[self.listaGuarda[i][0]][1] = self.listaGuarda[i][1]
		basedatos.libreriaLocal().fileJsonAddon(1, basedatos.libreriaLocal().ordenaLista(ajustes.listaAddonsSave))

	def onAutoChk(self, event):
		chk = event.GetEventObject()
		if chk.GetValue() == True:
			self.choiceTimer.Enable()
		else:
			self.choiceTimer.Disable()

	def onListBox(self, event):
		nombre = self.listbox.GetString(self.listbox.GetSelection()).split(" -- ")
		nombreLocal = ajustes.listaAddonsSave[self.listbox.GetSelection()][0]
		indice = self.datos.indiceName(nombreLocal)
		datos = self.datosServidor[indice]
		if event.GetKeyCode() == 32: # Pulsamos intro para seleccionar. 32 es espacio.
			self.menuDescarga = wx.Menu()
			for i in range(len(datos['links'])):
				item = self.menuDescarga.Append(i, _("Canal {}").format(datos['links'][i]['channel']))
				self.Bind(wx.EVT_MENU, self.onSelect, item)

			position = self.listbox.GetPosition()
			self.PopupMenu(self.menuDescarga,position)
			pass

	def modificaListBox(self, canalID):
		nombre = self.listbox.GetString(self.listbox.GetSelection()).split(" -- ")
		nombreLocal = ajustes.listaAddonsSave[self.listbox.GetSelection()][0]
		indice = self.datos.indiceName(nombreLocal)
		datos = self.datosServidor[indice]
		nombreCanal = datos['links'][canalID]['channel']
		nombreCompuesto = nombre[0] + " -- " + nombreCanal
		pos = self.listbox.GetSelection()
		self.listbox.Delete(pos)
		self.listbox.Insert(nombreCompuesto, pos)
		self.listbox.SetSelection(pos)
		self.listaGuarda.append([pos, canalID])

	def onSelect(self, event):
		self.modificaListBox(event.GetId())

class tiendaApp(wx.Dialog):
	def __init__(self, parent, dataServidor):

		WIDTH = 1600
		HEIGHT = 800

		super(tiendaApp,self).__init__(parent, -1, title=_("Tienda NVDA.ES"), size = (WIDTH, HEIGHT))

		ajustes.IS_WinON = True
		self.datos = dataServidor

		self.Panel = wx.Panel(self, 1)

		labelBusqueda = wx.StaticText(self.Panel, wx.ID_ANY, _("&Buscar:"))
		self.textoBusqueda = wx.TextCtrl(self.Panel, 2,style = wx.TE_PROCESS_ENTER)
		self.textoBusqueda.Bind(wx.EVT_TEXT_ENTER, self.onBusqueda)
		self.textoBusqueda.Bind(wx.EVT_CONTEXT_MENU, self.skip)

		labelComplementos = wx.StaticText(self.Panel, wx.ID_ANY, _("&Lista complementos:"))
		self.listboxComplementos = wx.ListBox(self.Panel, 3, style = wx.LB_NO_SB)

		self.temporal = []
		for x in range(0, len(self.datos.dataServidor)):
			self.temporal.append(self.datos.dataServidor[x]['summary'])

		if ajustes.tempOrden == False:
			self.listboxComplementos.Append(self.temporal)
		else:
			self.listboxComplementos.Append(sorted(self.temporal, key=str.lower))
		self.listboxComplementos.SetSelection(0)
		self.listboxComplementos.SetFocus()
		self.listboxComplementos.Bind(wx.EVT_KEY_UP, self.onLisbox)

		labelResultado = wx.StaticText(self.Panel, wx.ID_ANY, _("&Información:"))
		self.txtResultado = wx.TextCtrl(self.Panel, 4, style =wx.TE_MULTILINE|wx.TE_READONLY|wx.LB_NO_SB)
		self.txtResultado.Bind(wx.EVT_CONTEXT_MENU, self.skip)

		self.descargarBTN = wx.Button(self.Panel, 201, _("&Descargar complemento"))
		self.paginaWebBTN = wx.Button(self.Panel, 202, _("Visitar &página WEB"))
		self.salirBTN = wx.Button(self.Panel, 203, _("&Salir"))
		self.Bind(wx.EVT_BUTTON,self.onBoton)
		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)
		self.Bind(wx.EVT_CLOSE, self.onBoton)

		szMain = wx.BoxSizer(wx.HORIZONTAL)
		szComplementos = wx.BoxSizer(wx.VERTICAL)
		szResultados = wx.BoxSizer(wx.VERTICAL)
		szBotones = wx.BoxSizer(wx.HORIZONTAL)

		szComplementos.Add(labelBusqueda, 0)
		szComplementos.Add(self.textoBusqueda, 0, wx.EXPAND)
		szComplementos.Add(labelComplementos, 0)
		szComplementos.Add(self.listboxComplementos, 1, wx.EXPAND)

		szResultados.Add(labelResultado, 0)
		szResultados.Add(self.txtResultado, 1, wx.EXPAND)

		szBotones.Add(self.descargarBTN, 2, wx.CENTRE)
		szBotones.Add(self.paginaWebBTN, 2, wx.CENTRE)
		szBotones.Add(self.salirBTN, 2, wx.CENTRE)

		szComplementos.Add(szBotones, 0, wx.EXPAND)

		szMain.Add(szComplementos, 0, wx.EXPAND)
		szMain.Add(szResultados, 1, wx.EXPAND)

		self.Panel.SetSizer(szMain)

		self.onLisbox(None)
		self.onFocus()

		self.CenterOnScreen()

	def onFicha(self):
		nombre = self.listboxComplementos.GetString(self.listboxComplementos.GetSelection())
		indice = self.datos.indiceSummary(nombre)
		datos = self.datos.dataServidor[indice]
		ficha = \
_("""Autor: {}
Nombre del complemento: {}
Nombre interno: {}
Descripción: {}
Desarrollo: {}\n""").format(
	datos['author'],
	datos['summary'],
	datos['name'],
	datos['description'],
	_("Con soporte") if datos['legacy'] == 0 else _("Sin soporte"),
	)
		self.txtResultado.SetValue(ficha)

		for i in range(len(datos['links'])):
			fichaEnlaces = \
_("""Canal: {}
Versión: {}
Mínimo NVDA: {}
Testeado hasta versión de NVDA: {}
Total descargas: {}\n""").format(
	datos['links'][i]['channel'],
	datos['links'][i]['version'],
	datos['links'][i]['minimum'],
	datos['links'][i]['lasttested'],
	datos['links'][i]['downloads'],
	)
			self.txtResultado.AppendText(fichaEnlaces)
		self.txtResultado.SetInsertionPoint(0)

	def onFocus(self):
		self.Bind(wx.EVT_ACTIVATE, self.onSetFocus)
		self.textoBusqueda.Bind(wx.EVT_SET_FOCUS, self.onSetSelection)
		self.listboxComplementos.Bind(wx.EVT_SET_FOCUS, self.onSetSelection)
		self.txtResultado.Bind(wx.EVT_SET_FOCUS, self.onSetSelection)
		self.descargarBTN.Bind(wx.EVT_SET_FOCUS, self.onSetSelection)
		self.paginaWebBTN.Bind(wx.EVT_SET_FOCUS, self.onSetSelection)
		self.salirBTN.Bind(wx.EVT_SET_FOCUS, self.onSetSelection)

	def onSetFocus(self, event):
		"""Devolvemos el foco al último widget que lo tubo"""
		if event.GetActive() == True:
			getattr(self, ajustes.focoActual).SetFocus()
			pass

	def onSetSelection(self, event):
		"""Guarda en la variable el widgetque tiene el foco"""
		ajustes.focoActual = ajustes.id_widgets.get(event.GetId())

	def skip(self, event):
		return

	def onBusqueda(self, event):
		if self.textoBusqueda.GetValue() == "":
			self.listboxComplementos.Clear()
			if ajustes.tempOrden == False:
				self.listboxComplementos.Append(self.temporal)
			else:
				self.listboxComplementos.Append(sorted(self.temporal, key=str.lower))
			self.listboxComplementos.SetSelection(0)
			self.listboxComplementos.SetFocus()
		else:
			pattern = self.textoBusqueda.GetValue()
			listTemp = []
			for x in range(0, len(self.datos.dataServidor)):
				listTemp.append(self.datos.dataServidor[x]['summary'])
			filtro = [item for item in listTemp if pattern.lower() in item.lower()]
			self.listboxComplementos.Clear()
			if len(filtro) == 0:
				self.listboxComplementos.Append(_("No se encontraron resultados"))
				self.listboxComplementos.SetSelection(0)
				self.listboxComplementos.SetFocus()
			else:
				if ajustes.tempOrden == False:
					self.listboxComplementos.Append(filtro)
				else:
					self.listboxComplementos.Append(sorted(filtro, key=str.lower))
				self.listboxComplementos.SetSelection(0)
				self.listboxComplementos.SetFocus()

	def onLisbox(self, event):
		if self.listboxComplementos.GetSelection() == -1:
			pass
		else:
			if self.listboxComplementos.GetString(self.listboxComplementos.GetSelection()) == _("No se encontraron resultados"):
				self.txtResultado.Clear()
			else:
				self.onFicha()

	def onBoton(self, event):
		obj = event.GetEventObject()
		botonID = obj.GetId()
		nombre = self.listboxComplementos.GetString(self.listboxComplementos.GetSelection())
		indice = self.datos.indiceSummary(nombre)
		datos = self.datos.dataServidor[indice]
		if botonID == 201:
			self.menuDescarga = wx.Menu()

			for i in range(len(datos['links'])):
				item = self.menuDescarga.Append(i, _("Versión {}").format(datos['links'][i]['channel']))
				self.Bind(wx.EVT_MENU, self.onDescarga, item)

			position = self.descargarBTN.GetPosition()
			self.PopupMenu(self.menuDescarga,position)
			pass

		elif botonID == 202:
			webbrowser.open_new(datos['url'])
		elif botonID == 203:
			if ajustes.IS_Download == False:
				ajustes.IS_WinON = False
			ajustes.focoActual = "listboxComplementos"
			self.Destroy()
			gui.mainFrame.postPopup()
		else:
			if ajustes.IS_Download == False:
				ajustes.IS_WinON = False
			ajustes.focoActual = "listboxComplementos"
			self.Destroy()
			gui.mainFrame.postPopup()

	def onDescarga(self, event):
		if ajustes.IS_Download == False:
			HiloGuardarArchivo(self, event.GetId())
		else:
			msg = \
_("""Ya tiene un proceso de descarga activo, espere a que termine.""")
						# Translators: Title of the notification
			notify = wx.adv.NotificationMessage(title=_("Información"),
							# Translators: Notification message
				message=msg, parent=None, flags=wx.ICON_INFORMATION)
			notify.Show(timeout=10)

	def TrueDescarga(self, fichero_final, url, path):
		dlg = DescargaDialogo(_("Descargando %s...") % fichero_final, url, path, 15)
		result = dlg.ShowModal()
		if result == ajustes.ID_TRUE:
			if ajustes.tempInstall == True:
				addonGui.handleRemoteAddonInstall(path)
			try:
				ajustes.IS_Download = False
				self.listboxComplementos.SetFocus()
			except:
				ajustes.IS_Download = False
				ajustes.IS_WinON = False
				pass
			dlg.Destroy()
		else:
			try:
				ajustes.IS_Download = False
				self.listboxComplementos.SetFocus()
			except:
				ajustes.IS_Download = False
				ajustes.IS_WinON = False
				pass
			dlg.Destroy()

	def FalseDescarga(self):
		try:
			ajustes.IS_Download = False
			getattr(self, ajustes.focoActual).SetFocus()
			pass
		except:
			ajustes.IS_Download = False
			ajustes.IS_WinON = False
			pass

	def onkeyVentanaDialogo(self, event):
		if event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
			if ajustes.IS_Download == False:
				ajustes.IS_WinON = False
			ajustes.focoActual = "listboxComplementos"
			self.Destroy()
			gui.mainFrame.postPopup()
		else:
			event.Skip()

class BuscarActualizacionesDialogo(wx.Dialog):
	def __init__(self, parent, nombreUrl, verInstalada, verInstalar):

		WIDTH = 800
		HEIGHT = 600

		super(BuscarActualizacionesDialogo,self).__init__(parent, -1, title=_("Tienda NVDA.ES - Actualizaciones disponibles"), size = (WIDTH, HEIGHT))

		global chkUpdate
		if ajustes.tempChk == True:
			chkUpdate.stop()

		ajustes.IS_WinON = True

		# Dict con nombre complemento, url descarga
		self.nombreUrl = nombreUrl
		self.verInstalada = verInstalada
		self.verInstalar = verInstalar

		self.Panel = wx.Panel(self, 1)

		self.chkListBox = CustomCheckListBox(self.Panel, 2)
		for i in range(0, len(self.nombreUrl)):
			self.chkListBox.Append("{} {}-{}".format(list(self.nombreUrl.keys())[i], self.verInstalada[i], self.verInstalar[i]))
		self.chkListBox.Select(0)
		self.chkListBox.Bind(wx.EVT_CHECKLISTBOX, self.onAddonsChecked)

		self.selectionAllBTN = wx.Button(self.Panel, 101, _("&Seleccionar todo"))
		self.unselectionAllBTN = wx.Button(self.Panel, 102, _("&Deseleccionar todo"))
		self.ActualizarBTN = wx.Button(self.Panel, 103, _("&Actualizar"))
		self.CerrarBTN = wx.Button(self.Panel, 104, _("&Cerrar"))
		self.Bind(wx.EVT_BUTTON,self.onBoton)
		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)
		self.Bind(wx.EVT_CLOSE, self.onBoton)

		sizeMain = wx.BoxSizer(wx.VERTICAL)
		szBotoneSelect = wx.BoxSizer(wx.HORIZONTAL)
		szBotones = wx.BoxSizer(wx.HORIZONTAL)

		sizeMain.Add(self.chkListBox, 1, wx.EXPAND)

		szBotoneSelect.Add(self.selectionAllBTN, 2, wx.CENTER)
		szBotoneSelect.Add(self.unselectionAllBTN, 2, wx.CENTER)

		sizeMain.Add(szBotoneSelect, 0, wx.EXPAND)

		szBotones.Add(self.ActualizarBTN, 2, wx.CENTER)
		szBotones.Add(self.CerrarBTN, 2, wx.CENTER)

		sizeMain.Add(szBotones, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeMain)

		self.CenterOnScreen()

	def onAddonsChecked(self, event):
		index = event.GetSelection()
		label = self.chkListBox.GetString(index)
		status = False
		if self.chkListBox.IsChecked(index):
			status = True
		self.chkListBox.SetSelection(index)    # so that (un)checking also selects (moves the highlight)

	def onBoton(self, event):
		global chkUpdate
		obj = event.GetEventObject()
		botonID = obj.GetId()
		if botonID == 101:
			num = self.chkListBox.GetCount()
			for i in range(num):
				self.chkListBox.Check(	i, True)
			self.chkListBox.SetSelection(0)
			self.chkListBox.SetFocus()
		elif botonID == 102:
			self.chkListBox.Clear()
			for i in range(0, len(self.nombreUrl)):
				self.chkListBox.Append("{} {}-{}".format(list(self.nombreUrl.keys())[i], self.verInstalada[i], self.verInstalar[i]))
			self.chkListBox.Select(0)
			self.chkListBox.SetFocus()
		elif botonID == 103:
			listaSeleccion = [i for i in range(self.chkListBox.GetCount()) if self.chkListBox.IsChecked(i)]
			if len(listaSeleccion) == 0:
				gui.messageBox(_("Tiene que seleccionar una actualización para poder continuar."),
					_("Error"), wx.ICON_ERROR)
				self.chkListBox.SetFocus()
			else:
				hilo =HiloLanzaActualizacion(self.nombreUrl, listaSeleccion)
				hilo.start()
				ajustes.IS_WinON = False
				self.Destroy()
				gui.mainFrame.postPopup()
		elif botonID == 104:
			if ajustes.tempChk == True:
				chkUpdate = basedatos.RepeatTimer(ajustes.tiempoDict.get(ajustes.tempTimer), function_ChkUpdate)
			ajustes.IS_WinON = False
			self.Destroy()
			gui.mainFrame.postPopup()
		else:
			if ajustes.tempChk == True:
				chkUpdate = basedatos.RepeatTimer(ajustes.tiempoDict.get(ajustes.tempTimer), function_ChkUpdate)
			ajustes.IS_WinON = False
			self.Destroy()
			gui.mainFrame.postPopup()

	def onkeyVentanaDialogo(self, event):
		global chkUpdate
		if event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
			if ajustes.tempChk == True:
				chkUpdate = basedatos.RepeatTimer(ajustes.tiempoDict.get(ajustes.tempTimer), function_ChkUpdate)
			ajustes.IS_WinON = False
			self.Destroy()
			gui.mainFrame.postPopup()
		else:
			event.Skip()

class DescargaDialogo(wx.Dialog):
	def __init__(self, titulo, url, file, seconds):

		WIDTH = 550
		HEIGHT = 400

		super(DescargaDialogo, self).__init__(None, -1, title=titulo, size = (WIDTH, HEIGHT))

		self.CenterOnScreen()

		self.url = url
		self.file = file
		self.seconds = seconds

		panel = wx.Panel(self)
		self.Panel = panel

		self.progressBar=wx.Gauge(self.Panel, wx.ID_ANY, range=100, style = wx.GA_HORIZONTAL)
		self.textorefresco = wx.TextCtrl(self.Panel, wx.ID_ANY, style =wx.TE_MULTILINE|wx.TE_READONLY)
		self.textorefresco.Bind(wx.EVT_CONTEXT_MENU, self.skip)

		self.AceptarTRUE = wx.Button(self.Panel, ajustes.ID_TRUE, _("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptarTRUE, id=self.AceptarTRUE.GetId())
		self.AceptarTRUE.Disable()

		self.AceptarFALSE = wx.Button(self.Panel, ajustes.ID_FALSE, _("&Cerrar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptarFALSE, id=self.AceptarFALSE.GetId())
		self.AceptarFALSE.Disable()

		self.Bind(wx.EVT_CLOSE, self.onNull)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer_botones = wx.BoxSizer(wx.HORIZONTAL)

		sizer.Add(self.progressBar, 0, wx.EXPAND)
		sizer.Add(self.textorefresco, 1, wx.EXPAND)

		sizer_botones.Add(self.AceptarTRUE, 2, wx.CENTER)
		sizer_botones.Add(self.AceptarFALSE, 2, wx.CENTER)

		sizer.Add(sizer_botones, 0, wx.EXPAND)

		self.Panel.SetSizer(sizer)

		HiloDescarga(self, self.url, self.file, self.seconds)

		self.textorefresco.SetFocus()

	def skip(self, event):
		return

	def onNull(self, event):
		pass

	def next(self, event):
		self.progressBar.SetValue(event)

	def TextoRefresco(self, event):
		self.textorefresco.Clear()
		self.textorefresco.AppendText(event)

	def done(self, event):
		winsound.MessageBeep(0)
		self.AceptarTRUE.Enable()
		self.textorefresco.Clear()
		self.textorefresco.AppendText(event)
		self.textorefresco.SetInsertionPoint(0) 

	def error(self, event):
		winsound.MessageBeep(16)
		self.AceptarFALSE.Enable()
		self.textorefresco.Clear()
		self.textorefresco.AppendText(event)
		self.textorefresco.SetInsertionPoint(0) 

	def onAceptarTRUE(self, event):
		if self.IsModal():
			self.EndModal(event.EventObject.Id)
		else:
			self.Close()

	def onAceptarFALSE(self, event):
		if self.IsModal():
			self.EndModal(event.EventObject.Id)
		else:
			self.Close()

class ActualizacionDialogo(wx.Dialog):
	def __init__(self, frame, nombreUrl, listaSeleccion, seconds):

		WIDTH = 550
		HEIGHT = 400

		super(ActualizacionDialogo, self).__init__(None, -1, title=_("Actualizando complementos"), size = (WIDTH, HEIGHT))

		self.CenterOnScreen()

		ajustes.IS_WinON = True

		self.frame = frame
		self.nombreUrl = nombreUrl
		self.listaSeleccion = listaSeleccion
		self.seconds = seconds

		panel = wx.Panel(self)
		self.Panel = panel

		self.ProgressDescarga=wx.Gauge(self.Panel, wx.ID_ANY, range=100, style = wx.GA_HORIZONTAL)
		self.ProgressActualizacion=wx.Gauge(self.Panel, wx.ID_ANY, range=len(listaSeleccion), style = wx.GA_HORIZONTAL)
		self.textorefresco = wx.TextCtrl(self.Panel, wx.ID_ANY, style =wx.TE_MULTILINE|wx.TE_READONLY)
		self.textorefresco.Bind(wx.EVT_CONTEXT_MENU, self.skip)

		self.AceptarTRUE = wx.Button(self.Panel, ajustes.ID_TRUE, _("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptarTRUE, id=self.AceptarTRUE.GetId())
		self.AceptarTRUE.Disable()

		self.AceptarFALSE = wx.Button(self.Panel, ajustes.ID_FALSE, _("&Cerrar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptarFALSE, id=self.AceptarFALSE.GetId())
		self.AceptarFALSE.Disable()

		self.Bind(wx.EVT_CLOSE, self.onNull)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer_botones = wx.BoxSizer(wx.HORIZONTAL)

		sizer.Add(self.ProgressDescarga, 0, wx.EXPAND)
		sizer.Add(self.ProgressActualizacion, 0, wx.EXPAND)
		sizer.Add(self.textorefresco, 1, wx.EXPAND)

		sizer_botones.Add(self.AceptarTRUE, 2, wx.CENTER)
		sizer_botones.Add(self.AceptarFALSE, 2, wx.CENTER)

		sizer.Add(sizer_botones, 0, wx.EXPAND)

		self.Panel.SetSizer(sizer)

		HiloActualizacion(self, self.nombreUrl, self.listaSeleccion, self.seconds)

		self.textorefresco.SetFocus()

	def skip(self, event):
		return

	def onNull(self, event):
		pass

	def onDescarga(self, event):
		self.ProgressDescarga.SetValue(event)

	def onActualizacion(self, event):
		self.ProgressActualizacion.SetValue(event)

	def TextoRefresco(self, event):
		self.textorefresco.Clear()
		self.textorefresco.AppendText(event)

	def done(self, event):
		winsound.MessageBeep(0)
		self.AceptarTRUE.Enable()
		self.AceptarFALSE.Enable()
		self.textorefresco.Clear()
		self.textorefresco.AppendText(event)
		self.textorefresco.SetInsertionPoint(0) 

	def error(self, event):
		winsound.MessageBeep(16)
		self.AceptarFALSE.Enable()
		self.textorefresco.Clear()
		self.textorefresco.AppendText(event)
		self.textorefresco.SetInsertionPoint(0) 

	def onAceptarTRUE(self, event):
		ajustes.IS_WinON = False
		self.Destroy()
		gui.mainFrame.postPopup()
		core.restart()

	def onAceptarFALSE(self, event):
		global chkUpdate
		if ajustes.tempChk == True:
			chkUpdate = basedatos.RepeatTimer(ajustes.tiempoDict.get(ajustes.tempTimer), function_ChkUpdate)
		ajustes.IS_WinON = False
		self.Destroy()
		gui.mainFrame.postPopup()

class HiloGuardarArchivo(Thread):
	def __init__(self, frame, id):
		super(HiloGuardarArchivo, self).__init__()

		self.frame = frame
		self.id = id
		self.nombreFile = ""
		self.url = ""
		ajustes.IS_Download = True
		try:
			winsound.PlaySound(os.path.join(os.path.dirname(os.path.abspath(__file__)), "progress.wav"), winsound.SND_LOOP + winsound.SND_ASYNC)
		except:
			pass

		self.daemon = True
		self.start()
	def run(self):
		nombre = self.frame.listboxComplementos.GetString(self.frame.listboxComplementos.GetSelection())
		indice = self.frame.datos.indiceSummary(nombre)
		datos = self.frame.datos.dataServidor[indice]
		self.url = self.frame.datos.urlBase+datos['links'][self.id]['file']
		self.nombreFile = self.frame.datos.GetFilenameDownload(datos['links'][self.id]['file'])
		if self.nombreFile.split(".")[0] == "get":
			try:
				self.nombreFile = basedatos.obtenFile(datos['links'][self.id]['link'])
			except:
				try:
					self.nombreFile = basedatos.obtenFileAlt(self.url)
				except:
					try:
						self.nombreFile = basedatos.ultimoAlternativo(self.url)
					except:
						try:
							self.nombreFile = basedatos.ultimoAlternativo(datos['links'][self.id]['link'])
							self.url = datos['links'][self.id]['link']
						except:
							winsound.PlaySound(None, winsound.SND_PURGE)
							msg = \
_("""No se pudo obtener el nombre del archivo a descargar.

{} del canal {}

Se va a proceder a descargar con su navegador predefinido.""").format(nombre, datos['links'][self.id]['channel'])
							gui.messageBox(msg,
								_("Información"), wx.ICON_INFORMATION)
							self.nombreFile = ""
							webbrowser.open_new(self.url)
							return
		if self.nombreFile == "downloads":
			winsound.PlaySound(None, winsound.SND_PURGE)
			msg = \
_("""Este complemento necesita ser descargado desde su página web.

Se abrirá con su navegador predefinido en la pagina de descarga del complemento.""")
			gui.messageBox(msg,
				_("Información"), wx.ICON_INFORMATION)

			webbrowser.open_new(datos['links'][self.id]['link'])
			return
		else:
			caracteres = '\/:*?"<>| '
			if any(c in caracteres for c in self.nombreFile):
				try:
					self.nombreFile = basedatos.ultimoAlternativo(self.url)
				except:
					try:
						self.nombreFile = basedatos.ultimoAlternativo(datos['links'][self.id]['link'])
						self.url = datos['links'][self.id]['link']
					except:
						winsound.PlaySound(None, winsound.SND_PURGE)
						msg = \
_("""No se pudo obtener el nombre del archivo a descargar.

{} del canal {}

Se va a proceder a descargar con su navegador predefinido.""").format(nombre, datos['links'][self.id]['channel'])
						gui.messageBox(msg,
							_("Información"), wx.ICON_INFORMATION)
						self.nombreFile = ""
						webbrowser.open_new(self.url)
						return

		winsound.PlaySound(None, winsound.SND_PURGE)
		wildcard = _("Complemento de NVDA (*.nvda-addon)|*.nvda-addon")
		dlg = wx.FileDialog(None, message=_("Guardar en..."), defaultDir=os.environ['SYSTEMDRIVE'], defaultFile=self.nombreFile, wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			fichero_final = os.path.basename(path)
			dlg.Destroy()
			wx.CallAfter(self.frame.TrueDescarga, fichero_final, self.url, path)
		else:
			dlg.Destroy()
			wx.CallAfter(self.frame.FalseDescarga)

class HiloDescarga(Thread):
	def __init__(self, frame, url, ruta, tiempo):
		super(HiloDescarga, self).__init__()

		self.frame = frame
		self.url = url
		self.ruta = ruta
		self.tiempo = tiempo

		self.daemon = True
		self.start()

	def humanbytes(self, B): # Convierte bytes
		B = float(B)
		KB = float(1024)
		MB = float(KB ** 2) # 1,048,576
		GB = float(KB ** 3) # 1,073,741,824
		TB = float(KB ** 4) # 1,099,511,627,776

		if B < KB:
			return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
		elif KB <= B < MB:
			return '{0:.2f} KB'.format(B/KB)
		elif MB <= B < GB:
			return '{0:.2f} MB'.format(B/MB)
		elif GB <= B < TB:
			return '{0:.2f} GB'.format(B/GB)
		elif TB <= B:
			return '{0:.2f} TB'.format(B/TB)

	def __call__(self, block_num, block_size, total_size):
		readsofar = block_num * block_size
		if total_size > 0:
			percent = readsofar * 1e2 / total_size
			wx.CallAfter(self.frame.next, percent)
			time.sleep(1 / 995)
			wx.CallAfter(self.frame.TextoRefresco, _("Espere por favor...\n") + _("Descargando: %s") % self.humanbytes(readsofar))
			if readsofar >= total_size: # Si queremos hacer algo cuando la descarga termina.
				pass
		else: # Si la descarga es solo el tamaño
			wx.CallAfter(self.frame.TextoRefresco, _("Espere por favor...\n") + _("Descargando: %s") % self.humanbytes(readsofar))

	def run(self):
		try:
			socket.setdefaulttimeout(self.tiempo) # Dara error si pasan 30 seg sin internet
			try:
				req = urllib.request.Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
				obj = urllib.request.urlopen(req).geturl()
				urllib.request.urlretrieve(obj, self.ruta, reporthook=self.__call__)
			except:
				urllib.request.urlretrieve(self.url, self.ruta, reporthook=self.__call__)
			wx.CallAfter(self.frame.done, _("La descarga se completó.\n") + _("Ya puede cerrar esta ventana."))
		except:
			wx.CallAfter(self.frame.error, _("Algo salió mal.\n") + _("Compruebe que tiene conexión a internet y vuelva a intentarlo.\n") + _("Ya puede cerrar esta ventana."))
			try:
				os.remove(self.ruta)
			except:
				pass

class HiloLanzaActualizacion(Thread):
	def __init__(self, nombreUrl, listaSeleccion):
		super(HiloLanzaActualizacion, self).__init__()
		self.daemon = True
		self.nombreUrl = nombreUrl
		self.listaSeleccion = listaSeleccion

	def run(self):
		def LanzaDialogo(nombreUrl, listaSeleccion):
			self._MainWindows = ActualizacionDialogo(gui.mainFrame, nombreUrl, listaSeleccion, 15)
			gui.mainFrame.prePopup()
			self._MainWindows.Show()

		wx.CallAfter(LanzaDialogo, self.nombreUrl, self.listaSeleccion)

class HiloActualizacion(Thread):
	def __init__(self, frame, nombreUrl, listaSeleccion, tiempo):
		super(HiloActualizacion, self).__init__()

		self.frame = frame
		self.nombreUrl = nombreUrl
		self.listaSeleccion = listaSeleccion
		self.tiempo = tiempo

		self.directorio = os.path.join(ajustes.dirDatos, "temp")

		self.daemon = True
		self.start()

	def generaFichero(self):
		if os.path.exists(self.directorio) == False:
			os.mkdir(self.directorio)
		nuevoIndex = len(os.listdir(self.directorio))
		return os.path.join(self.directorio, "temp%s.nvda-addon" % nuevoIndex)

	def humanbytes(self, B): # Convierte bytes
		B = float(B)
		KB = float(1024)
		MB = float(KB ** 2) # 1,048,576
		GB = float(KB ** 3) # 1,073,741,824
		TB = float(KB ** 4) # 1,099,511,627,776

		if B < KB:
			return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
		elif KB <= B < MB:
			return '{0:.2f} KB'.format(B/KB)
		elif MB <= B < GB:
			return '{0:.2f} MB'.format(B/MB)
		elif GB <= B < TB:
			return '{0:.2f} GB'.format(B/GB)
		elif TB <= B:
			return '{0:.2f} TB'.format(B/TB)

	def __call__(self, block_num, block_size, total_size):
		readsofar = block_num * block_size
		if total_size > 0:
			percent = readsofar * 1e2 / total_size
			wx.CallAfter(self.frame.onDescarga, percent)
			time.sleep(1 / 995)
			wx.CallAfter(self.frame.TextoRefresco, _("Espere por favor...\n") + _("Descargando: %s") % self.humanbytes(readsofar))
			if readsofar >= total_size: # Si queremos hacer algo cuando la descarga termina.
				pass
		else: # Si la descarga es solo el tamaño
			wx.CallAfter(self.frame.TextoRefresco, _("Espere por favor...\n") + _("Descargando: %s") % self.humanbytes(readsofar))

	def run(self):
		lstError = []
		try:
			for i in self.listaSeleccion:
				fichero = self.generaFichero()
				socket.setdefaulttimeout(self.tiempo)
				req = urllib.request.Request(list(self.nombreUrl.values())[i], headers={'User-Agent': 'Mozilla/5.0'})
				obj = urllib.request.urlopen(req).geturl()
				urllib.request.urlretrieve(obj, fichero, reporthook=self.__call__)
				wx.CallAfter(self.frame.onActualizacion, i+1)
				bundle = addonHandler.AddonBundle(fichero)
				if not addonVersionCheck.hasAddonGotRequiredSupport(bundle):
					pass #Podemos crear un control de errores aquí para complementos que no se pueden instalar por incompatibilidad y luego dar un mensaje
				else:
					if addonHandler.addonVersionCheck.isAddonTested(bundle):
						bundleName = bundle.manifest['name']
						isDisabled = False
						for addon in addonHandler.getAvailableAddons():
							if bundleName == addon.manifest['name']:
								if addon.isDisabled:
									isDisabled = True
								if not addon.isPendingRemove:
									addon.requestRemove()
								break
						addonHandler.installAddonBundle(bundle)
					else:
						lstError.append(bundle.manifest['summary'])
			if len(lstError) == 0:
				ajustes.reiniciarTrue = True
				wx.CallAfter(self.frame.done, _("La actualización se completó.\n") + _("NVDA necesita reiniciarse para aplicar las actualizaciones.\n") + _("¿Desea reiniciar NVDA ahora?"))
			else:
				if len(lstError) == len(self.listaSeleccion):
					wx.CallAfter(self.frame.error, _("No se pudo instalar el complemento.\n") + _("Fallo de compatibilidad.\n") + _("Busque una actualización compatible."))
				else:
					temp = []
					for i in lstError:
						temp.append(i)
					msg = \
_("""Se completo la instalación correctamente.

Pero hay complementos que no se pudieron instalar.

Los siguientes complementos son incompatibles, busque una versión compatible:

{}

NVDA necesita reiniciarse para aplicar las instalaciones.
¿Desea reiniciar NVDA ahora?""").format("\n".join(str(x) for x in temp))
					ajustes.reiniciarTrue = True
					wx.CallAfter(self.frame.done, msg)
		except Exception as e:
			wx.CallAfter(self.frame.error, _("Algo salió mal.\n") + _("Compruebe que tiene conexión a internet y vuelva a intentarlo.\n") + _("Ya puede cerrar esta ventana."))
		try:
			shutil.rmtree(self.directorio, ignore_errors=True)
		except:
			pass

class HiloComplemento(Thread):
	def __init__(self, opcion):
		super(HiloComplemento, self).__init__()
		self.daemon = True
		self.opcion = opcion
	def run(self):
		def tiendaAppDialogo(data):
			self._MainWindows = tiendaApp(gui.mainFrame, data)
			gui.mainFrame.prePopup()
			self._MainWindows.Show()

		def ActualizacionDialogo(nombreUrl, verInstalada, verInstalar):
			self._MainWindows = BuscarActualizacionesDialogo(gui.mainFrame, nombreUrl, verInstalada, verInstalar)
			gui.mainFrame.prePopup()
			self._MainWindows.Show()

		try:
			datos = basedatos.NVDAStoreClient()
			if self.opcion == 1:
				wx.CallAfter(tiendaAppDialogo, datos)
			elif self.opcion == 2:
				nombreUrl, verInstalada, verInstalar = datos.chkActualizaS()
				if nombreUrl == False:
					ajustes.IS_WinON = True
					gui.messageBox(_("No hay actualizaciones."),
						_("Información"), wx.ICON_INFORMATION)
					ajustes.IS_WinON = False
				else:
					wx.CallAfter(ActualizacionDialogo, nombreUrl, verInstalada, verInstalar)
		except:
			msg = \
_("""No se pudo tener acceso al servidor de complementos.

Inténtelo en unos minutos.""")
			gui.messageBox(msg,
				_("Error"), wx.ICON_ERROR)

