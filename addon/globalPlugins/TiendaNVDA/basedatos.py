# -*- coding: utf-8 -*-
# Copyright (C) 2021 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import addonHandler
import json
import urllib.request
import os, sys
from threading import Timer

def obtenFile(url):
	opener = urllib.request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	p = urllib.request.urlopen(url)
	fichero = p.headers.get_filename()
	nombreFile = os.path.splitext(fichero)[0]
	return nombreFile

def obtenFileAlt(url):
	opener = urllib.request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	urllib.request.install_opener(opener)
	p = urllib.request.urlopen(url)
	fichero = p.headers.get_filename()
	nombreFile = os.path.splitext(fichero)[0]
	return nombreFile

class NVDAStoreClient(object):
	def __init__(self):
		super(NVDAStoreClient, self).__init__()

		self.opener = urllib.request.build_opener()
		self.opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		urllib.request.install_opener(self.opener)
		self.dataServidor = json.loads(self.opener.open('https://nvda.es/files/get.php?addonslist').read().decode("utf-8"))
		self.urlBase = "https://nvda.es/files/get.php?file="
		self.dataLocal = list(addonHandler.getAvailableAddons())

	def GetFilenameDownload(self, valor):
		for x in range(0, len(self.dataServidor)):
			num = len(self.dataServidor[x]['links'])
			for i in range(num):
				if self.dataServidor[x]['links'][i]['file'] == valor:
					temp = self.dataServidor[x]['links'][i]['link']
					return os.path.basename(temp)

	def GetLinkDownload(self, valor):
		for x in range(0, len(self.dataServidor)):
			num = len(self.dataServidor[x]['links'])
			for i in range(num):
				if self.dataServidor[x]['links'][i]['file'] == valor:
					return self.dataServidor[x]['links'][i]['link']

	def indiceSummary(self, valor):
		for x in range(0, len(self.dataServidor)):
			if self.dataServidor[x]['summary'].lower() == valor.lower():
				return x
		return False

	def chkVersion(self, verServidor, verLocal):
		if (verServidor > verLocal) - (verServidor < verLocal)  == -1 or  (verServidor > verLocal) - (verServidor < verLocal)  == 0:
			return False
		else:
			return True

	def chkActualizaS(self):
		lstActualizar = []
		lstUrl = []
		lstVerServidor = []
		lstVerLocal = []
		for i in self.dataLocal:
			for x in range(0, len(self.dataServidor)):
				if self.dataServidor[x]['name'].lower() == i.manifest["name"].lower():
					if self.chkVersion(self.dataServidor[x]['links'][0]['version'], i.manifest["version"]) == True:
						lstActualizar.append("{}".format(i.manifest["summary"]))
						lstUrl.append(self.urlBase + self.dataServidor[x]['links'][0]['file'])
						lstVerServidor.append(self.dataServidor[x]['links'][0]['version'])
						lstVerLocal.append(i.manifest["version"])
		if len(lstActualizar) == 0:
			return False, False, False
		else:
			return dict(zip(lstActualizar, lstUrl)), lstVerLocal, lstVerServidor

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

