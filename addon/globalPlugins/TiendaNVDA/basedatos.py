import addonHandler
import json
import urllib.request
import funciones
import ajustes

class JsonNVDAes():
	def __init__(self):
		super(JsonNVDAes, self).__init__()

		opener = urllib.request.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		self.dataServidor = json.loads(opener.open('https://nvda.es/files/get.php?addonslist').read().decode("utf-8"))
		self.dataLocal = list(addonHandler.getAvailableAddons())
		self.urlBase = "https://nvda.es/files/get.php?file="

	def indiceName(self, valor):
		for x in range(0, len(self.dataServidor)):
			if self.dataServidor[x]['name'].lower() == valor.lower():
				return x
		return False

	def indiceSummary(self, valor):
		for x in range(0, len(self.dataServidor)):
			if self.dataServidor[x]['summary'].lower() == valor.lower():
				return x
		return False

	def obtenerNameLocal(self, valor):
		for i in self.dataLocal:
			if i.manifest["summary"].lower() == valor.lower():
				p = i.manifest["name"]
		return p

	def nombrEntero(self, orden = False):
		lista = []
		for i in range(0, len(self.dataServidor)):
			lista.append(self.dataServidor[i]['summary'])
		if orden == False:
			return lista
		else:
			lista.sort()
			return lista

	def listaComplementosInstalados(self):
		lista1 = []
		lista2 = []
		for i in self.dataLocal:
			for x in range(0, len(self.dataServidor)):
				if i.manifest["name"].lower() == self.dataServidor[x]['name'].lower():
					lista1.append(i.manifest["summary"])
					lista2.append(self.dataServidor[x]['links'][0]['channel'])
		return dict(zip(lista1, lista2))

	def chkActualizaS(self):
		lstActualizar = []
		lstUrl = []
		lstVerServidor = []
		lstVerLocal = []
		for i in self.dataLocal:
			for x in range(0, len(self.dataServidor)):
				if self.dataServidor[x]['name'].lower() == i.manifest["name"].lower():
					canal = ajustes.listaComplementos.get(i.manifest["summary"])
					for z in range(len(self.dataServidor[x]['links'])):
						if self.dataServidor[x]['links'][z]['channel'].lower() == canal.lower():
							if funciones.chkVersion(self.dataServidor[x]['links'][z]['version'], i.manifest["version"]) == True:
								lstActualizar.append("{}".format(i.manifest["summary"]))
								lstUrl.append(self.urlBase + self.dataServidor[x]['links'][z]['file'])
								lstVerServidor.append(self.dataServidor[x]['links'][z]['version'])
								lstVerLocal.append(i.manifest["version"])
		if len(lstActualizar) == 0:
			return False, False, False
		else:
			return dict(zip(lstActualizar, lstUrl)), lstVerLocal, lstVerServidor
