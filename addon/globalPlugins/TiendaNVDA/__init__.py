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
from logHandler import log
import config
from gui.settingsDialogs import NVDASettingsDialog, SettingsPanel
from gui import guiHelper, nvdaControls
import wx
import wx.adv
import webbrowser
from threading import Thread, Timer
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
except Exception as e:
	log.info(_("No se pudieron cargar las librerías necesarias para la Tienda"))

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()

		if globalVars.appArgs.secure: return

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
		else:
			ui.message(_("Ya hay una instancia de la Tienda NVDA abierta."))

	@script(gesture=None, description= _("Busca actualizaciones de los complementos instalados"), category= "TiendaNVDA")
	def script_menu2(self, event):
		if ajustes.IS_WinON == False:
			self._MainWindows = HiloComplemento(2)
			self._MainWindows.start()
		else:
			ui.message(_("Ya hay una instancia de la Tienda NVDA abierta."))

class tiendaApp(wx.Dialog):
	def __init__(self, parent):

		WIDTH = 1600
		HEIGHT = 800

		super(tiendaApp,self).__init__(parent, -1, title=_("Tienda NVDA.ES"), size = (WIDTH, HEIGHT))

		ajustes.IS_WinON = True
		self.datos = basedatos.NVDAStoreClient()

		self.Panel = wx.Panel(self, 1)

		labelBusqueda = wx.StaticText(self.Panel, wx.ID_ANY, _("&Buscar:"))
		self.textoBusqueda = wx.TextCtrl(self.Panel, 2,style = wx.TE_PROCESS_ENTER)
		self.textoBusqueda.Bind(wx.EVT_CONTEXT_MENU, self.skip)
		self.textoBusqueda.Bind(wx.EVT_TEXT_ENTER, self.onBusqueda)

		labelComplementos = wx.StaticText(self.Panel, wx.ID_ANY, _("&Lista complementos:"))
		self.listboxComplementos = wx.ListBox(self.Panel, 3, style = wx.LB_NO_SB)
		for x in range(0, len(self.datos.dataServidor)):
			self.listboxComplementos.Append(self.datos.dataServidor[x]['summary'])
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
Descripción: {}\n""").format(
	datos['author'],
	datos['summary'],
	datos['name'],
	datos['description'],
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
			for x in range(0, len(self.datos.dataServidor)):
				self.listboxComplementos.Append(self.datos.dataServidor[x]['summary'])
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
				self.listboxComplementos.Append(filtro)
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
		indice = self.datos.indiceSummary(nombre)
		datos = self.datos.dataServidor[indice]
		url = self.datos.urlBase+datos['links'][event.GetId()]['file']
		nombreFile = self.datos.GetFilenameDownload(datos['links'][event.GetId()]['file'])
		if nombreFile.split(".")[0] == "get":
			try:
				nombreFile = basedatos.obtenFile(datos['links'][event.GetId()]['link'])
			except:
				try:
					nombreFile = basedatos.obtenFileAlt(url)
				except:
					msg = \
_("""No se pudo obtener el nombre del archivo a descargar.

{} del canal {}

Se va a proceder a descargar con su navegador predefinido.""").format(nombre, datos['links'][event.GetId()]['channel'])
					gui.messageBox(msg,
						_("Información"), wx.ICON_INFORMATION)
					nombreFile = ""
					webbrowser.open_new(url)
					return
		HiloGuardarArchivo(self, nombreFile, url)

	def TrueDescarga(self, fichero_final, url, path):
		dlg = DescargaDialogo(_("Descargando %s...") % fichero_final, url, path, 15)
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
			getattr(self, ajustes.focoActual).SetFocus()
			pass

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

		super(BuscarActualizacionesDialogo,self).__init__(parent, -1, title=_("Tienda NVDA.ES - Actualizaciones disponibles"), size = (WIDTH, HEIGHT))

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

		self.ActualizarBTN = wx.Button(self.Panel, 101, _("&Actualizar"))
		self.CerrarBTN = wx.Button(self.Panel, 102, _("&Cerrar"))
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
#		print(index)
		status = False
		if self.chkListBox.IsChecked(index):
			status = True
#		print('Box %s is %s checked \n' % (label, status))
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
		ajustes.IS_WinON = False
		self.Destroy()
		gui.mainFrame.postPopup()

class HiloGuardarArchivo(Thread):
	def __init__(self, frame, nombreFile, url):
		super(HiloGuardarArchivo, self).__init__()

		self.frame = frame
		self.nombreFile = nombreFile
		self.url = url
		self.daemon = True
		self.start()
	def run(self):
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
				wx.CallAfter(self.frame.onActualizacion, i+1)
			wx.CallAfter(self.frame.done, _("La actualización se completó.\n") + _("NVDA necesita reiniciarse para aplicar las actualizaciones.\n") + _("¿Desea reiniciar NVDA ahora?"))
		except:
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
		def tiendaAppDialogo():
			self._MainWindows = tiendaApp(gui.mainFrame)
			gui.mainFrame.prePopup()
			self._MainWindows.Show()

		def ActualizacionDialogo(nombreUrl, verInstalada, verInstalar):
			self._MainWindows = BuscarActualizacionesDialogo(gui.mainFrame, nombreUrl, verInstalada, verInstalar)
			gui.mainFrame.prePopup()
			self._MainWindows.Show()

		try:
			datos = basedatos.NVDAStoreClient()
			if self.opcion == 1:
				wx.CallAfter(tiendaAppDialogo)
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

class RepeatTimer(object):
	def __init__(self, interval, function, *args, **kwargs):

		self._timer     = None
		self.interval   = interval
		self.function   = function
		self.args       = args
		self.kwargs     = kwargs
		self.is_running = False
		self.start()

	def _run(self):
		self.is_running = False
		self.start()
		self.function(*self.args, **self.kwargs)

	def start(self):
		if not self.is_running:
			self._timer = Timer(self.interval, self._run)
			self._timer.start()
			self.is_running = True

	def stop(self):
		self._timer.cancel()
		self.is_running = False

