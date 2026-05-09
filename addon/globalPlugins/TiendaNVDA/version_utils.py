# -*- coding: utf-8 -*-
# Copyright (C) 2021-2025 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.
#
# Módulo de utilidades de versión - Reemplazo ligero de packaging.version
# Solo implementa lo necesario: parseo y comparación de versiones PEP 440
#

import re
from typing import Tuple, Optional
import addonAPIVersion

ADDON_API_VERSION_REGEX = re.compile(r"^(0|\d{4})\.(\d+)(?:\.(\d+))?$")

# Regex PEP 440 simplificado
_VERSION_PATTERN = re.compile(
	r"^\s*v?"
	r"(?:(?P<epoch>\d+)!)?"
	r"(?P<release>\d+(?:\.\d+)*)"
	r"(?:[-_.]?(?P<pre>(?:a|alpha|b|beta|c|rc|preview)[-_.]?\d*))"
	r"?(?:[-_.]?(?:post|rev|r)[-_.]?(?P<post>\d*))?"
	r"(?:[-_.]?dev[-_.]?(?P<dev>\d*))?"
	r"(?:\+(?P<local>[a-z0-9]+(?:[-_.][a-z0-9]+)*))?"
	r"\s*$",
	re.IGNORECASE
)


class InvalidVersion(ValueError):
	"""Versión no válida según PEP 440"""
	pass


class Version:
	"""Versión PEP 440 simplificada con soporte de comparación"""

	def __init__(self, version_str: str):
		self._original = version_str
		match = _VERSION_PATTERN.match(version_str)
		if not match:
			# Intentar parseo simple de versiones tipo "2024.1.0" o "1.2.3"
			simple = re.match(r"^\s*v?(\d+(?:\.\d+)*)\s*$", version_str)
			if simple:
				self.epoch = 0
				self.release = tuple(int(x) for x in simple.group(1).split("."))
				self.pre = None
				self.post = None
				self.dev = None
				self.local = None
			else:
				raise InvalidVersion(f"Versión no válida: {version_str}")
		else:
			self.epoch = int(match.group("epoch")) if match.group("epoch") else 0
			self.release = tuple(int(x) for x in match.group("release").split("."))
			self.pre = self._parse_pre(match.group("pre"))
			self.post = self._parse_numeric(match.group("post"))
			self.dev = self._parse_numeric(match.group("dev"))
			self.local = match.group("local")

	@staticmethod
	def _parse_pre(pre_str: Optional[str]) -> Optional[Tuple[str, int]]:
		if not pre_str:
			return None
		m = re.match(r"(a|alpha|b|beta|c|rc|preview)[-_.]?(\d*)", pre_str, re.IGNORECASE)
		if not m:
			return None
		kind = m.group(1).lower()
		num = int(m.group(2)) if m.group(2) else 0
		# Normalizar
		if kind in ("a", "alpha"):
			kind = "a"
		elif kind in ("b", "beta"):
			kind = "b"
		elif kind in ("c", "rc", "preview"):
			kind = "rc"
		return (kind, num)

	@staticmethod
	def _parse_numeric(val: Optional[str]) -> Optional[int]:
		if val is None:
			return None
		return int(val) if val else 0

	def _cmp_key(self):
		"""Genera una clave de comparación"""
		# pre: a < b < rc < release (None = release)
		pre_order = {"a": 0, "b": 1, "rc": 2}
		if self.pre:
			pre_key = (pre_order.get(self.pre[0], 0), self.pre[1])
		else:
			pre_key = (3, 0)  # release > cualquier pre

		post_key = self.post if self.post is not None else -1
		dev_key = self.dev if self.dev is not None else float('inf')

		return (self.epoch, self.release, pre_key, post_key, dev_key)

	def __repr__(self):
		return f"Version('{self._original}')"

	def __str__(self):
		return self._original

	def __eq__(self, other):
		if not isinstance(other, Version):
			return NotImplemented
		return self._cmp_key() == other._cmp_key()

	def __lt__(self, other):
		if not isinstance(other, Version):
			return NotImplemented
		return self._cmp_key() < other._cmp_key()

	def __le__(self, other):
		if not isinstance(other, Version):
			return NotImplemented
		return self._cmp_key() <= other._cmp_key()

	def __gt__(self, other):
		if not isinstance(other, Version):
			return NotImplemented
		return self._cmp_key() > other._cmp_key()

	def __ge__(self, other):
		if not isinstance(other, Version):
			return NotImplemented
		return self._cmp_key() >= other._cmp_key()

	def __ne__(self, other):
		if not isinstance(other, Version):
			return NotImplemented
		return self._cmp_key() != other._cmp_key()


def parse(version_str: str) -> Version:
	"""Parsea una cadena de versión y devuelve un objeto Version comparable"""
	return Version(version_str)


def getAPIVersionTupleFromString(version_str: str) -> Tuple[int, ...]:
	"""Convierte una cadena de versión NVDA a tupla (year, major, minor)"""
	match = ADDON_API_VERSION_REGEX.match(version_str)
	if not match:
		raise ValueError(version_str)
	return tuple(int(i) if i is not None else 0 for i in match.groups())


def hasAddonGotRequiredSupport(addonMin, currentAPIVersion=addonAPIVersion.CURRENT) -> bool:
	return addonMin <= currentAPIVersion


def isAddonTested(addonMax, backwardsCompatToVersion=addonAPIVersion.BACK_COMPAT_TO) -> bool:
	return addonMax >= backwardsCompatToVersion


def isAddonCompatible(
		addonMin,
		addonMax,
		currentAPIVersion=addonAPIVersion.CURRENT,
		backwardsCompatToVersion=addonAPIVersion.BACK_COMPAT_TO
) -> bool:
	return hasAddonGotRequiredSupport(addonMin, currentAPIVersion) and isAddonTested(addonMax, backwardsCompatToVersion)
