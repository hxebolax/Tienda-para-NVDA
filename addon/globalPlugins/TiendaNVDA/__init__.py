# -*- coding: utf-8 -*-
# Copyright (C) 2020 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

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
import wx
import webbrowser
from threading import Thread
import urllib.request
import socket
import time
import winsound
import shutil
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ajustes
import basedatos
import funciones

# For translation
addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()

		if globalVars.appArgs.secure:
			return

		self.menu = wx.Menu()
		tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
		# Translators: Nombre del submenú para tienda de complementos
		self.tiendaComplementos = self.menu.Append(wx.ID_ANY, _("Listado de complementos"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_menu1, self.tiendaComplementos)
		# Translators: Nombre del submenú para buscar actualizaciones
		self.tiendaActualizaciones = self.menu.Append(wx.ID_ANY, _("Buscar actualizaciones de complementos"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_menu2, self.tiendaActualizaciones)
		# Translators: Nombre del submenú opciones
		self.tiendaOpciones = self.menu.Append(wx.ID_ANY, _("Opciones"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.menu3, self.tiendaOpciones)
		# Translators: Nombre del menú Tienda de complementos
		self.tiendaMenu = tools_menu.AppendSubMenu(self.menu, _("Tienda NVDA"))

	def terminate(self):
		try:
			if not self._MainWindows:
				self._MainWindows.Destroy()
		except (AttributeError, RuntimeError):
			pass

	@script(gesture=None, description= _("Muestra la ventana con todos los complementos y su información"), category= "TiendaNVDA")
	def script_menu1(self, event):
		if ajustes.IS_WinON == False:
			self._MainWindows = HiloComplemento(1)
			self._MainWindows.start()

	@script(gesture=None, description= _("Busca actualizaciones de los complementos instalados"), category= "TiendaNVDA")
	def script_menu2(self, event):
		if ajustes.IS_WinON == False:
			self._MainWindows = HiloComplemento(2)
			self._MainWindows.start()

	def menu3(self, event):
		if ajustes.IS_WinON == False:
			self._MainWindows = HiloComplemento(3)
			self._MainWindows.start()

class tiendaApp(wx.Dialog):
	def __init__(self, parent, datos):

		WIDTH = 1600
		HEIGHT = 800

		super(tiendaApp,self).__init__(parent, -1, title="Tienda NVDA", size = (WIDTH, HEIGHT))

		ajustes.IS_WinON = True
		self.data = datos

		self.Panel = wx.Panel(self, 1)

		labelBusqueda = wx.StaticText(self.Panel, wx.ID_ANY, "&Buscar:")
		self.textoBusqueda = wx.TextCtrl(self.Panel, 2)
		self.textoBusqueda.Bind(wx.EVT_CONTEXT_MENU, self.skip)
		self.textoBusqueda.Bind(wx.EVT_KEY_UP, self.onBusquedaCall)

		labelComplementos = wx.StaticText(self.Panel, wx.ID_ANY, "&Lista complementos:")
		self.listboxComplementos = wx.ListBox(self.Panel, 3, style = wx.LB_NO_SB)
		if ajustes.ordenacion == False:
			self.listboxComplementos.Append(self.data.nombrEntero())
		else:
			self.listboxComplementos.Append(self.data.nombrEntero(True))
		self.listboxComplementos.SetSelection(0)
		self.listboxComplementos.SetFocus()
		self.listboxComplementos.Bind(wx.EVT_KEY_UP, self.onLisbox)

		labelResultado = wx.StaticText(self.Panel, wx.ID_ANY, "&Información:")
		self.txtResultado = wx.TextCtrl(self.Panel, 4, style =wx.TE_MULTILINE|wx.TE_READONLY|wx.LB_NO_SB)

		self.descargarBTN = wx.Button(self.Panel, 201, "&Descargar complemento")
		self.paginaWebBTN = wx.Button(self.Panel, 202, "Visitar &página WEB")
		self.salirBTN = wx.Button(self.Panel, 203, "&Salir")
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

	def onBusqueda(self):
		temporal = []
		busqueda = self.textoBusqueda.GetValue()
		if ajustes.ordenacion == False:
			lista = self.data.nombrEntero()
		else:
			lista = self.data.nombrEntero(True)
		self.listboxComplementos.Clear()
		for item in lista:
			if busqueda.lower() in item.lower():
				temporal.append(item)
		if len(temporal) == 0:
			self.listboxComplementos.Append("No se encontraron resultados")
			self.listboxComplementos.SetSelection(0)
			self.onLisbox(None)
		else:
			self.listboxComplementos.Append(temporal)
			self.listboxComplementos.SetSelection(0)
			self.onLisbox(None)

	def onBusquedaCall(self, event):
		event.Skip()
		wx.	CallAfter(self.onBusqueda)

	def onFicha(self):
		nombre = self.listboxComplementos.GetString(self.listboxComplementos.GetSelection())
		indice = self.data.indiceSummary(nombre)
		datos = self.data.dataServidor[indice]
		ficha = \
"""Autor: {}
Nombre del complemento: {}
Nombre interno: {}
Descripción: {}\n""".format(
	datos['author'],
	datos['summary'],
	datos['name'],
	datos['description'],
	)
		self.txtResultado.SetValue(ficha)

		for i in range(len(datos['links'])):
			fichaEnlaces = \
"""Canal: {}
Versión: {}
Mínimo NVDA: {}
Testeado hasta versión de NVDA: {}
Total descargas: {}\n""".format(
	datos['links'][i]['channel'],
	datos['links'][i]['version'],
	datos['links'][i]['minimum'],
	datos['links'][i]['lasttested'],
	datos['links'][i]['downloads'],
	)
			self.txtResultado.AppendText(fichaEnlaces)
		self.txtResultado.SetInsertionPoint(0)


	def onLisbox(self, event):
		if self.listboxComplementos.GetSelection() == -1:
			pass
		else:
			if self.listboxComplementos.GetString(self.listboxComplementos.GetSelection()) == "No se encontraron resultados":
				self.txtResultado.Clear()
			else:
				nombre = self.listboxComplementos.GetString(self.listboxComplementos.GetSelection())
				indice = self.data.indiceSummary(nombre)
				datos = self.data.dataServidor[indice]
				self.onFicha()

	def onBoton(self, event):
		obj = event.GetEventObject()
		botonID = obj.GetId()
		nombre = self.listboxComplementos.GetString(self.listboxComplementos.GetSelection())
		indice = self.data.indiceSummary(nombre)
		datos = self.data.dataServidor[indice]
		if botonID == 201:
			self.menuDescarga = wx.Menu()

			for i in range(len(datos['links'])):
				item = self.menuDescarga.Append(i, "Versión {}".format(datos['links'][i]['channel']))
				self.Bind(wx.EVT_MENU, self.onDescarga, item)

			position = self.descargarBTN.GetPosition()
			self.PopupMenu(self.menuDescarga,position)
			pass

		elif botonID == 202:
			webbrowser.open_new(datos['url'])
		elif botonID == 203:
			ajustes.IS_WinON = False
			ajustes.focoActual = "listboxComplementos"
			self.Destroy()
			gui.mainFrame.postPopup()
		else:
			ajustes.IS_WinON = False
			ajustes.focoActual = "listboxComplementos"
			self.Destroy()
			gui.mainFrame.postPopup()

	def onDescarga(self, event):
		nombre = self.listboxComplementos.GetString(self.listboxComplementos.GetSelection())
		indice = self.data.indiceSummary(nombre)
		datos = self.data.dataServidor[indice]
		url = self.data.urlBase+datos['links'][event.GetId()]['file']
		HiloGuardarArchivo(self, url)

	def TrueDescarga(self, fichero_final, objeto, path):
		dlg = DescargaDialogo("Descargando %s..." % fichero_final, objeto, path, 15)
		result = dlg.ShowModal()
		if result == ajustes.ID_TRUE:
			if ajustes.installDescarga == True:
				addonGui.handleRemoteAddonInstall(path)
			self.listboxComplementos.SetFocus()
			dlg.Destroy()
		else:
			self.listboxComplementos.SetFocus()
			dlg.Destroy()

	def FalseDescarga(self):
		self.listboxComplementos.SetFocus()

	def onkeyVentanaDialogo(self, event):
		if event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
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

		super(BuscarActualizacionesDialogo,self).__init__(parent, -1, title="Tienda NVDA", size = (WIDTH, HEIGHT))

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

		self.ActualizarBTN = wx.Button(self.Panel, 101, "&Actualizar")
		self.CerrarBTN = wx.Button(self.Panel, 102, "&Cerrar")
		self.Bind(wx.EVT_BUTTON,self.onBoton)
		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)
		self.Bind(wx.EVT_CLOSE, self.onBoton)

		sizeMain = wx.BoxSizer(wx.VERTICAL)
		szBotones = wx.BoxSizer(wx.HORIZONTAL)

		sizeMain.Add(self.chkListBox, 1, wx.EXPAND)
		szBotones.Add(self.ActualizarBTN, 2, wx.CENTER)
		szBotones.Add(self.CerrarBTN, 2, wx.CENTER)

		sizeMain.Add(szBotones, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeMain)

		self.CenterOnScreen()

	def onAddonsChecked(self, event):
#		if any([self.addonsList.IsChecked(addon) for addon in range(self.addonsList.GetItemCount())]):

		index = event.GetSelection()
		label = self.chkListBox.GetString(index)
		print(index)
		status = False
		if self.chkListBox.IsChecked(index):
			status = True
		print('Box %s is %s checked \n' % (label, status))
		self.chkListBox.SetSelection(index)    # so that (un)checking also selects (moves the highlight)
#		print(self.listIndex)

	def onBoton(self, event):
		obj = event.GetEventObject()
		botonID = obj.GetId()
		if botonID == 101:
			listaSeleccion = [i for i in range(self.chkListBox.GetCount()) if self.chkListBox.IsChecked(i)]
			if len(listaSeleccion) == 0:
				gui.messageBox(_("Tiene que seleccionar una actualización para poder continuar."),
					_("Error"), wx.ICON_ERROR)
				self.self.chkListBox.SetFocus()
			else:
				hilo =HiloLanzaActualizacion(self.nombreUrl, listaSeleccion)
				hilo.start()
				ajustes.IS_WinON = False
				self.Destroy()
				gui.mainFrame.postPopup()
		elif botonID == 102:
			ajustes.IS_WinON = False
			self.Destroy()
			gui.mainFrame.postPopup()
		else:
			ajustes.IS_WinON = False
			self.Destroy()
			gui.mainFrame.postPopup()

	def onkeyVentanaDialogo(self, event):
		if event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
			ajustes.IS_WinON = False
			self.Destroy()
			gui.mainFrame.postPopup()
		else:
			event.Skip()

class AjustesDialogo(wx.Dialog):
	def __init__(self, parent, datos):

		WIDTH = 800
		HEIGHT = 600

		super(AjustesDialogo,self).__init__(parent, -1, title="Opciones", size = (WIDTH, HEIGHT))

		ajustes.IS_WinON = True
		self.data = datos

		self.Panel = wx.Panel(self)

		self.TreeBook = wx.Treebook(self.Panel)

		self.PageGeneral = wx.Panel(self.TreeBook)
		self.PageComplementos = wx.Panel(self.TreeBook)

		self.TreeBook.AddPage(self.PageGeneral, "General")
		self.TreeBook.AddPage(self.PageComplementos, "Complementos")

		self.TreeBook.SetFocus()

		self.AceptarBTN = wx.Button(self.Panel, wx.ID_ANY, "&Aceptar")
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, wx.ID_ANY, "&Cancelar")
		self.Bind(wx.EVT_BUTTON, self.onCancelar, id=self.CancelarBTN.GetId())
		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)
		self.Bind(wx.EVT_CLOSE, self.onCancelar)

		sizer_TreeBook = wx.BoxSizer(wx.VERTICAL)
		sizer_TreeBook_BTN = wx.BoxSizer(wx.HORIZONTAL)

		sizer_TreeBook.Add(self.TreeBook, 1, wx.ALL|wx.EXPAND, 5)
		sizer_TreeBook_BTN.Add(self.AceptarBTN, 2, wx.CENTER, 5)
		sizer_TreeBook_BTN.Add(self.CancelarBTN, 2, wx.CENTER, 5)

		sizer_TreeBook.Add(sizer_TreeBook_BTN, 0, wx.CENTER, 5)

		self.Panel.SetSizer(sizer_TreeBook)

########## Pagina General

		self.checkBox101 = wx.CheckBox(self.PageGeneral, 101, "Ordenar por orden alfabético la lista de complementos")
		if ajustes.ordenacion == True:
			self.checkBox101.SetValue(True)
		else:
			self.checkBox101.SetValue(False)

		self.checkBox102 = wx.CheckBox(self.PageGeneral, 102, "Instalar complementos después de descargar de la tienda")
		if ajustes.installDescarga == True:
			self.checkBox102.SetValue(True)
		else:
			self.checkBox102.SetValue(False)

		sizeVertical = wx.BoxSizer(wx.VERTICAL)
		sizeVertical.Add(self.checkBox101, 0, wx.EXPAND)
		sizeVertical.Add(self.checkBox102, 0, wx.EXPAND)
		self.PageGeneral.SetSizer(sizeVertical)

########## Pagina Complementos

		labelComplementos = wx.StaticText(self.PageComplementos, wx.ID_ANY, "&Lista de complementos - Versión para buscar actualización:")
		self.lstBoxComplementos = wx.ListBox(self.PageComplementos, 101)
		for k, v in ajustes.listaComplementos.items():
			self.lstBoxComplementos.Append(k + " -- " + v)
		self.lstBoxComplementos.SetSelection(0)
		self.lstBoxComplementos.Bind(wx.EVT_KEY_UP, self.onListBox)

		sizerPrincipal = wx.BoxSizer(wx.VERTICAL)

		sizerPrincipal.Add(labelComplementos, 0)
		sizerPrincipal.Add(self.lstBoxComplementos, 1, wx.EXPAND)

		self.PageComplementos.SetSizer(sizerPrincipal)

		self.Bind(wx.EVT_CHECKBOX,self.onChecked) 

		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def onChecked(self, event):
		diccionario_ajuste = {
			101:"ajustes.ordenacion",
			102:"ajustes.installDescarga",
		}
		chk = event.GetEventObject()
		chkId = chk.GetId()
		valor = diccionario_ajuste.get(chkId)
		if eval(diccionario_ajuste.get(chkId)) == True:
			chk.SetValue(False)
			exec(valor+"=False")
		else:
			chk.SetValue(True)
			exec(valor+"=True")

	def onListBox(self, event):
		nombre = self.lstBoxComplementos.GetString(self.lstBoxComplementos.GetSelection()).split(" -- ")
		nombreLocal = self.data.obtenerNameLocal(nombre[0])
		indice = self.data.indiceName(nombreLocal)
		datos = self.data.dataServidor[indice]
		if event.GetKeyCode() == 32: # Pulsamos intro para seleccionar. 32 es espacio.
			self.menuDescarga = wx.Menu()
			for i in range(len(datos['links'])):
				item = self.menuDescarga.Append(i, "Canal {}".format(datos['links'][i]['channel']))
				self.Bind(wx.EVT_MENU, self.onSelect, item)

			position = self.lstBoxComplementos.GetPosition()
			self.PopupMenu(self.menuDescarga,position)
			pass

	def modificaListBox(self, canalID):
		nombre = self.lstBoxComplementos.GetString(self.lstBoxComplementos.GetSelection()).split(" -- ")
		nombreLocal = self.data.obtenerNameLocal(nombre[0])
		indice = self.data.indiceName(nombreLocal)
		datos = self.data.dataServidor[indice]
		nombreCanal = datos['links'][canalID]['channel']
		nombreCompuesto = nombre[0] + " -- " + nombreCanal
		pos = self.lstBoxComplementos.GetSelection()
		self.lstBoxComplementos.Delete(pos)
		self.lstBoxComplementos.Insert(nombreCompuesto, pos)
		self.lstBoxComplementos.SetSelection(pos)

	def onSelect(self, event):
		self.modificaListBox(event.GetId())

	def guardaListBox(self):
		p = [self.lstBoxComplementos.GetString(i) for i in range(self.lstBoxComplementos.GetCount())]
		l1 = []
		l2 = []
		for i in p:
			z = i.split(" -- ")
			l1.append(z[0])
			l2.append(z[1])
		ajustes.listaComplementos = dict(zip(l1, l2))

	def onAceptar(self, event):
		self.guardaListBox()
		ajustes.GuardaValores()
		ajustes.IS_WinON = False
		self.Destroy()
		gui.mainFrame.postPopup()

	def onkeyVentanaDialogo(self, event):
		if event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
			ajustes.ValoresDefecto()
			ajustes.GuardaValores()
			ajustes.IS_WinON = False
			self.Destroy()
			gui.mainFrame.postPopup()
		else:
			event.Skip()

	def onCancelar(self, event):
		ajustes.ValoresDefecto()
		ajustes.GuardaValores()
		ajustes.IS_WinON = False
		self.Destroy()
		gui.mainFrame.postPopup()

class DescargaDialogo(wx.Dialog):
	def __init__(self, titulo, url, file, seconds):

		super(DescargaDialogo, self).__init__(None, -1, title=titulo)

#		self.SetSize((400, 130))
		self.CenterOnScreen()

		self.url = url
		self.file = file
		self.seconds = seconds

		panel = wx.Panel(self)
		self.Panel = panel

		self.progressBar=wx.Gauge(self.Panel, wx.ID_ANY, range=100, style = wx.GA_HORIZONTAL)
		self.textorefresco = wx.TextCtrl(self.Panel, wx.ID_ANY, style =wx.TE_MULTILINE|wx.TE_READONLY)
		self.textorefresco.Bind(wx.EVT_CONTEXT_MENU, self.skip)

		self.AceptarTRUE = wx.Button(self.Panel, ajustes.ID_TRUE, "&Aceptar")
		self.Bind(wx.EVT_BUTTON, self.onAceptarTRUE, id=self.AceptarTRUE.GetId())
		self.AceptarTRUE.Disable()

		self.AceptarFALSE = wx.Button(self.Panel, ajustes.ID_FALSE, "&Cerrar")
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

		super(ActualizacionDialogo, self).__init__(None, -1, title="Actualizando complementos")

#		self.SetSize((400, 130))
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

		self.AceptarTRUE = wx.Button(self.Panel, ajustes.ID_TRUE, "&Aceptar")
		self.Bind(wx.EVT_BUTTON, self.onAceptarTRUE, id=self.AceptarTRUE.GetId())
		self.AceptarTRUE.Disable()

		self.AceptarFALSE = wx.Button(self.Panel, ajustes.ID_FALSE, "&Cerrar")
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
		ajustes.IS_WinON = False
		self.Destroy()
		gui.mainFrame.postPopup()

class HiloGuardarArchivo(Thread):
	def __init__(self, frame, url):
		super(HiloGuardarArchivo, self).__init__()

		self.frame = frame
		self.url = url
		self.daemon = True
		self.start()
	def run(self):
		fichero, objeto = funciones.obtenerNombreArchivo(self.url)
		wildcard = "Complemento de NVDA (*.nvda-addon)|*.nvda-addon"
		dlg = wx.FileDialog(None, message="Guardar en...", defaultDir=os.environ['SYSTEMDRIVE'], defaultFile=fichero, wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			fichero_final = os.path.basename(path)
			dlg.Destroy()
			wx.CallAfter(self.frame.TrueDescarga, fichero_final, objeto, path)
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
		self.daemon = True
		self.opcion = opcion
	def run(self):
		def tiendaAppDialogo(datos):
			self._MainWindows = tiendaApp(gui.mainFrame, datos)
			gui.mainFrame.prePopup()
			self._MainWindows.Show()

		def ActualizacionDialogo(nombreUrl, verInstalada, verInstalar):
			self._MainWindows = BuscarActualizacionesDialogo(gui.mainFrame, nombreUrl, verInstalada, verInstalar)
			gui.mainFrame.prePopup()
			self._MainWindows.Show()

		def OpcionesDialogo(datos):
			self._MainWindows = AjustesDialogo(gui.mainFrame, datos)
			gui.mainFrame.prePopup()
			self._MainWindows.Show()

		try:
			datos = basedatos.JsonNVDAes()
			if self.opcion == 1:
				wx.CallAfter(tiendaAppDialogo, datos)
			elif self.opcion == 2:
				nombreUrl, verInstalada, verInstalar = datos.chkActualizaS()
				if nombreUrl == False:
					gui.messageBox(_("No hay actualizaciones."),
						_("Información"), wx.ICON_INFORMATION)
				else:
					wx.CallAfter(ActualizacionDialogo, nombreUrl, verInstalada, verInstalar)
			elif self.opcion == 3:
				wx.CallAfter(OpcionesDialogo, datos)
		except:
			msg = \
"""No se pudo tener acceso al servidor de complementos.

Inténtelo en unos minutos."""
			gui.messageBox(msg,
				_("Error"), wx.ICON_ERROR)

class HiloDescarga(Thread):
	def __init__(self, frame, objeto, ruta, tiempo):
		super(HiloDescarga, self).__init__()

		self.frame = frame
		self.objeto = objeto
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
			wx.CallAfter(self.frame.TextoRefresco, "Espere por favor...\n" + "Descargando: %s" % self.humanbytes(readsofar))
			if readsofar >= total_size: # Si queremos hacer algo cuando la descarga termina.
				pass
		else: # Si la descarga es solo el tamaño
			wx.CallAfter(self.frame.TextoRefresco, "Espere por favor...\n" + "Descargando: %s" % self.humanbytes(readsofar))

	def run(self):
		try:
			socket.setdefaulttimeout(self.tiempo) # Dara error si pasan 30 seg sin internet
			urllib.request.urlretrieve(self.objeto.geturl(), self.ruta, reporthook=self.__call__)
			wx.CallAfter(self.frame.done, "La descarga se completó.\n" + "Ya puede cerrar esta ventana.")
		except:
			wx.CallAfter(self.frame.error, "Algo salió mal.\n" + "Compruebe que tiene conexión a internet y vuelva a intentarlo.\n" + "Ya puede cerrar esta ventana.")
			os.remove(self.ruta)

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
			wx.CallAfter(self.frame.TextoRefresco, "Espere por favor...\n" + "Descargando: %s" % self.humanbytes(readsofar))
			if readsofar >= total_size: # Si queremos hacer algo cuando la descarga termina.
				pass
		else: # Si la descarga es solo el tamaño
			wx.CallAfter(self.frame.TextoRefresco, "Espere por favor...\n" + "Descargando: %s" % self.humanbytes(readsofar))

	def run(self):

		try:
			for i in self.listaSeleccion:
				fichero = self.generaFichero()
				socket.setdefaulttimeout(self.tiempo)
				opener = urllib.request.build_opener()
				opener.addheaders = [('User-agent', 'Mozilla/5.0')]
				urllib.request.install_opener(opener)
				urllib.request.urlretrieve(list(self.nombreUrl.values())[i], fichero, reporthook=self.__call__)
				bundle = addonHandler.AddonBundle(fichero)
				if not addonVersionCheck.hasAddonGotRequiredSupport(bundle):
					pass #Podemos crear un control de errores aquí para complementos que no se pueden instalar por incompatibilidad y luego dar un mensaje
				else:
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
				wx.CallAfter(self.frame.onActualizacion, 1)
			wx.CallAfter(self.frame.done, "La actualización se completó.\nNVDA necesita reiniciarse para aplicar las actualizaciones.\n¿Desea reiniciar NVDA ahora?")
		except:
			wx.CallAfter(self.frame.error, "Algo salió mal.\n" + "Compruebe que tiene conexión a internet y vuelva a intentarlo.\n" + "Ya puede cerrar esta ventana.")
		try:
			shutil.rmtree(self.directorio, ignore_errors=True)
		except:
			pass


