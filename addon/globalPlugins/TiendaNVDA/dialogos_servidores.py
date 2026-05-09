# -*- coding: utf-8 -*-
# Copyright (C) 2021-2025 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.
#
# Diálogos de gestión de servidores
#

import addonHandler
import globalVars
import gui
import ui
import wx
import os
from . import ajustes
from . import basedatos
from . import red

addonHandler.initTranslation()


class GestorServidores(wx.Dialog):
	def __init__(self):
		super().__init__(None, -1, title=_("Gestor de servidores de complementos"))
		self.SetSize((400, 300))
		panel = wx.Panel(self)
		sizer = wx.BoxSizer(wx.VERTICAL)
		label = wx.StaticText(panel, label=_("&Lista de servidores:"))
		sizer.Add(label, 0, wx.EXPAND | wx.ALL, 5)
		self.listBox = wx.ListBox(panel, choices=[
			ajustes.listaServidores[i][0] for i in range(len(ajustes.listaServidores))
		])
		sizer.Add(self.listBox, 1, wx.EXPAND | wx.ALL, 5)
		self.listBox.SetSelection(0)
		btnSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.addBtn = wx.Button(panel, label=_("&Añadir"))
		self.editBtn = wx.Button(panel, label=_("&Editar"))
		self.deleteBtn = wx.Button(panel, label=_("&Borrar"))
		btnSizer.Add(self.addBtn, 1, wx.ALL, 5)
		btnSizer.Add(self.editBtn, 1, wx.ALL, 5)
		btnSizer.Add(self.deleteBtn, 1, wx.ALL, 5)
		sizer.Add(btnSizer, 0, wx.EXPAND)
		self.closeBtn = wx.Button(panel, wx.ID_CLOSE, _("&Cerrar"))
		sizer.Add(self.closeBtn, 0, wx.ALIGN_CENTER | wx.ALL, 5)
		panel.SetSizer(sizer)
		self.CenterOnScreen()
		self.addBtn.Bind(wx.EVT_BUTTON, self.onAdd)
		self.editBtn.Bind(wx.EVT_BUTTON, self.onEdit)
		self.deleteBtn.Bind(wx.EVT_BUTTON, self.onDelete)
		self.closeBtn.Bind(wx.EVT_BUTTON, self.onClose)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)

	def onAdd(self, event):
		dlg = AnadirEditar(self, 0)
		if dlg.ShowModal() == 0:
			num = len(ajustes.listaServidores) + 1
			ajustes.listaServidores.append([dlg.nombreText.GetValue(), dlg.urlText.GetValue(), f"data{num}.json"])
			basedatos.ServidoresComplementos().fileJsonAddon(1, ajustes.listaServidores)
			self._refreshList()
		dlg.Destroy()

	def onEdit(self, event):
		sel = self.listBox.GetSelection()
		if sel == 0:
			ui.message(_("El servidor de la comunidad hispanohablante no puede ser editado."))
			return
		dlg = AnadirEditar(self, 1, ajustes.listaServidores[sel])
		if dlg.ShowModal() == 0:
			ficheroJson = ajustes.listaServidores[sel][2]
			ajustes.listaServidores[sel] = [dlg.nombreText.GetValue(), dlg.urlText.GetValue(), ficheroJson]
			basedatos.ServidoresComplementos().fileJsonAddon(1, ajustes.listaServidores)
			self._refreshList()
		dlg.Destroy()

	def onDelete(self, event):
		sel = self.listBox.GetSelection()
		if sel == 0:
			ui.message(_("El servidor de la comunidad hispanohablante no puede ser borrado."))
			return
		msg = _("¿Está seguro que desea borrar el servidor: {}?").format(self.listBox.GetString(sel))
		if wx.MessageBox(msg, _("Confirmar"), wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
			ficheroJson = ajustes.listaServidores[sel][2]
			del ajustes.listaServidores[sel]
			basedatos.ServidoresComplementos().fileJsonAddon(1, ajustes.listaServidores)
			try:
				os.remove(os.path.join(globalVars.appArgs.configPath, "TiendaNVDA_Modern", ficheroJson))
			except:
				pass
			self._refreshList()

	def _refreshList(self):
		self.listBox.Clear()
		self.listBox.Append([ajustes.listaServidores[i][0] for i in range(len(ajustes.listaServidores))])
		self.listBox.SetSelection(min(len(ajustes.listaServidores) - 1, self.listBox.GetSelection()))
		self.listBox.SetFocus()

	def onKeyPress(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.EndModal(0)
		else:
			event.Skip()

	def onClose(self, event):
		self.EndModal(0)


class AnadirEditar(wx.Dialog):
	def __init__(self, parent, opcion, datos=None):
		title = _("Añadir servidor") if opcion == 0 else _("Editar servidor")
		super().__init__(parent, title=title)
		self.opcion = opcion
		panel = wx.Panel(self)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(wx.StaticText(panel, label=_("&Nombre del servidor:")), 0, wx.ALL, 5)
		self.nombreText = wx.TextCtrl(panel)
		sizer.Add(self.nombreText, 0, wx.EXPAND | wx.ALL, 5)
		sizer.Add(wx.StaticText(panel, label=_("&URL del servidor:")), 0, wx.ALL, 5)
		self.urlText = wx.TextCtrl(panel)
		sizer.Add(self.urlText, 0, wx.EXPAND | wx.ALL, 5)
		btnSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.okBtn = wx.Button(panel, wx.ID_OK, _("&Aceptar"))
		self.cancelBtn = wx.Button(panel, wx.ID_CANCEL, _("&Cancelar"))
		btnSizer.Add(self.okBtn, 1, wx.ALL, 5)
		btnSizer.Add(self.cancelBtn, 1, wx.ALL, 5)
		sizer.Add(btnSizer, 0, wx.ALIGN_CENTER)
		panel.SetSizer(sizer)
		self.Fit()
		self.CenterOnScreen()
		if datos:
			self.nombreText.SetValue(datos[0])
			self.urlText.SetValue(datos[1])
		self.okBtn.Bind(wx.EVT_BUTTON, self.onOk)
		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)

	def onOk(self, event):
		if not self.nombreText.GetValue().strip():
			ui.message(_("El nombre del servidor no puede estar vacío."))
			self.nombreText.SetFocus()
			return
		if not self.urlText.GetValue().strip():
			ui.message(_("La URL del servidor no puede estar vacía."))
			self.urlText.SetFocus()
			return
		nombres = [ajustes.listaServidores[i][0] for i in range(len(ajustes.listaServidores))]
		if self.opcion == 0 and self.nombreText.GetValue() in nombres:
			ui.message(_("Ya existe un servidor con ese nombre."))
			return
		if not red.check_json(self.urlText.GetValue()):
			ui.message(_("La URL introducida no es válida."))
			return
		self.EndModal(0)

	def onKeyPress(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.EndModal(1)
		else:
			event.Skip()


class SinComplementos(wx.Dialog):
	def __init__(self, parent):
		super().__init__(parent, title=_("Servidor sin complementos"), size=(450, 150))
		ajustes.IS_WinON = True
		panel = wx.Panel(self)
		sizer = wx.BoxSizer(wx.VERTICAL)
		resultados = [ajustes.listaServidores[i][0] for i in range(len(ajustes.listaServidores))]
		self.choice = wx.Choice(panel, choices=[_("Seleccione un servidor")] + resultados)
		self.choice.SetSelection(0)
		sizer.Add(self.choice, 0, wx.EXPAND | wx.ALL, 10)
		btnSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.okBtn = wx.Button(panel, label=_("&Aceptar"))
		self.closeBtn = wx.Button(panel, label=_("&Cerrar"))
		btnSizer.Add(self.okBtn, 1, wx.ALL, 5)
		btnSizer.Add(self.closeBtn, 1, wx.ALL, 5)
		sizer.Add(btnSizer, 0, wx.ALIGN_CENTER)
		panel.SetSizer(sizer)
		self.CenterOnScreen()
		self.okBtn.Bind(wx.EVT_BUTTON, self.onOk)
		self.closeBtn.Bind(wx.EVT_BUTTON, self.onClose)

	def onOk(self, event):
		if self.choice.GetSelection() == 0:
			gui.messageBox(_("Debe seleccionar un servidor."), _("Información"), wx.ICON_INFORMATION)
			return
		ajustes.IS_WinON = False
		sel = self.choice.GetSelection() - 1
		ajustes.selectSRV = sel
		ajustes.urlServidor = ajustes.listaServidores[sel][1]
		ajustes.setConfig("urlServidor", ajustes.urlServidor)
		ajustes.setConfig("selectSRV", sel)
		ajustes.listaAddonsSave = basedatos.libreriaLocal(ajustes.listaServidores[sel][2]).fileJsonAddon(2)
		self.Destroy()
		gui.mainFrame.postPopup()
		from .hilos import HiloComplemento
		HiloComplemento(1, "nvda_es").start()

	def onClose(self, event):
		ajustes.IS_WinON = False
		self.Destroy()
		gui.mainFrame.postPopup()
