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
# Idioma y documentación Turco: umut korkmaz
# Idioma Italiano: Simone Dal Maso
# Idioma Árabe: Wafiq Taher
# Idioma Alemán: Bernd Dorer
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
import config
import core
from scriptHandler import script
from logHandler import log
from gui.settingsDialogs import NVDASettingsDialog, SettingsPanel
from gui import guiHelper, nvdaControls
from tones import beep
import wx
import wx.adv
from threading import Thread
import urllib.request
import socket
import time
import winsound
import shutil
import os
import sys
import traceback
dirAddonPath=os.path.dirname(__file__)
sys.path.append(dirAddonPath)
import traductor
del sys.path[-1]
from . import ajustes
from . import basedatos

# For translation
addonHandler.initTranslation()

inicio = None
chkUpdate = None

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

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()

		if hasattr(globalVars, "tienda"):
			self.postStartupHandler()
		core.postNvdaStartup.register(self.postStartupHandler)
		globalVars.tienda = None

	def postStartupHandler(self):
		hilo = Thread(target=self.tareasDeRed, daemon = True).start()

	def tareasDeRed(self):
		global inicio
		try:
			ajustes.setup()
			inicio = True
		except Exception as e:
			log.info(_("No se pudieron cargar las librerías necesarias para la Tienda"))
			msg = \
_("""Error producido en las librerías::

{}""").format(e)
			log.info(msg)
			exc, type, trace = sys.exc_info()
			traceback.print_exception(exc, type, trace)
			inicio = False

		if inicio:
			global chkUpdate
			if ajustes.tempChk == True:
				chkUpdate = basedatos.RepeatTimer(ajustes.tiempoDict.get(ajustes.tempTimer), function_ChkUpdate)
			NVDASettingsDialog.categoryClasses.append(TiendaPanel)

			self.menu = wx.Menu()
			self.tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
			# Translators: Nombre del submenú para tienda de complementos
			self.tiendaComplementos = self.menu.Append(wx.ID_ANY, _("Listado de complementos"))
			gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_menu1, self.tiendaComplementos)
			# Translators: Nombre del submenú para buscar actualizaciones
			self.tiendaActualizaciones = self.menu.Append(wx.ID_ANY, _("Buscar actualizaciones de complementos"))
			gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_menu2, self.tiendaActualizaciones)
			# Translators: Nombre del submenú para mostrar el manual
			self.tiendaDocumentacion = self.menu.Append(wx.ID_ANY, _("Documentación del complemento"))
			gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_menu3, self.tiendaDocumentacion)
			# Translators: Nombre del menú Tienda de complementos
			self.tiendaMenu = self.tools_menu.AppendSubMenu(self.menu, _("Tienda NVDA.ES"))
		else:
			log.info(_("Inicio del complemento cancelado."))
			return

	def terminate(self):
		global chkUpdate
		try:
			self.tools_menu.Remove(self.tiendaMenu)
		except Exception:
			pass
		try:
			if inicio:
				chkUpdate.stop()
				NVDASettingsDialog.categoryClasses.remove(TiendaPanel)
				core.postNvdaStartup.unregister(self.postStartupHandler)
			if not self._MainWindows:
				self._MainWindows.Destroy()
		except (AttributeError, RuntimeError):
			pass
		super().terminate()

	@script(gesture=None, description= _("Muestra la ventana con todos los complementos y su información"), category= _("Tienda para NVDA.ES"))
	def script_menu1(self, event):
		if inicio:
			if ajustes.reiniciarTrue == False:
				if ajustes.IS_WinON == False:
					self._MainWindows = HiloComplemento(1)
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

	@script(gesture=None, description= _("Busca actualizaciones de los complementos instalados"), category= _("Tienda para NVDA.ES"))
	def script_menu2(self, event):
		if inicio:
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

	def script_menu3(self, event):
		wx.LaunchDefaultBrowser(addonHandler.Addon(os.path.join(os.path.dirname(__file__), "..", "..")).getDocFilePath())

if globalVars.appArgs.secure:
	GlobalPlugin = globalPluginHandler.GlobalPlugin # noqa: F811 

class TiendaPanel(SettingsPanel):
	#TRANSLATORS: title for the Update Channel settings category
	title = _("Tienda NVDA.ES")

	def makeSettings(self, sizer):
		helper=guiHelper.BoxSizerHelper(self, sizer=sizer)

		self.choiceSRV = helper.addLabeledControl(_("Seleccione un servidor de complementos"), wx.Choice, choices=[ajustes.listaServidores[i][0] for i in range(0, len(ajustes.listaServidores))])
		self.choiceSRV.Selection = ajustes.selectSRV
		self.choiceSRV.Bind(wx.EVT_CHOICE, self.onChoiceSRV)

		self.gestionaBTN = helper.addItem (wx.Button (self, label = _("&Gestionar Servidores de complementos")))
		self.gestionaBTN.Bind(wx.EVT_BUTTON, self.onGestiona)

		self.autoChk = helper.addItem(wx.CheckBox(self, label=_("Activar o desactivar la comprobación de actualizaciones")))
		self.autoChk.Bind(wx.EVT_CHECKBOX,self.onAutoChk)

		self.choiceTimer = helper.addLabeledControl(_("Seleccione un tiempo para comprobar si hay actualizaciones"), wx.Choice, choices=ajustes.tiempoChk)

		self.autoLang = helper.addItem(wx.CheckBox(self, label=_("Activar o desactivar el traductor para las descripciones de los complementos")))
		self.autoLang.Bind(wx.EVT_CHECKBOX,self.onAutoLang)

		self.choiceLang = helper.addLabeledControl(_("Seleccione un idioma para traducir las descripciones de los complementos"), wx.Choice, choices=ajustes.langLST)

		self.ordenChk = helper.addItem(wx.CheckBox(self, label=_("Ordenar por orden alfabético los complementos de la tienda y las búsquedas")))

		self.installChk = helper.addItem(wx.CheckBox(self, label=_("Instalar complementos después de descargar")))

		self.datos = basedatos.NVDAStoreClient()
		self.datosServidor = self.datos.dataServidor
		self.listbox = helper.addLabeledControl(_("Complementos instalados que hay en el servidor:"), wx.ListBox)
		if self.datosServidor == None:
			pass
		else:
			if len(ajustes.listaAddonsSave) == 0:
				pass
			else:
				for i in ajustes.listaAddonsSave:
					for x in range(0, len(self.datosServidor)):
						if self.datosServidor[x]['name'].lower() == i[0].lower():
							if i[1] == 9:
								self.listbox.Append("{} -- {}".format(self.datosServidor[x]['summary'], _("Descartar actualizaciones")))
							else:
								self.listbox.Append("{} -- {}".format(self.datosServidor[x]['summary'], self.datosServidor[x]['links'][i[1]]['channel']))

		if self.listbox.GetSelection() == -1:
			pass
		else:
			self.listbox.SetSelection(0)
		self.listbox.Bind(wx.EVT_KEY_UP, self.onListBox)

		self.autoChk.Value = ajustes.tempChk
		if self.autoChk.Value:
			self.choiceTimer.Enable()
		else:
			self.choiceTimer.Disable()

		self.choiceTimer.Selection = ajustes.tempTimer

		self.autoLang.Value = ajustes.tempTrans
		if self.autoLang.Value:
			self.choiceLang.Enable()
		else:
			self.choiceLang.Disable()

		self.choiceLang.Selection = ajustes.tempLang

		self.ordenChk.Value =ajustes.tempOrden

		self.installChk.Value =ajustes.tempInstall

		self.listaOriginal = basedatos.libreriaLocal(ajustes.listaServidores[ajustes.selectSRV][2]).fileJsonAddon(2)
		self.listaGuarda = []
		self.onChoiceSRV(None)

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

		ajustes.tempChk = self.autoChk.Value
		ajustes. tempTimer= self.choiceTimer.Selection
		ajustes.tempTrans = self.autoLang.Value
		ajustes. tempLang= self.choiceLang.Selection
		ajustes.tempOrden = self.ordenChk.Value
		ajustes.tempInstall = self.installChk.Value

		if ajustes.tempChk:
			try:
				chkUpdate.stop()
				ajustes.contadorRepeticion = 0
				ajustes.contadorRepeticionSn = 0
			except:
				pass
			chkUpdate = basedatos.RepeatTimer(ajustes.tiempoDict.get(ajustes.tempTimer), function_ChkUpdate)
			chkUpdate.start()

		if len(self.listaGuarda) == 0:
			pass
		else:
			for i in range(0, len(self.listaGuarda)):
				ajustes.listaAddonsSave[self.listaGuarda[i][0]][1] = self.listaGuarda[i][1]
		basedatos.libreriaLocal(ajustes.listaServidores[ajustes.selectSRV][2]).fileJsonAddon(1, basedatos.libreriaLocal().ordenaLista(ajustes.listaAddonsSave))

	def onPanelActivated(self):
		self.originalProfileName = config.conf.profiles[-1].name
		config.conf.profiles[-1].name = None
		self.Show()

	def onPanelDeactivated(self):
		config.conf.profiles[-1].name = self.originalProfileName
		self.Hide()

#	def postSave(self):
#		a = [x[1] for x in self.listaOriginal]
#		b = [x[1] for x in ajustes.listaAddonsSave]
#		c = [list(i) for i in [(i, a[i], b[i]) for i in range(len(a)) if a[i] != b[i]]]
#		if len(c) == 0:
#			pass
#			print("No hay modificaciones")
#		else:
#			pass
#			print(c)

	def onChoiceSRV(self, event):
		try:
			ajustes.urlServidor = ajustes.listaServidores[self.choiceSRV.Selection][1]
			ajustes.selectSRV = self.choiceSRV.Selection
		except:
			ajustes.urlServidor = ajustes.listaServidores[0][1]
			ajustes.selectSRV = 0

		self.datos = basedatos.NVDAStoreClient()
		self.datosServidor = self.datos.dataServidor
		if self.datosServidor == None:
			self.listbox.Clear()
			self.listbox.Append(_("No se pudo tener acceso al servidor"))
			self.listbox.SetSelection(0)
		else:
			self.listaOriginal = basedatos.libreriaLocal(ajustes.listaServidores[ajustes.selectSRV][2]).fileJsonAddon(2)
			self.listaGuarda = []
			ajustes.listaAddonsSave = basedatos.libreriaLocal(ajustes.listaServidores[ajustes.selectSRV][2]).fileJsonAddon(2)
			self.listbox.Clear()
			if len(ajustes.listaAddonsSave) == 0:
				self.listbox.Append(_("Sin complementos compatibles"))
			else:
				for i in ajustes.listaAddonsSave:
					for x in range(0, len(self.datosServidor)):
						if self.datosServidor[x]['name'].lower() == i[0].lower():
							if i[1] == 9:
								self.listbox.Append("{} -- {}".format(self.datosServidor[x]['summary'], _("Descartar actualizaciones")))
							else:
								self.listbox.Append("{} -- {}".format(self.datosServidor[x]['summary'], self.datosServidor[x]['links'][i[1]]['channel']))
			self.listbox.SetSelection(0)

	def onAutoChk(self, event):
		chk = event.GetEventObject()
		if chk.GetValue():
			self.choiceTimer.Enable()
		else:
			self.choiceTimer.Disable()

	def onAutoLang(self, event):
		chk = event.GetEventObject()
		if chk.GetValue():
			self.choiceLang.Enable()
		else:
			self.choiceLang.Disable()

	def onListBox(self, event):
		if self.listbox.GetString(self.listbox.GetSelection()) == _("Sin complementos compatibles"):
			pass
		else:
			if self.listbox.GetString(self.listbox.GetSelection()) == _("No se pudo tener acceso al servidor"):
				pass
			else:
				nombre = self.listbox.GetString(self.listbox.GetSelection()).split(" -- ")
				nombreLocal = ajustes.listaAddonsSave[self.listbox.GetSelection()][0]
				indice = self.datos.indiceName(nombreLocal)
				datos = self.datosServidor[indice]
				if event.GetKeyCode() == 32: # Pulsamos intro para seleccionar. 32 es espacio.
					self.menuDescarga = wx.Menu()
					for i in range(len(datos['links'])):
						item = self.menuDescarga.Append(i, _("Canal {}").format(datos['links'][i]['channel']))
						self.Bind(wx.EVT_MENU, self.onSelect, item)
					item = self.menuDescarga.Append(9, _("Descartar actualizaciones"))
					self.Bind(wx.EVT_MENU, self.onSelect, item)

					position = self.listbox.GetPosition()
					self.PopupMenu(self.menuDescarga,position)
					pass

	def modificaListBox(self, canalID):
		nombre = self.listbox.GetString(self.listbox.GetSelection()).split(" -- ")
		nombreLocal = ajustes.listaAddonsSave[self.listbox.GetSelection()][0]
		indice = self.datos.indiceName(nombreLocal)
		datos = self.datosServidor[indice]
		if canalID == 9:
			nombreCanal = _("Descartar actualizaciones")
			nombreCompuesto = nombre[0] + " -- " + nombreCanal
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
		if ajustes.IS_WinON:
			msg = \
_("""Ya hay una instancia de la Tienda NVDA abierta.

Para gestionar los servidores es necesario que la Tienda este cerrada.""")
			ui.message(msg)
		else:
			dlg = GestorServidores()
			res = dlg.ShowModal()
			if res == 0:
				dlg.Destroy()
				self.onChoiceSRV(None)
				self.choiceSRV.Clear()
				self.choiceSRV.Append([ajustes.listaServidores[i][0] for i in range(0, len(ajustes.listaServidores))])
				self.choiceSRV.SetSelection(ajustes.selectSRV)
				self.choiceSRV.SetFocus()

class GestorServidores(wx.Dialog):
	def __init__(self):
		super(GestorServidores, self).__init__(None, -1, title=_("Gestor de servidores de complementos"))

		self.SetSize((400, 300))

		self.panel_1 = wx.Panel(self, wx.ID_ANY)

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		label_1 = wx.StaticText(self.panel_1, wx.ID_ANY, _("&Lista de servidores:"))
		sizer_1.Add(label_1, 0, wx.EXPAND, 0)

		self.list_box_1 = wx.ListBox(self.panel_1, wx.ID_ANY, choices=[ajustes.listaServidores[i][0] for i in range(0, len(ajustes.listaServidores))])
		sizer_1.Add(self.list_box_1, 1, wx.EXPAND, 0)
		self.list_box_1.SetSelection(0)

		sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)

		self.añadirBTN = wx.Button(self.panel_1, 101, _("&Añadir"))
		sizer_2.Add(self.añadirBTN, 2, wx.CENTRE, 0)

		self.editarBTN = wx.Button(self.panel_1, 102, _("&Editar"))
		sizer_2.Add(self.editarBTN, 2, wx.CENTRE, 0)

		self.borrarBTN = wx.Button(self.panel_1, 103, _("&Borrar"))
		sizer_2.Add(self.borrarBTN, 2, wx.CENTRE, 0)

		sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_1.Add(sizer_3, 0, wx.EXPAND, 0)

		self.cerrarBTN = wx.Button(self.panel_1, 0, _("&Cerrar"))
		sizer_3.Add(self.cerrarBTN, 2, wx.CENTRE, 0)

		self.panel_1.SetSizer(sizer_1)
		self.Layout()
		self.CenterOnScreen()

		self.inicio()

	def inicio(self):
		self.Bind(wx.EVT_BUTTON,self.onBoton)
		self.Bind(wx.EVT_BUTTON, self.onCerrar, id=self.cerrarBTN.GetId())
		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)
		self.Bind(wx.EVT_CLOSE, self.onCerrar)

	def onBoton(self, event):
		botonID = event.GetEventObject().GetId()
		if botonID == 101: # Añadir
			dlg = AñadirEditar(self, 0)
			res = dlg.ShowModal()
			if res == 0:
				num = len(ajustes.listaServidores) + 1
				ajustes.listaServidores.append([dlg.nombreText.GetValue(), dlg.urlText.GetValue(), "data{}.json".format(num)])
				basedatos.ServidoresComplementos().fileJsonAddon(1, ajustes.listaServidores)
				self.list_box_1.Clear()
				self.list_box_1.Append([ajustes.listaServidores[i][0] for i in range(0, len(ajustes.listaServidores))])
				self.list_box_1.SetSelection(len(ajustes.listaServidores) - 1)
				self.list_box_1.SetFocus()
			dlg.Destroy()
		elif botonID == 102: # Editar
			if self.list_box_1.GetSelection() == 0:
				ui.message(_("El servidor de la comunidad hispanohablante no puede ser editado."))
			else:
				dlg = AñadirEditar(self, 1, ajustes.listaServidores[self.list_box_1.GetSelection()])
				res = dlg.ShowModal()
				if res == 0:
					indice = self.list_box_1.GetSelection()
					ficheroJson = ajustes.listaServidores[indice][2]
					del ajustes.listaServidores[indice]
					ajustes.listaServidores.insert(indice, [dlg.nombreText.GetValue(), dlg.urlText.GetValue(), ficheroJson])
					basedatos.ServidoresComplementos().fileJsonAddon(1, ajustes.listaServidores)
					self.list_box_1.Clear()
					self.list_box_1.Append([ajustes.listaServidores[i][0] for i in range(0, len(ajustes.listaServidores))])
					self.list_box_1.SetSelection(len(ajustes.listaServidores) - 1)
					self.list_box_1.SetFocus()
				dlg.Destroy()
		elif botonID == 103: # borrar
			if self.list_box_1.GetSelection() == 0:
				ui.message(_("El servidor de la comunidad hispanohablante no puede ser borrado."))
			else:
				msg = \
_("""ADVERTENCIA:

Esta acción no es reversible.

Va a borrar el servidor:

{}

¿Esta seguro que desea continuar?""").format(self.list_box_1.GetString(self.list_box_1.GetSelection()))
				MsgBox = wx.MessageDialog(None, msg, _("Pregunta"), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
				ret = MsgBox.ShowModal()
				if ret == wx.ID_YES:
					MsgBox.Destroy
					indice = self.list_box_1.GetSelection()
					ficheroJson = ajustes.listaServidores[indice][2]
					del ajustes.listaServidores[indice]
					basedatos.ServidoresComplementos().fileJsonAddon(1, ajustes.listaServidores)
					try:
						os.remove(os.path.join(globalVars.appArgs.configPath, "TiendaNVDA", ficheroJson))
					except:
						pass
					self.list_box_1.Clear()
					self.list_box_1.Append([ajustes.listaServidores[i][0] for i in range(0, len(ajustes.listaServidores))])
					self.list_box_1.SetSelection(len(ajustes.listaServidores) - 1)
					self.list_box_1.SetFocus()
				else:
					MsgBox.Destroy
					self.list_box_1.SetFocus()

	def onkeyVentanaDialogo(self, event):
		if event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
			if self.IsModal():
				self.EndModal(0)
			else:
				self.Close()
		else:
			event.Skip()

	def onCerrar(self, event):
		if self.IsModal():
			self.EndModal(0)
		else:
			self.Close()

class AñadirEditar(wx.Dialog):
	def __init__(self, frame, opcion, datos=[]):
		super(AñadirEditar, self).__init__(None, -1, title="")

		self.frame = frame
		self.opcion = opcion
		self.datos = datos
		self.SetTitle(_("Añadir servidor")) if self.opcion == 0 else self.SetTitle(_("Editar servidor"))

		self.panel_1 = wx.Panel(self, wx.ID_ANY)

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		label_1 = wx.StaticText(self.panel_1, wx.ID_ANY, _("&Nombre del servidor:"))
		sizer_1.Add(label_1, 0, wx.EXPAND, 0)

		self.nombreText = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
		sizer_1.Add(self.nombreText, 0, wx.EXPAND, 0)

		label_2 = wx.StaticText(self.panel_1, wx.ID_ANY, _("&URL del servidor:"))
		sizer_1.Add(label_2, 0, wx.EXPAND, 0)

		self.urlText = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
		sizer_1.Add(self.urlText, 0, wx.EXPAND, 0)

		sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)

		self.aceptarBTN = wx.Button(self.panel_1, 0, _("&Aceptar"))
		sizer_2.Add(self.aceptarBTN, 2, wx.CENTER, 0)

		self.cancelarBTN = wx.Button(self.panel_1, 1, _("&Cancelar"))
		sizer_2.Add(self.cancelarBTN, 2, wx.CENTER, 0)

		self.panel_1.SetSizer(sizer_1)

		self.Layout()
		self.CenterOnScreen()

		self.inicio()

	def inicio(self):
		self.nombreText.Bind(wx.EVT_CONTEXT_MENU, self.skip)
		self.urlText.Bind(wx.EVT_CONTEXT_MENU, self.skip)
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.aceptarBTN.GetId())
		self.Bind(wx.EVT_BUTTON, self.onCancelar, id=self.cancelarBTN.GetId())
		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)
		self.Bind(wx.EVT_CLOSE, self.onCancelar)
		if self.opcion == 1:
			self.nombreText.SetValue(self.datos[0])
			self.urlText.SetValue(self.datos[1])

	def onAceptar(self, event):
		if self.nombreText.GetValue() == "":
			msg = \
_("""El campo de nombre de servidor no puede quedar en blanco.

Introduzca uno para poder continuar.""")
			ui.message(msg)
			self.nombreText.SetFocus()
		else:
			if self.urlText.GetValue() == "":
				msg = \
_("""El campo de URL de servidor no puede quedar en blanco.

Introduzca uno para poder continuar.""")
				ui.message(msg)
				self.urlText.SetFocus()
			else:
				if basedatos.estaenlistado([ajustes.listaServidores[i][0] for i in range(0, len(ajustes.listaServidores))], self.nombreText.GetValue()):
					msg = \
_("""Ya tiene un servidor con el mismo nombre.

Modifique el nombre del servidor para poder continuar.""")
					ui.message(msg)
					self.nombreText.SetFocus()
				else:
					if basedatos.chkJson(self.urlText.GetValue()) == False:
						msg = \
_("""La URL introducida dio error.

Compruebe que es una URL correcta de base de datos de complementos.""")
						ui.message(msg)
						self.urlText.SetFocus()
					else:
						if self.IsModal():
							self.EndModal(0)
						else:
							self.Close()

	def skip(self, event):
		return

	def onkeyVentanaDialogo(self, event):
		if event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
			if self.IsModal():
				self.EndModal(1)
			else:
				self.Close()
		else:
			event.Skip()

	def onCancelar(self, event):
		if self.IsModal():
			self.EndModal(1)
		else:
			self.Close()

class SinComplementos(wx.Dialog):
	def __init__(self, parent):

		WIDTH = 450
		HEIGHT = 150

		super(SinComplementos,self).__init__(parent, -1, title=_("Servidor sin complementos"), size = (WIDTH, HEIGHT))

		ajustes.IS_WinON = True
		self.choiceSelection = 0
		self.resultados = []
		for i in range(len(ajustes.listaServidores)):
			self.resultados.append("{}".format(ajustes.listaServidores[i][0]))

		self.Panel = wx.Panel(self)
		self.choice = wx.Choice(self.Panel, wx.ID_ANY, choices =[_("Seleccione un servidor")] + self.resultados)
		self.choice.SetSelection(self.choiceSelection)
		self.choice.Bind(wx.EVT_CHOICE, self.onChoiceApp)
		#Translators: etiqueta del botón aceptar
		self.aceptarBTN = wx.Button(self.Panel, wx.ID_ANY, _("&Aceptar"))
		self.aceptarBTN.Bind(wx.EVT_BUTTON, self.onAceptar)
		#Translators: etiqueta del botón cancelar
		self.cerrarBTN = wx.Button(self.Panel, wx.ID_CANCEL, _("&Cerrar"))
		self.cerrarBTN.Bind(wx.EVT_BUTTON, self.close, id=wx.ID_CANCEL)

		sizerV = wx.BoxSizer(wx.VERTICAL)
		sizerH = wx.BoxSizer(wx.HORIZONTAL)

		sizerV.Add(self.choice, 0, wx.EXPAND | wx.ALL)

		sizerH.Add(self.aceptarBTN, 2, wx.CENTER)
		sizerH.Add(self.cerrarBTN, 2, wx.CENTER)

		sizerV.Add(sizerH, 0, wx.CENTER)

		self.Panel.SetSizer(sizerV)

		self.CenterOnScreen()

	def onChoiceApp(self, event):
		#Translators: título de selección de aplicación
		if self.choice.GetString(self.choice.GetSelection()) == _("Seleccione un servidor"):
			self.choiceSelection = 0
		else:
			self.choiceSelection = event.GetSelection()

	def onAceptar(self, event):
		if self.choiceSelection == 0:
			gui.messageBox(_("Debe seleccionar un servidor para continuar."), _("Información"), wx.ICON_INFORMATION)
			self.choice.SetFocus()
		else:
			ajustes.IS_WinON = False
			ajustes.selectSRV = self.choiceSelection - 1
			ajustes.urlServidor = ajustes.listaServidores[ajustes.selectSRV][1]
			ajustes.setConfig("urlServidor", ajustes.listaServidores[ajustes.selectSRV][1])
			ajustes.setConfig("selectSRV", ajustes.selectSRV)
			ajustes.listaAddonsSave = basedatos.libreriaLocal(ajustes.listaServidores[ajustes.selectSRV][2]).fileJsonAddon(2)
			self.Destroy()
			gui.mainFrame.postPopup()
			self._MainWindows = HiloComplemento(1)
			self._MainWindows.start()

	def close(self, event):
		ajustes.IS_WinON = False
		self.Destroy()
		gui.mainFrame.postPopup()

class tiendaApp(wx.Dialog):
	def __init__(self, parent, dataServidor):

		WIDTH = 1600
		HEIGHT = 800

		super(tiendaApp,self).__init__(parent, -1, title=ajustes.titulo, size = (WIDTH, HEIGHT))

		ajustes.IS_WinON = True
		self.datos = dataServidor
		self.indiceFiltro = ajustes.indiceFiltro
		self.temporal = []
		self.dirDoc = None

		self.Panel = wx.Panel(self, 1)

		labelBusqueda = wx.StaticText(self.Panel, wx.ID_ANY, _("&Buscar:"))
		self.textoBusqueda = wx.TextCtrl(self.Panel, 2,style = wx.TE_PROCESS_ENTER)
		self.textoBusqueda.Bind(wx.EVT_TEXT_ENTER, self.onBusqueda)
		self.textoBusqueda.Bind(wx.EVT_CONTEXT_MENU, self.skip)

		self.buscarBTN = wx.Button(self.Panel, 201, _("B&uscar"))

		labelComplementos = wx.StaticText(self.Panel, wx.ID_ANY, _("&Lista complementos:"))
		self.listboxComplementos = wx.ListBox(self.Panel, 3, style = wx.LB_NO_SB)
		wx.CallAfter(self.onCargaFiltro, self.indiceFiltro)
		self.listboxComplementos.Bind(wx.EVT_KEY_UP, self.onLisbox)
		self.listboxComplementos.Bind(wx.EVT_CONTEXT_MENU, self.menuListBox)

		self.accionBTN = wx.Button(self.Panel, 202, _("&Acción"))

		labelResultado = wx.StaticText(self.Panel, wx.ID_ANY, _("&Información:"))
		self.txtResultado = wx.TextCtrl(self.Panel, 4, style =wx.TE_MULTILINE|wx.TE_READONLY|wx.LB_NO_SB)
		self.txtResultado.Bind(wx.EVT_CONTEXT_MENU, self.skip)
		self.txtResultado.Bind(wx.EVT_KEY_UP, self.ontxtResultado)

		self.descargarBTN = wx.Button(self.Panel, 203, _("&Descargar complemento"))
		self.paginaWebBTN = wx.Button(self.Panel, 204, _("Visitar &página WEB"))
		self.cambiarSrvBTN = wx.Button(self.Panel, 205, _("&Cambiar de servidor"))
		self.salirBTN = wx.Button(self.Panel, 206, _("&Salir"))
		self.Bind(wx.EVT_BUTTON,self.onBoton)
		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)
		self.Bind(wx.EVT_CLOSE, self.onBoton)

		szMain = wx.BoxSizer(wx.HORIZONTAL)
		szComplementos = wx.BoxSizer(wx.VERTICAL)
		szResultados = wx.BoxSizer(wx.VERTICAL)
		szBotones = wx.BoxSizer(wx.HORIZONTAL)

		szComplementos.Add(labelBusqueda, 0)
		szComplementos.Add(self.textoBusqueda, 0, wx.EXPAND)
		szComplementos.Add(self.buscarBTN, 0, wx.EXPAND)
		szComplementos.Add(labelComplementos, 0)
		szComplementos.Add(self.listboxComplementos, 1, wx.EXPAND)
		szComplementos.Add(self.accionBTN, 0, wx.EXPAND)

		szResultados.Add(labelResultado, 0)
		szResultados.Add(self.txtResultado, 1, wx.EXPAND)

		szBotones.Add(self.descargarBTN, 2, wx.CENTRE)
		szBotones.Add(self.paginaWebBTN, 2, wx.CENTRE)
		szBotones.Add(self.cambiarSrvBTN, 2, wx.CENTRE)
		szBotones.Add(self.salirBTN, 2, wx.CENTRE)

		szResultados.Add(szBotones, 0, wx.EXPAND)

		szMain.Add(szComplementos, 0, wx.EXPAND)
		szMain.Add(szResultados, 1, wx.EXPAND)

		self.Panel.SetSizer(szMain)

		self.onLisbox(None)
#		self.onFocus()

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

	def onFichaTrans(self):
		beep(400,150)
		nombre = self.listboxComplementos.GetString(self.listboxComplementos.GetSelection())
		indice = self.datos.indiceSummary(nombre)
		datos = self.datos.dataServidor[indice]
		if ajustes.tempTrans:
			try:
				traducir = traductor.translate(datos['description'], ajustes.langDict.get(ajustes.tempLang))
			except:
				ui.message(_("No se pudo traducir la descripción"))
				traducir =datos['description']
		else:
			traducir =datos['description']

		ficha = \
_("""Autor: {}
Nombre del complemento: {}
Nombre interno: {}
Descripción: {}
Desarrollo: {}\n""").format(
	datos['author'],
	datos['summary'],
	datos['name'],
	traducir,
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
		beep(100,150)

	def onFocus(self):
		self.Bind(wx.EVT_ACTIVATE, self.onSetFocus)
		self.textoBusqueda.Bind(wx.EVT_SET_FOCUS, self.onSetSelection)
		self.listboxComplementos.Bind(wx.EVT_SET_FOCUS, self.onSetSelection)
		self.txtResultado.Bind(wx.EVT_SET_FOCUS, self.onSetSelection)
		self.descargarBTN.Bind(wx.EVT_SET_FOCUS, self.onSetSelection)
		self.paginaWebBTN.Bind(wx.EVT_SET_FOCUS, self.onSetSelection)
		self.cambiarSrvBTN.Bind(wx.EVT_SET_FOCUS, self.onSetSelection)
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

	def menuListBox(self, event):
		nombre = self.listboxComplementos.GetString(self.listboxComplementos.GetSelection())
		indice = self.datos.indiceSummary(nombre)
		datos = self.datos.dataServidor[indice]
		self.menu = wx.Menu()

		self.menuFiltro = wx.Menu()
		item1 = self.menuFiltro.Append(6, _("Mostrar todos los complementos"))
		self.Bind(wx.EVT_MENU, self.onCargaFiltro, item1)
		item2 = self.menuFiltro.Append(7, _("Mostrar los complementos con compatibilidad de API 2023"))
		self.Bind(wx.EVT_MENU, self.onCargaFiltro, item2)
		item3 = self.menuFiltro.Append(8, _("Mostrar los complementos con compatibilidad de API 2022"))
		self.Bind(wx.EVT_MENU, self.onCargaFiltro, item3)
		item4 = self.menuFiltro.Append(9, _("Mostrar los complementos ordenados por autor"))
		self.Bind(wx.EVT_MENU, self.onCargaFiltro, item4)
		item5 = self.menuFiltro.Append(10, _("Mostrar por descargas de mayor a menor"))
		self.Bind(wx.EVT_MENU, self.onCargaFiltro, item5)
		self.menu.AppendSubMenu(self.menuFiltro, _("&Filtros"))

		self.menuPortapapeles = wx.Menu()
		item6 = self.menuPortapapeles.Append(11, _("Copiar información"))
		self.Bind(wx.EVT_MENU, self.onPortapapeles, item6)
		item7 = self.menuPortapapeles.Append(12, _("Copiar enlace a la página web del complemento"))
		self.Bind(wx.EVT_MENU, self.onPortapapeles, item7)
		self.menuPortapapelesDescarga = wx.Menu()
		for i in range(len(datos['links'])):
			itemx = self.menuPortapapelesDescarga.Append(i, _("Canal {}").format(datos['links'][i]['channel']))
			self.Bind(wx.EVT_MENU, self.onPortapapeles, itemx)
		self.menuPortapapeles.AppendSubMenu(self.menuPortapapelesDescarga, _("Copiar enlace de descarga del complemento"))
		self.menu.AppendSubMenu(self.menuPortapapeles, _("&Copiar al portapapeles"))

		for i in self.datos.dataLocal:
			if datos['name'].lower() == i.name.lower():
				self.dirDoc = addonHandler.Addon(i.path).getDocFilePath()
				if self.dirDoc:
					itemDoc = self.menu.Append(20, _("Ver documentación del complemento instalado"))
					self.Bind(wx.EVT_MENU, self.onDocumentacion, itemDoc)

		position = self.listboxComplementos.GetPosition()
		self.PopupMenu(self.menu,position)
#		pass

	def onBusqueda(self, event):
		if self.textoBusqueda.GetValue() == "":
			self.listboxComplementos.Clear()
			if self.indiceFiltro == 6:
				if ajustes.tempOrden == False:
					self.listboxComplementos.Append(self.temporal)
				else:
					self.listboxComplementos.Append(sorted(self.temporal, key=str.lower))
			elif self.indiceFiltro == 7:
				if ajustes.tempOrden == False:
					self.listboxComplementos.Append(self.temporal)
				else:
					self.listboxComplementos.Append(sorted(self.temporal, key=str.lower))
			elif self.indiceFiltro == 8:
				if ajustes.tempOrden == False:
					self.listboxComplementos.Append(self.temporal)
				else:
					self.listboxComplementos.Append(sorted(self.temporal, key=str.lower))
			else:
				self.listboxComplementos.Append(self.temporal)
			self.listboxComplementos.SetSelection(0)
			self.listboxComplementos.SetFocus()
		else:
			pattern = self.textoBusqueda.GetValue()
			filtro = [item for item in self.temporal if pattern.lower() in item.lower()]
			self.listboxComplementos.Clear()
			if len(filtro) == 0:
				self.listboxComplementos.Append(_("No se encontraron resultados"))
				self.listboxComplementos.SetSelection(0)
				self.listboxComplementos.SetFocus()
			else:
				if self.indiceFiltro == 6 or self.indiceFiltro == 7 or self.indiceFiltro == 8:
					if ajustes.tempOrden == False:
						self.listboxComplementos.Append(filtro)
					else:
						self.listboxComplementos.Append(sorted(filtro, key=str.lower))
				else:
					self.listboxComplementos.Append(filtro)
				self.listboxComplementos.SetSelection(0)
				self.listboxComplementos.SetFocus()

	def onCargaFiltro (self, event):
		try:
			indice = event.GetId()
		except:
			indice = event
		self.indiceFiltro =indice
		ajustes.indiceFiltro = indice
		del self.temporal[:]
		self.listboxComplementos.Clear()
		self.textoBusqueda.Clear()
		if self.indiceFiltro == 6:
			self.SetTitle(ajustes.titulo + _(" - Todos los complementos"))
			for x in range(0, len(self.datos.dataServidor)):
				self.temporal.append(self.datos.dataServidor[x]['summary'])
			if ajustes.tempOrden == False:
				self.listboxComplementos.Append(self.temporal)
			else:
				self.listboxComplementos.Append(sorted(self.temporal, key=str.lower))
		if self.indiceFiltro == 7:
			self.SetTitle(ajustes.titulo + _(" - Complementos compatibles con API 2023"))
			dataserver = [x for x in self.datos.dataServidor if x['links'][0]['lasttested'].split('.')[0] == "2023"]
			for x in range(0, len(dataserver)):
					self.temporal.append(dataserver[x]['summary'])
			if ajustes.tempOrden == False:
				self.listboxComplementos.Append(self.temporal)
			else:
				self.listboxComplementos.Append(sorted(self.temporal, key=str.lower))

		if self.indiceFiltro == 8:
			self.SetTitle(ajustes.titulo + _(" - Complementos compatibles con API 2022"))
			dataserver = [x for x in self.datos.dataServidor if x['links'][0]['lasttested'].split('.')[0] == "2022"]
			for x in range(0, len(dataserver)):
					self.temporal.append(dataserver[x]['summary'])
			if ajustes.tempOrden == False:
				self.listboxComplementos.Append(self.temporal)
			else:
				self.listboxComplementos.Append(sorted(self.temporal, key=str.lower))
		if self.indiceFiltro == 9:
			self.SetTitle(ajustes.titulo + _(" - Complementos por autor"))
			dataserver = sorted(self.datos.dataServidor, key=lambda k: k.get('author', 0), reverse=False)

			for x in range(0, len(dataserver)):
				self.temporal.append(dataserver[x]['summary'])
			self.listboxComplementos.Append(self.temporal)
		if self.indiceFiltro == 10:
			self.SetTitle(ajustes.titulo + _(" - Complementos por descarga de mayor a menor"))
			dataserver = sorted(self.datos.dataServidor, key=lambda k: k['links'][0].get('downloads', 0), reverse=True)
			for x in range(0, len(dataserver)):
				self.temporal.append(dataserver[x]['summary'])
			self.listboxComplementos.Append(self.temporal)

		self.listboxComplementos.SetSelection(0)
		self.listboxComplementos.SetFocus()
		self.onLisbox(None)

	def onPortapapeles(self, event):
		nombre = self.listboxComplementos.GetString(self.listboxComplementos.GetSelection())
		indice = self.datos.indiceSummary(nombre)
		datos = self.datos.dataServidor[indice]
		if event.GetId() == 6 or event.GetId() == 7 or event.GetId() == 8 or event.GetId() == 9 or event.GetId() == 10:
			self.onCargaFiltro(event.GetId())
		elif event.GetId() == 11:
			msg = \
_("""Se copio la información del complemento al portapapeles""")
			self.onCopiaPortapapeles(msg, self.txtResultado.GetValue())
		elif event.GetId() == 12:
			msg = \
_("""Se copio la URL de la página oficial del complemento al portapapeles""")
			self.onCopiaPortapapeles(msg, datos['url'])
		else:
			msg = \
_("""Se copio la URL de descarga al portapapeles""")
			self.onCopiaPortapapeles(msg, "{}{}".format(self.datos.urlBase, datos['links'][event.GetId()]['file']))

	def onCopiaPortapapeles(self, msg, valor):
		self.dataObj = wx.TextDataObject()
		self.dataObj.SetText(valor)
		if wx.TheClipboard.Open():
			wx.TheClipboard.SetData(self.dataObj)
			wx.TheClipboard.Flush()
			# Translators: Title of the notification
			notify = wx.adv.NotificationMessage(title=_("Información"),
				# Translators: Notification message
				message=msg, parent=None, flags=wx.ICON_INFORMATION)
			notify.Show(timeout=10)
		else:
			# Translators: Title of the notification
			notify = wx.adv.NotificationMessage(title=_("Error"),
				# Translators: Notification message
				message=_("No se pudo llevar a cabo la copia al portapapeles"), parent=None, flags=wx.ICON_ERROR)
			notify.Show(timeout=10)

	def onDocumentacion(self, event):
		wx.LaunchDefaultBrowser('file://' + self.dirDoc, flags=0)

	def onLisbox(self, event):
		try:
			tecla = event.GetKeyCode()
		except:
			tecla = None
		if self.listboxComplementos.GetSelection() == -1:
			pass
		else:
			if self.listboxComplementos.GetString(self.listboxComplementos.GetSelection()) == _("No se encontraron resultados"):
				self.txtResultado.Clear()
			else:
				if tecla == wx.WXK_F1:
					msg = \
_("""Se encuentra en el complemento {} de {}""").format(self.listboxComplementos.GetSelection()+1, self.listboxComplementos.GetCount())
					ui.message(msg)
				else:
					if tecla == wx.WXK_F2:
						ui.message(self.txtResultado.GetValue())
					else:
						if tecla == wx.WXK_F3:
							msg = \
_("""No tiene activada la opción traducir la descripción de complementos en opciones de la tienda.

Active dicha opción y elija un idioma para poder usar esta característica.""")
							self.onFichaTrans() if ajustes.tempTrans else ui.message(msg)
						else:
							self.onFicha()

	def ontxtResultado(self, event):
		tecla = event.GetKeyCode()
		if tecla == wx.WXK_F3:
			msg = \
_("""No tiene activada la opción traducir la descripción de complementos en opciones de la tienda.

Active dicha opción y elija un idioma para poder usar esta característica.""")
			self.onFichaTrans() if ajustes.tempTrans else ui.message(msg)
		else:
			event.Skip()

	def onBoton(self, event):
		obj = event.GetEventObject()
		botonID = obj.GetId()
		nombre = self.listboxComplementos.GetString(self.listboxComplementos.GetSelection())
		indice = self.datos.indiceSummary(nombre)
		datos = self.datos.dataServidor[indice]
		if botonID == 201:
			self.onBusqueda(None)
		elif botonID == 202:
			self.menuListBox(None)
		elif botonID == 203:
			self.menuDescarga = wx.Menu()

			for i in range(len(datos['links'])):
				item = self.menuDescarga.Append(i, _("Versión {}").format(datos['links'][i]['channel']))
				self.Bind(wx.EVT_MENU, self.onDescarga, item)

			position = self.descargarBTN.GetPosition()
			self.PopupMenu(self.menuDescarga,position)
			pass

		elif botonID == 204:
			wx.LaunchDefaultBrowser(datos['url'])
		elif botonID == 205:
			self.menu = wx.Menu()
			for i in range(len(ajustes.listaServidores)):
				i = self.menu.Append(i, "{}".format(ajustes.listaServidores[i][0]), "", wx.ITEM_CHECK)
			self.menu.Bind(wx.EVT_MENU_RANGE, self.onCambiarSRV, id=0, id2=len(ajustes.listaServidores)-1)
			self.menu.Check(ajustes.selectSRV, True)
			self.cambiarSrvBTN.PopupMenu(self.menu)

		elif botonID == 206:
			if ajustes.IS_Download == False:
				ajustes.IS_WinON = False
			else:
				ajustes.IS_TEMPORAL = True
			ajustes.focoActual = "listboxComplementos"
			self.Destroy()
			gui.mainFrame.postPopup()
		else:
			if ajustes.IS_Download == False:
				ajustes.IS_WinON = False
			else:
				ajustes.IS_TEMPORAL = True
			ajustes.focoActual = "listboxComplementos"
			self.Destroy()
			gui.mainFrame.postPopup()

	def onCambiarSRV(self, event):
		ajustes.selectSRV = event.GetId()
		ajustes.urlServidor = ajustes.listaServidores[ajustes.selectSRV][1]
		ajustes.setConfig("urlServidor", ajustes.listaServidores[event.GetId()][1])
		ajustes.setConfig("selectSRV", event.GetId())
		ajustes.listaAddonsSave = basedatos.libreriaLocal(ajustes.listaServidores[ajustes.selectSRV][2]).fileJsonAddon(2)
		if ajustes.IS_Download == False:
			ajustes.IS_WinON = False
		else:
			ajustes.IS_TEMPORAL = True
			ajustes.focoActual = "listboxComplementos"
		self.Destroy()
		gui.mainFrame.postPopup()
		self._MainWindows = HiloComplemento(1)
		self._MainWindows.start()

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
				self.onSetFocus(None)
			except:
				ajustes.IS_Download = False
				ajustes.IS_WinON = False
				ajustes.IS_TEMPORAL = False
				pass
			dlg.Destroy()
		else:
			try:
				ajustes.IS_Download = False
				self.onSetFocus(None)
			except:
				ajustes.IS_Download = False
				ajustes.IS_WinON = False
				ajustes.IS_TEMPORAL = False
				pass
			dlg.Destroy()

	def FalseDescarga(self):
		try:
			ajustes.IS_Download = False
			self.onSetFocus(None)
			pass
		except:
			ajustes.IS_Download = False
			ajustes.IS_WinON = False
			ajustes.IS_TEMPORAL = False
			pass

	def onkeyVentanaDialogo(self, event):
		if event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
			if ajustes.IS_Download == False:
				ajustes.IS_WinON = False
			else:
				ajustes.IS_TEMPORAL = True
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
			ajustes.contadorRepeticion = 0
			ajustes.contadorRepeticionSn = 0

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

		self.Panel = wx.Panel(self)

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

		self.download_thread = Thread(target=self.descargaActualizaciones, daemon = True).start()

		self.textorefresco.SetFocus()

	def skip(self, event):
		return

	def onNull(self, event):
		pass

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

	def descargaActualizaciones(self):
		try:
			socket.setdefaulttimeout(self.seconds) # Dara error si pasan 30 seg sin internet

			req = urllib.request.Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
			try:
				obj = urllib.request.urlopen(req)
			except:
				req = urllib.request.Request(self.url, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
				obj = urllib.request.urlopen(req)

			total_size = int(obj.headers.get('Content-Length'))
			if total_size >= 10000000:
				wx.CallAfter(self.TextoRefresco, _("Espere por favor...\n") + _("Descargando Un complemento grande..."))
				descargado = 0
				with urllib.request.urlopen(req) as obj, open(self.file, 'wb') as f:
					buffer = obj.read(8192)
					while buffer:
						f.write(buffer)
						descargado += len(buffer)
						progress = (descargado / total_size) * 100
						wx.CallAfter(self.next, int(progress))
						buffer = obj.read(8192)
					obj.close()
			else:
				descargado = 0
				with open(self.file, 'wb') as f:
					buffer = obj.read(8192)
					while buffer:
						f.write(buffer)
						descargado += len(buffer)
						progress = (descargado / total_size) * 100
						wx.CallAfter(self.next, int(progress))
						wx.CallAfter(self.TextoRefresco, _("Espere por favor...\n") + _("Descargando: %s") % self.humanbytes(descargado))
						buffer = obj.read(8192)
					obj.close()

			wx.CallAfter(self.done, _("La descarga se completó.\n") + _("Ya puede cerrar esta ventana."))
		except Exception as e:
			wx.CallAfter(self.error, _("Algo salió mal.\n") + _("Compruebe que tiene conexión a internet y vuelva a intentarlo.\n") + _("Error:\n\n{}\n").format(e) + _("Ya puede cerrar esta ventana."))
			try:
				os.remove(self.file)
			except:
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
		self.directorio = os.path.join(ajustes.dirDatos, "temp")

		self.Panel = wx.Panel(self)

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

		self.download_thread = Thread(target=self.descargaActualizaciones, daemon = True).start()
		self.textorefresco.SetFocus()

	def skip(self, event):
		return

	def onNull(self, event):
		pass

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

	def descargaActualizaciones(self):
		lstError = []
		try:
			for i in self.listaSeleccion:
				fichero = self.generaFichero()
				socket.setdefaulttimeout(self.seconds)
				req = urllib.request.Request(list(self.nombreUrl.values())[i], headers={'User-Agent': 'Mozilla/5.0'})
				try:
					obj = urllib.request.urlopen(req)
				except:
					req = urllib.request.Request(list(self.nombreUrl.values())[i], headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
					obj = urllib.request.urlopen(req)

				total_size = int(obj.headers.get('Content-Length'))
				if total_size >= 10000000:
					wx.CallAfter(self.TextoRefresco, _("Espere por favor...\n") + _("Descargando Un complemento grande..."))
					descargado = 0
					with urllib.request.urlopen(req) as obj, open(fichero, 'wb') as f:
						buffer = obj.read(8192)
						while buffer:
							f.write(buffer)
							descargado += len(buffer)
							progress = (descargado / total_size) * 100
							wx.CallAfter(self.onDescarga, int(progress))
							buffer = obj.read(8192)
						obj.close()
				else:
					descargado = 0
					with open(fichero, 'wb') as f:
						buffer = obj.read(8192)
						while buffer:
							f.write(buffer)
							descargado += len(buffer)
							progress = (descargado / total_size) * 100
							wx.CallAfter(self.onDescarga, int(progress))
							wx.CallAfter(self.TextoRefresco, _("Espere por favor...\n") + _("Descargando: %s") % self.humanbytes(descargado))
							buffer = obj.read(8192)
						obj.close()

				wx.CallAfter(self.onActualizacion, i+1)
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
				wx.CallAfter(self.done, _("La actualización se completó.\n") + _("NVDA necesita reiniciarse para aplicar las actualizaciones.\n") + _("¿Desea reiniciar NVDA ahora?"))
			else:
				if len(lstError) == len(self.listaSeleccion):
					wx.CallAfter(self.error, _("No se pudo instalar el complemento.\n") + _("Fallo de compatibilidad.\n") + _("Busque una actualización compatible."))
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
					wx.CallAfter(self.done, msg)
		except Exception as e:
			wx.CallAfter(self.error, _("Algo salió mal.\n") + _("Compruebe que tiene conexión a internet y vuelva a intentarlo.\n") + _("Ya puede cerrar esta ventana."))
		try:
			shutil.rmtree(self.directorio, ignore_errors=True)
		except:
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
			winsound.PlaySound('C:\\Windows\\Media\\Windows Proximity Connection.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
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
							ajustes.IS_Download = False
							if ajustes.IS_TEMPORAL == True:
								ajustes.IS_WinON = False
								ajustes.IS_TEMPORAL = False
							wx.LaunchDefaultBrowser(self.url)
							return
		if self.nombreFile == "downloads":
			winsound.PlaySound(None, winsound.SND_PURGE)
			msg = \
_("""Este complemento necesita ser descargado desde su página web.

Se abrirá con su navegador predefinido en la pagina de descarga del complemento.""")
			gui.messageBox(msg,
				_("Información"), wx.ICON_INFORMATION)
			ajustes.IS_Download = False
			if ajustes.IS_TEMPORAL == True:
				ajustes.IS_WinON = False
				ajustes.IS_TEMPORAL = False
			wx.LaunchDefaultBrowser(datos['links'][self.id]['link'])
			return
		else:
			if self.nombreFile == None:
				winsound.PlaySound(None, winsound.SND_PURGE)
				msg = \
_("""No se pudo obtener el nombre del archivo a descargar.

{} del canal {}

Se va a proceder a descargar con su navegador predefinido.""").format(nombre, datos['links'][self.id]['channel'])
				gui.messageBox(msg,
					_("Información"), wx.ICON_INFORMATION)
				self.nombreFile = ""
				ajustes.IS_Download = False
				if ajustes.IS_TEMPORAL == True:
					ajustes.IS_WinON = False
					ajustes.IS_TEMPORAL = False
				wx.LaunchDefaultBrowser(self.url)
				return

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
						ajustes.IS_Download = False
						if ajustes.IS_TEMPORAL == True:
							ajustes.IS_WinON = False
							ajustes.IS_TEMPORAL = False
						wx.LaunchDefaultBrowser(self.url)
						return

		if self.nombreFile == None:
			winsound.PlaySound(None, winsound.SND_PURGE)
			msg = \
_("""No se pudo obtener el nombre del archivo a descargar.

{} del canal {}

Se va a proceder a descargar con su navegador predefinido.""").format(nombre, datos['links'][self.id]['channel'])
			gui.messageBox(msg,
				_("Información"), wx.ICON_INFORMATION)
			self.nombreFile = ""
			ajustes.IS_Download = False
			if ajustes.IS_TEMPORAL == True:
				ajustes.IS_WinON = False
				ajustes.IS_TEMPORAL = False
			wx.LaunchDefaultBrowser(self.url)
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

class HiloComplemento(Thread):
	def __init__(self, opcion):
		super(HiloComplemento, self).__init__()

		self.opcion = opcion
		self.daemon = True

	def run(self):
		def tiendaAppDialogo(data):
			if len(data.dataServidor) == 0:
				self._MainWindows = SinComplementos(gui.mainFrame)
				gui.mainFrame.prePopup()
				self._MainWindows.Show()
			else:
				self._MainWindows = tiendaApp(gui.mainFrame, data)
				gui.mainFrame.prePopup()
				self._MainWindows.Show()

		def ActualizacionDialogo(nombreUrl, verInstalada, verInstalar):
			self._MainWindows = BuscarActualizacionesDialogo(gui.mainFrame, nombreUrl, verInstalada, verInstalar)
			gui.mainFrame.prePopup()
			self._MainWindows.Show()

		def OtroServidor():
			self._MainWindows = SinComplementos(gui.mainFrame)
			gui.mainFrame.prePopup()
			self._MainWindows.Show()

		try:
			datos = basedatos.NVDAStoreClient()
			if datos.dataServidor == None:
				msg = \
_("""No se pudo tener acceso al servidor de complementos.

Inténtelo en unos minutos.

¿Desea no obstante intentar cambiar de servidor?""")
				MsgBox = wx.MessageDialog(None, msg, _("Pregunta"), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
				ret = MsgBox.ShowModal()
				if ret == wx.ID_YES:
					MsgBox.Destroy
					wx.CallAfter(OtroServidor)

				else:
					MsgBox.Destroy
			else:
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
		except Exception as e:
			msg = \
_("""No se pudo tener acceso al servidor de complementos.

Inténtelo en unos minutos.""")
			gui.messageBox(msg,
				_("Error"), wx.ICON_ERROR)
			exc, type, trace = sys.exc_info()
			traceback.print_exception(exc, type, trace)

