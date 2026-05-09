# -*- coding: utf-8 -*-
# Copyright (C) 2021-2025 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.
#
# Diálogos de actualizaciones, descargas y restauración de backup
#

import addonHandler
from addonHandler import addonVersionCheck
import gui
from gui.nvdaControls import CustomCheckListBox
import ui
import core
from logHandler import log
from tones import beep
import wx
import winsound
import shutil
import os
import time
import traceback
from threading import Thread, Event

from . import ajustes
from . import basedatos
from . import tienda_oficial
from . import red
from . import version_utils
from .addon_manager import AddonManager

addonHandler.initTranslation()


class DescargaDialogo(wx.Dialog):
	"""Diálogo de progreso de descarga con reintentos automáticos usando requests"""

	def __init__(self, parent, titulo, url, file, seconds, isInstaller=False):
		super().__init__(parent, title=titulo, size=(500, 300))
		self.url = url
		self.file = file
		self.seconds = seconds
		self.isInstaller = isInstaller

		panel = wx.Panel(self)
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.progressBar = wx.Gauge(panel, range=100)
		sizer.Add(self.progressBar, 0, wx.EXPAND | wx.ALL, 10)
		self.txtInfo = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
		sizer.Add(self.txtInfo, 1, wx.EXPAND | wx.ALL, 10)
		btnSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.okBtn = wx.Button(panel, id=ajustes.ID_TRUE, label=_("&Aceptar"))
		self.cancelBtn = wx.Button(panel, id=ajustes.ID_FALSE, label=_("&Cerrar"))
		self.okBtn.Disable()
		self.cancelBtn.Disable()
		btnSizer.Add(self.okBtn, 1, wx.ALL, 5)
		btnSizer.Add(self.cancelBtn, 1, wx.ALL, 5)
		sizer.Add(btnSizer, 0, wx.ALIGN_CENTER)
		panel.SetSizer(sizer)
		self.CenterOnScreen()

		self.okBtn.Bind(wx.EVT_BUTTON, self.onOk)
		self.cancelBtn.Bind(wx.EVT_BUTTON, self.onCancel)
		self.Bind(wx.EVT_CLOSE, lambda e: None)
		Thread(target=self._descargar, daemon=True).start()

	def _descargar(self):
		def _progress(percent, downloaded, total):
			wx.CallAfter(self.progressBar.SetValue, percent)

		success = red.download_file(
			self.url, self.file,
			timeout=self.seconds,
			progress_callback=_progress,
			max_retries=3
		)

		if success:
			if not self.isInstaller:
				wx.CallAfter(self.txtInfo.AppendText, _("\nDescarga completada correctamente."))
				wx.CallAfter(self.okBtn.Enable)
			else:
				wx.CallAfter(self.EndModal, ajustes.ID_TRUE)
		else:
			wx.CallAfter(self.txtInfo.AppendText, _("\nError en la descarga tras varios intentos."))
			wx.CallAfter(self.cancelBtn.Enable)

	def onOk(self, event):
		self.EndModal(ajustes.ID_TRUE)

	def onCancel(self, event):
		self.EndModal(ajustes.ID_FALSE)


class BuscarActualizacionesDialogo(wx.Dialog):
	"""Diálogo para buscar y aplicar actualizaciones"""

	def __init__(self, parent, nombreUrl, verInstalada, verInstalar, fuente="nvda_es"):
		super().__init__(parent, title=_("Actualizaciones disponibles"), size=(800, 500))
		ajustes.IS_WinON = True
		self.nombreUrl = nombreUrl
		self.verInstalada = verInstalada
		self.verInstalar = verInstalar
		self.fuente = fuente

		panel = wx.Panel(self)
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.checkList = CustomCheckListBox(panel)
		for i, nombre in enumerate(nombreUrl.keys()):
			self.checkList.Append(f"{nombre} {verInstalada[i]} -> {verInstalar[i]}")
		self.checkList.SetSelection(0)
		sizer.Add(self.checkList, 1, wx.EXPAND | wx.ALL, 10)

		btnSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.selectAllBtn = wx.Button(panel, label=_("&Seleccionar todo"))
		self.deselectAllBtn = wx.Button(panel, label=_("&Deseleccionar todo"))
		self.updateBtn = wx.Button(panel, label=_("&Actualizar"))
		self.closeBtn = wx.Button(panel, label=_("&Cerrar"))
		btnSizer.Add(self.selectAllBtn, 1, wx.ALL, 5)
		btnSizer.Add(self.deselectAllBtn, 1, wx.ALL, 5)
		btnSizer.Add(self.updateBtn, 1, wx.ALL, 5)
		btnSizer.Add(self.closeBtn, 1, wx.ALL, 5)
		sizer.Add(btnSizer, 0, wx.EXPAND)
		panel.SetSizer(sizer)
		self.CenterOnScreen()

		self.selectAllBtn.Bind(wx.EVT_BUTTON, self.onSelectAll)
		self.deselectAllBtn.Bind(wx.EVT_BUTTON, self.onDeselectAll)
		self.updateBtn.Bind(wx.EVT_BUTTON, self.onUpdate)
		self.closeBtn.Bind(wx.EVT_BUTTON, self.onClose)
		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)

	def onSelectAll(self, event):
		for i in range(self.checkList.GetCount()):
			self.checkList.Check(i, True)

	def onDeselectAll(self, event):
		for i in range(self.checkList.GetCount()):
			self.checkList.Check(i, False)

	def onUpdate(self, event):
		seleccionados = [i for i in range(self.checkList.GetCount()) if self.checkList.IsChecked(i)]
		if not seleccionados:
			gui.messageBox(_("Seleccione al menos una actualización."), _("Error"), wx.ICON_ERROR)
			return
		from .hilos import HiloLanzaActualizacion
		HiloLanzaActualizacion(self.nombreUrl, seleccionados).start()
		ajustes.IS_WinON = False
		self.Destroy()
		gui.mainFrame.postPopup()

	def onClose(self, event):
		ajustes.IS_WinON = False
		self.Destroy()
		gui.mainFrame.postPopup()

	def onKeyPress(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.onClose(None)
		else:
			event.Skip()


class ActualizacionDialogo(wx.Dialog):
	"""Diálogo para actualizar múltiples complementos usando requests"""

	def __init__(self, frame, nombreUrl, listaSeleccion, seconds, allowIncompatible=False):
		super().__init__(frame, title=_("Actualizando complementos"), size=(550, 420))
		ajustes.IS_WinON = True
		self.nombreUrl = nombreUrl
		self.listaSeleccion = listaSeleccion
		self.seconds = seconds
		self.allowIncompatible = allowIncompatible
		self.directorio = os.path.join(ajustes.dirDatos, "temp")
		self.snapshotInicial = AddonManager.getSnapshot()
		self.exito = []
		self.fallos = []

		panel = wx.Panel(self)
		sizer = wx.BoxSizer(wx.VERTICAL)
		self.progressDescarga = wx.Gauge(panel, range=100)
		self.progressTotal = wx.Gauge(panel, range=len(listaSeleccion))
		sizer.Add(wx.StaticText(panel, label=_("Progreso descarga:")), 0, wx.ALL, 5)
		sizer.Add(self.progressDescarga, 0, wx.EXPAND | wx.ALL, 5)
		sizer.Add(wx.StaticText(panel, label=_("Progreso total:")), 0, wx.ALL, 5)
		sizer.Add(self.progressTotal, 0, wx.EXPAND | wx.ALL, 5)
		self.txtInfo = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
		sizer.Add(self.txtInfo, 1, wx.EXPAND | wx.ALL, 10)
		btnSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.reiniciarBtn = wx.Button(panel, label=_("&Reiniciar NVDA"))
		self.cerrarBtn = wx.Button(panel, label=_("&Cerrar"))
		self.reiniciarBtn.Disable()
		self.cerrarBtn.Disable()
		btnSizer.Add(self.reiniciarBtn, 1, wx.ALL, 5)
		btnSizer.Add(self.cerrarBtn, 1, wx.ALL, 5)
		sizer.Add(btnSizer, 0, wx.ALIGN_CENTER)
		panel.SetSizer(sizer)
		self.CenterOnScreen()

		self.reiniciarBtn.Bind(wx.EVT_BUTTON, self.onReiniciar)
		self.cerrarBtn.Bind(wx.EVT_BUTTON, self.onCerrar)
		self.Bind(wx.EVT_CLOSE, lambda e: None)
		Thread(target=self._actualizarTodos, daemon=True).start()

	def _actualizarTodos(self):
		if not os.path.exists(self.directorio):
			os.makedirs(self.directorio)

		for idx, i in enumerate(self.listaSeleccion):
			try:
				url = list(self.nombreUrl.values())[i]
				nombre = list(self.nombreUrl.keys())[i]
				fichero = os.path.join(self.directorio, f"temp{idx}.nvda-addon")

				wx.CallAfter(self.txtInfo.SetValue, _("Descargando: {}").format(nombre))

				def _progress(percent, downloaded, total):
					wx.CallAfter(self.progressDescarga.SetValue, percent)

				success = red.download_file(url, fichero, timeout=self.seconds, progress_callback=_progress)

				if not success:
					self.fallos.append(f"{nombre}: Error de descarga")
					wx.CallAfter(self.progressTotal.SetValue, idx + 1)
					continue

				# Instalar en el hilo principal
				install_result = [False]
				evt = Event()

				def instalar_en_main():
					try:
						abs_path = os.path.normpath(os.path.abspath(fichero))
						if not os.path.exists(abs_path) or os.path.getsize(abs_path) == 0:
							log.error(f"Archivo no encontrado o vacío: {abs_path}")
							evt.set()
							return
						time.sleep(0.3)
						bundle = addonHandler.AddonBundle(abs_path)
						is_compatible = addonVersionCheck.hasAddonGotRequiredSupport(bundle)
						if self.allowIncompatible or is_compatible:
							for addon in addonHandler.getAvailableAddons():
								if bundle.manifest['name'] == addon.manifest['name']:
									if not addon.isPendingRemove:
										addon.requestRemove()
									break
							install_result[0] = AddonManager.installAddon(abs_path, silent=True)
					except Exception as e:
						log.error(f"Error instalando {nombre}: {e}")
					evt.set()

				wx.CallAfter(self.txtInfo.SetValue, _("Instalando: {}").format(nombre))
				wx.CallAfter(instalar_en_main)
				evt.wait()

				if install_result[0]:
					self.exito.append(nombre)
				else:
					self.fallos.append(nombre)
				wx.CallAfter(self.progressTotal.SetValue, idx + 1)
			except Exception as e:
				self.fallos.append(f"{nombre}: {e}")

		try:
			shutil.rmtree(self.directorio, ignore_errors=True)
		except:
			pass

		if self.fallos or self.exito:
			reporte = _("RESUMEN DE OPERACIÓN:\n")
			reporte += "========================\n"
			if self.exito:
				reporte += _("Instalados con éxito ({}):\n").format(len(self.exito))
				for n in self.exito:
					reporte += f" - {n}\n"
			if self.fallos:
				if self.exito:
					reporte += "\n"
				reporte += _("Errores/Fallos ({}):\n").format(len(self.fallos))
				for n in self.fallos:
					reporte += f" - {n}\n"
			if self.exito:
				ajustes.reiniciarTrue = True
				wx.CallAfter(self._done, reporte)
			else:
				wx.CallAfter(self._error, reporte)
		else:
			wx.CallAfter(self._error, _("No se procesó ningún complemento."))

	def _done(self, reporte):
		winsound.MessageBeep(0)
		self.reiniciarBtn.Enable()
		self.cerrarBtn.Enable()
		self.txtInfo.SetValue(reporte + "\n" + _("Operación completada. Reinicie NVDA para aplicar cambios."))

	def _error(self, reporte):
		winsound.MessageBeep(16)
		self.cerrarBtn.Enable()
		self.txtInfo.SetValue(reporte)

	def onReiniciar(self, event):
		ajustes.IS_WinON = False
		ajustes.reiniciarTrue = False
		self.Destroy()
		gui.mainFrame.postPopup()
		core.restart()

	def onCerrar(self, event):
		ajustes.IS_WinON = False
		self._preguntarReinicio()
		self.Destroy()
		gui.mainFrame.postPopup()

	def _preguntarReinicio(self):
		if ajustes.reiniciarTrue or AddonManager.hasChanged(self.snapshotInicial):
			if gui.messageBox(
				_("Se han realizado cambios en los complementos que requieren reiniciar NVDA para surtir efecto. ¿Desea reiniciar ahora?"),
				_("Reiniciar NVDA"), wx.YES_NO | wx.ICON_QUESTION
			) == wx.YES:
				ajustes.reiniciarTrue = False
				core.restart()
		ajustes.reiniciarTrue = False


class RestaurarBackupDialogo(wx.Dialog):
	"""Diálogo para restaurar complementos desde un backup"""

	def __init__(self, parent, backup_data):
		super().__init__(parent, title=_("Restaurar desde Backup"), size=(900, 600))
		ajustes.IS_WinON = True
		self.backup_data = backup_data
		self.addons_encontrados = []

		panel = wx.Panel(self)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		contentSizer = wx.BoxSizer(wx.HORIZONTAL)

		leftSizer = wx.BoxSizer(wx.VERTICAL)
		leftSizer.Add(wx.StaticText(panel, label=_("&Seleccione complementos a restaurar:")), 0, wx.ALL, 5)
		self.checkList = CustomCheckListBox(panel)
		self.checkList.Bind(wx.EVT_LISTBOX, self.onSeleccion)
		leftSizer.Add(self.checkList, 1, wx.EXPAND | wx.ALL, 5)

		rightSizer = wx.BoxSizer(wx.VERTICAL)
		rightSizer.Add(wx.StaticText(panel, label=_("&Información de la versión encontrada:")), 0, wx.ALL, 5)
		self.txtInfo = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
		rightSizer.Add(self.txtInfo, 1, wx.EXPAND | wx.ALL, 5)

		contentSizer.Add(leftSizer, 1, wx.EXPAND)
		contentSizer.Add(rightSizer, 1, wx.EXPAND)
		mainSizer.Add(contentSizer, 1, wx.EXPAND | wx.ALL, 10)

		selBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.selectAllBtn = wx.Button(panel, label=_("&Seleccionar todo"))
		self.deselectAllBtn = wx.Button(panel, label=_("&Deseleccionar todo"))
		selBtnSizer.Add(self.selectAllBtn, 1, wx.ALL, 5)
		selBtnSizer.Add(self.deselectAllBtn, 1, wx.ALL, 5)
		mainSizer.Add(selBtnSizer, 0, wx.CENTER)

		btnSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.installBtn = wx.Button(panel, label=_("&Instalar seleccionados"))
		self.closeBtn = wx.Button(panel, label=_("&Cerrar"))
		btnSizer.Add(self.installBtn, 1, wx.ALL, 10)
		btnSizer.Add(self.closeBtn, 1, wx.ALL, 10)
		mainSizer.Add(btnSizer, 0, wx.EXPAND)
		panel.SetSizer(mainSizer)
		self.CenterOnScreen()

		self.selectAllBtn.Bind(wx.EVT_BUTTON, self.onSelectAll)
		self.deselectAllBtn.Bind(wx.EVT_BUTTON, self.onDeselectAll)
		self.installBtn.Bind(wx.EVT_BUTTON, self.onInstall)
		self.closeBtn.Bind(wx.EVT_BUTTON, self.onClose)
		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)
		Thread(target=self._hiloBusqueda, daemon=True).start()

	def _hiloBusqueda(self):
		wx.CallAfter(ui.message, _("Buscando mejores versiones en los servidores..."))
		try:
			clientES = basedatos.NVDAStoreClient()
			addonsOficial = tienda_oficial.obtener_complementos_oficiales(includeIncompatible=ajustes.tempAllowIncompatible)

			for b_addon in self.backup_data.get('addons', []):
				name = b_addon['name'].lower()
				summary = b_addon['summary']
				idx_es = clientES.indiceName(name)
				addon_es = clientES.dataServidor[idx_es] if idx_es is not None else None
				addon_of = next((a for a in addonsOficial if a.addonId.lower() == name), None)

				mejor = None
				fuente = ""
				if addon_es and addon_of:
					v_es = addon_es['links'][0]['version']
					v_of = addon_of.addonVersionName
					try:
						if version_utils.parse(v_of) >= version_utils.parse(v_es):
							mejor = addon_of
							fuente = "oficial"
						else:
							mejor = addon_es
							fuente = "nvda_es"
					except:
						mejor = addon_of
						fuente = "oficial"
				elif addon_es:
					mejor = addon_es
					fuente = "nvda_es"
				elif addon_of:
					mejor = addon_of
					fuente = "oficial"
				wx.CallAfter(self._agregarAddonEncontrado, mejor, fuente, name, summary)
			wx.CallAfter(ui.message, _("Búsqueda de backup finalizada."))
		except Exception as e:
			log.error(f"Error en hilo de búsqueda de backup: {e}")
			wx.CallAfter(ui.message, _("Error al procesar el backup"))

	def _agregarAddonEncontrado(self, mejor, fuente, name, summary):
		def agregar():
			if mejor:
				v_desc = mejor.addonVersionName if fuente == "oficial" else mejor['links'][0]['version']
				self.addons_encontrados.append((fuente, mejor, name))
				idx = self.checkList.Append(f"{summary} ({v_desc}) [{fuente}]")
				self.checkList.Check(idx, True)
			else:
				self.checkList.Append(f"{summary} " + _("(No encontrado en servidores)"))
				self.addons_encontrados.append((None, None, name))
			if self.checkList.GetSelection() == -1 and self.checkList.GetCount() > 0:
				self.checkList.SetSelection(0)
				self.onSeleccion(None)
		wx.CallAfter(agregar)

	def onSeleccion(self, event):
		sel = self.checkList.GetSelection()
		if sel == -1 or sel >= len(self.addons_encontrados):
			return
		fuente, addon, b_name = self.addons_encontrados[sel]
		if not addon:
			self.txtInfo.SetValue(_("Este complemento no se ha encontrado en los servidores actuales."))
			return
		if fuente == "nvda_es":
			ficha = _("FUENTE: NVDA.ES\n")
			ficha += "========================================\n"
			ficha += _("Nombre: {}\n").format(addon['summary'])
			ficha += _("ID: {}\n").format(addon['name'])
			ficha += _("Versión disponible: {}\n").format(addon['links'][0]['version'])
			ficha += _("Autor: {}\n").format(addon['author'])
			ficha += "\n" + _("Descripción:") + "\n"
			ficha += "----------------------------------------\n"
			ficha += (addon['description'] or _("Sin descripción.")) + "\n"
		else:
			ficha = _("FUENTE: TIENDA OFICIAL\n")
			ficha += "========================================\n"
			ficha += _("Nombre: {}\n").format(addon.displayName)
			ficha += _("ID: {}\n").format(addon.addonId)
			ficha += _("Versión disponible: {}\n").format(addon.addonVersionName)
			ficha += _("Editor: {}\n").format(addon.publisher)
			ficha += "\n" + _("Descripción:") + "\n"
			ficha += "----------------------------------------\n"
			ficha += (addon.description or _("Sin descripción.")) + "\n"
		self.txtInfo.SetValue(ficha)
		self.txtInfo.SetInsertionPoint(0)

	def onSelectAll(self, event):
		for i in range(self.checkList.GetCount()):
			self.checkList.Check(i, True)

	def onDeselectAll(self, event):
		for i in range(self.checkList.GetCount()):
			self.checkList.Check(i, False)

	def onInstall(self, event):
		seleccionados = [i for i in range(self.checkList.GetCount()) if self.checkList.IsChecked(i)]
		if not seleccionados:
			gui.messageBox(_("Seleccione al menos un complemento."), _("Aviso"), wx.ICON_WARNING)
			return

		incompatibles = []
		for i in seleccionados:
			fuente, addon, b_name = self.addons_encontrados[i]
			if not addon:
				continue
			compatible = True
			if fuente == "oficial":
				compatible = addon.isCompatible
			else:
				minNVDA = addon['links'][0].get('minimum')
				lastTested = addon['links'][0].get('lasttested')
				if minNVDA and lastTested:
					try:
						compatible = version_utils.isAddonCompatible(
							version_utils.getAPIVersionTupleFromString(minNVDA),
							version_utils.getAPIVersionTupleFromString(lastTested)
						)
					except:
						pass
			if not compatible:
				name = (addon.displayName if fuente == "oficial" else addon['summary'])
				incompatibles.append(name)

		if incompatibles:
			msg = _("Los siguientes complementos no son compatibles:\n\n%s\n\n¿Desea intentar instalarlos de todos modos?") % "\n".join(incompatibles)
			if gui.messageBox(msg, _("Advertencia"), wx.YES_NO | wx.ICON_WARNING) == wx.NO:
				return

		nombreUrl = {}
		indices = []
		for idx, i in enumerate(seleccionados):
			fuente, addon, b_name = self.addons_encontrados[i]
			if not addon:
				continue
			if fuente == "oficial":
				nombreUrl[addon.displayName] = addon.URL
			else:
				clientES = basedatos.NVDAStoreClient()
				url = clientES.urlBase + addon['links'][0]['file']
				nombreUrl[addon['summary']] = url
			indices.append(idx)

		if not nombreUrl:
			return

		self.Hide()
		dlg = ActualizacionDialogo(gui.mainFrame, nombreUrl, indices, 15, allowIncompatible=bool(incompatibles))
		gui.mainFrame.prePopup()
		dlg.ShowModal()
		dlg.Destroy()
		self.onClose(None)

	def onClose(self, event):
		ajustes.IS_WinON = False
		self.Destroy()
		gui.mainFrame.postPopup()

	def onKeyPress(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.onClose(None)
		else:
			event.Skip()
