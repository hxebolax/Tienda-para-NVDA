from urllib.request import urlopen, urlretrieve, build_opener, install_opener
import os

def  obtenerNombreArchivo(url):
	opener = build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	install_opener(opener)
	p = urlopen(url)
	fichero = p.headers.get_filename()
	nombre = os.path.splitext(fichero)[0]
	return 	nombre, p

def chkVersion(verServidor, verLocal):
	if (verServidor > verLocal) - (verServidor < verLocal)  == -1 or  (verServidor > verLocal) - (verServidor < verLocal)  == 0:
		return False
	else:
		return True
