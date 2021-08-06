# -*- coding: utf-8 -*-
# Copyright (C) 2020 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import globalVars
import addonHandler
import wx
import os
import sys
import shutil

# For translation
addonHandler.initTranslation()

dir = addonHandler._getDefaultAddonPaths()
dirDatos =os.path.join(globalVars.appArgs.configPath, "TiendaNVDA")
if os.path.exists(dirDatos) == False:
	os.mkdir(dirDatos)
else:
	try:
		shutil.rmtree(dirDatos, ignore_errors=True)
		os.mkdir(dirDatos)
	except:
		pass

IS_WinON = False
focoActual = "listboxComplementos"
ID_TRUE = wx.NewIdRef() # para botón aceptar
ID_FALSE = wx.NewIdRef() # para botón cancelar

### Diccionario para el foco.
id_widgets = {
# WidGets generales
	1:"Panel",
	2:"textoBusqueda",
	3:"listboxComplementos",
	4:"txtResultado",
# Botones
	201:"descargarBTN",
	202:"paginaWebBTN",
	203:"salirBTN",
}
