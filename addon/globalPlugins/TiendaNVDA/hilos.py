# -*- coding: utf-8 -*-
# Copyright (C) 2021-2025 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.
#
# Hilos de carga para la tienda de complementos
#

import addonHandler
import gui
import ui
import wx
import traceback
from threading import Thread
from logHandler import log
from . import ajustes
from . import basedatos
from . import tienda_oficial

addonHandler.initTranslation()


class HiloLanzaActualizacion(Thread):
	"""Hilo para lanzar el diálogo de actualización"""

	def __init__(self, nombreUrl, listaSeleccion):
		super().__init__(daemon=True)
		self.nombreUrl = nombreUrl
		self.listaSeleccion = listaSeleccion

	def run(self):
		def lanzar():
			from .dialogos_actualizaciones import ActualizacionDialogo
			dlg = ActualizacionDialogo(gui.mainFrame, self.nombreUrl, self.listaSeleccion, 15)
			gui.mainFrame.prePopup()
			dlg.Show()
		wx.CallAfter(lanzar)


class HiloComplemento(Thread):
	"""Hilo para cargar la tienda de complementos"""

	def __init__(self, opcion, fuente):
		super().__init__(daemon=True)
		self.opcion = opcion
		self.fuente = fuente

	def run(self):
		try:
			fuente_val = self.fuente.value if hasattr(self.fuente, 'value') else self.fuente
			if fuente_val == "nvda_es":
				self._cargarNVDAES()
			elif fuente_val in ("oficial", "official"):
				self._cargarOficial()
			elif fuente_val == "all":
				self._cargarUnificada()
		except Exception as e:
			log.debug(f"Error en HiloComplemento: {e}")
			traceback.print_exc()

	def _cargarNVDAES(self):
		datos = basedatos.NVDAStoreClient()
		if datos.dataServidor is None:
			msg = _("No se pudo conectar al servidor y no hay datos en caché. ¿Desea intentar cambiar de servidor?")
			if wx.MessageBox(msg, _("Error"), wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
				wx.CallAfter(self._mostrarSinComplementos)
			return

		if datos.isOffline:
			ui.message(_("Trabajando en modo OFFLINE. Los datos mostrados pueden estar desactualizados. Algunas descargas podrían no funcionar."))

		if self.opcion == 1:
			if len(datos.dataServidor) == 0:
				wx.CallAfter(self._mostrarSinComplementos)
			else:
				wx.CallAfter(self._mostrarTiendaES, datos)
		elif self.opcion == 2:
			nombreUrl, verInstalada, verInstalar = datos.chkActualizaS(includeIncompatible=ajustes.tempAllowIncompatible)
			if nombreUrl is None:
				ajustes.IS_WinON = True
				gui.messageBox(_("No hay actualizaciones disponibles."), _("Información"), wx.ICON_INFORMATION)
				ajustes.IS_WinON = False
			else:
				wx.CallAfter(self._mostrarActualizaciones, nombreUrl, verInstalada, verInstalar)

	def _cargarOficial(self):
		addons = tienda_oficial.obtener_complementos_oficiales(
			includeIncompatible=ajustes.tempAllowIncompatible
		)
		if not addons:
			gui.messageBox(_("No se pudieron obtener complementos de la tienda oficial."), _("Error"), wx.ICON_ERROR)
			return

		if self.opcion == 1:
			wx.CallAfter(self._mostrarTiendaOficial, addons)
		elif self.opcion == 2:
			updates = tienda_oficial.buscar_actualizaciones_oficiales()
			if not updates:
				ajustes.IS_WinON = True
				gui.messageBox(_("No hay actualizaciones oficiales disponibles."), _("Información"), wx.ICON_INFORMATION)
				ajustes.IS_WinON = False
			else:
				nombreUrl = {}
				verInstalada = []
				verInstalar = []
				for storeAddon, installed in updates:
					nombreUrl[storeAddon.displayName] = storeAddon.URL
					verInstalada.append(installed.version)
					verInstalar.append(storeAddon.addonVersionName)
				wx.CallAfter(self._mostrarActualizaciones, nombreUrl, verInstalada, verInstalar, "oficial")

	def _cargarUnificada(self):
		datosES = basedatos.NVDAStoreClient()
		addonsOficial = tienda_oficial.obtener_complementos_oficiales(
			includeIncompatible=ajustes.tempAllowIncompatible
		)
		wx.CallAfter(self._mostrarTiendaUnificada, datosES, addonsOficial)

	def _mostrarSinComplementos(self):
		from .dialogos_servidores import SinComplementos
		dlg = SinComplementos(gui.mainFrame)
		gui.mainFrame.prePopup()
		dlg.Show()

	def _mostrarTiendaES(self, datos):
		from .dialogos_tienda_es import TiendaApp
		dlg = TiendaApp(gui.mainFrame, datos)
		gui.mainFrame.prePopup()
		dlg.Show()

	def _mostrarTiendaOficial(self, addons):
		from .dialogos_tienda_oficial import TiendaOficialApp
		dlg = TiendaOficialApp(gui.mainFrame, addons)
		gui.mainFrame.prePopup()
		dlg.Show()

	def _mostrarTiendaUnificada(self, datosES, addonsOficial):
		from .dialogos_tienda_unificada import TiendaUnificadaApp
		dlg = TiendaUnificadaApp(gui.mainFrame, datosES, addonsOficial)
		gui.mainFrame.prePopup()
		dlg.Show()

	def _mostrarActualizaciones(self, nombreUrl, verInstalada, verInstalar, fuente="nvda_es"):
		from .dialogos_actualizaciones import BuscarActualizacionesDialogo
		dlg = BuscarActualizacionesDialogo(gui.mainFrame, nombreUrl, verInstalada, verInstalar, fuente)
		gui.mainFrame.prePopup()
		dlg.Show()
