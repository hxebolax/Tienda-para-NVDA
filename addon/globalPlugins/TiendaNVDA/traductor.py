# -*- coding: utf-8 -*-
# Copyright (C) 2021-2025 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.
#
# Módulo de traducción - Usa Google Translate vía requests
# Escrito desde cero como módulo único
#

import re
import html
import requests
from logHandler import log

_AGENT = {
	'User-Agent': (
		'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; '
		'SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'
	)
}

_BASE_URL = "http://translate.google.com/m?tl={}&sl={}&q={}"


def translate(text: str, to_language: str = "auto", from_language: str = "auto") -> str:
	"""
	Traduce texto usando Google Translate.
	
	Args:
		text: Texto a traducir
		to_language: Código de idioma destino (ej: 'es', 'en', 'fr')
		from_language: Código de idioma origen ('auto' para detección automática)
	
	Returns:
		Texto traducido o cadena vacía si falla
	"""
	if not text or not text.strip():
		return ""

	try:
		encoded_text = requests.utils.quote(text)
		url = _BASE_URL.format(to_language, from_language, encoded_text)
		response = requests.get(url, headers=_AGENT, timeout=15)
		response.raise_for_status()
		data = response.text
		# Buscar el resultado en el HTML
		results = re.findall(r'(?s)class="(?:t0|result-container)">(.*?)<', data)
		if results:
			return html.unescape(results[0])
		return ""
	except Exception as e:
		log.debug(f"Error al traducir: {e}")
		return ""
