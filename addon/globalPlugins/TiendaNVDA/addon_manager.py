# -*- coding: utf-8 -*-
# Copyright (C) 2021-2025 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.
#
# Módulo de gestión de complementos instalados
#

import addonHandler
from addonHandler import state, AddonStateCategory
from logHandler import log
import time
import os
import json
from typing import Optional, List, Dict, Any, Tuple
from . import version_utils

addonHandler.initTranslation()


class AddonManager:
	"""Gestiona acciones avanzadas sobre los complementos instalados"""

	_installedCache = None
	_lastCacheTime = 0
	CACHE_TTL = 2

	@staticmethod
	def refreshCache():
		AddonManager._installedCache = None
		AddonManager._lastCacheTime = 0

	@staticmethod
	def getInstalledAddonsDict() -> Dict[str, Any]:
		currentTime = time.time()
		if AddonManager._installedCache is not None and (currentTime - AddonManager._lastCacheTime) < AddonManager.CACHE_TTL:
			return AddonManager._installedCache
		installed = {}
		for addon in addonHandler.getAvailableAddons():
			name_lower = addon.manifest['name'].lower()
			installed[name_lower] = {
				'version': addon.manifest['version'],
				'summary': addon.manifest['summary'],
				'description': addon.manifest['description'],
				'author': addon.manifest['author'],
				'isDisabled': addon.isDisabled,
				'isPendingRemove': addon.isPendingRemove,
				'isPendingInstall': addon.isPendingInstall,
				'isCompatible': getattr(addon, 'isCompatible', True),
				'isBlocked': getattr(addon, 'isBlocked', False),
				'overrideIncompatibility': getattr(addon, 'overrideIncompatibility', False),
				'canOverrideCompatibility': getattr(addon, 'canOverrideCompatibility', False),
				'obj': addon,
				'realName': addon.manifest['name']
			}
		AddonManager._installedCache = installed
		AddonManager._lastCacheTime = currentTime
		return installed

	@staticmethod
	def getSnapshot() -> Dict[str, Tuple[str, bool, bool, bool]]:
		return {
			addon.manifest['name'].lower(): (
				addon.manifest['version'], addon.isDisabled,
				addon.isPendingRemove, getattr(addon, 'isBlocked', False)
			)
			for addon in addonHandler.getAvailableAddons()
		}

	@staticmethod
	def hasChanged(initialSnapshot: Dict) -> bool:
		return AddonManager.getSnapshot() != initialSnapshot

	@staticmethod
	def disableAddon(name: str) -> bool:
		name_lower = name.lower()
		for addon in addonHandler.getAvailableAddons():
			if addon.manifest['name'].lower() == name_lower:
				addon.enable(False)
				return True
		return False

	@staticmethod
	def enableAddon(name: str, override: bool = False) -> bool:
		name_lower = name.lower()
		for addon in addonHandler.getAvailableAddons():
			if addon.manifest['name'].lower() == name_lower:
				hasOverride = addon.name in state[AddonStateCategory.OVERRIDE_COMPATIBILITY]
				try:
					hasPendingOverride = addon.name in state[AddonStateCategory.PENDING_OVERRIDE_COMPATIBILITY]
				except (KeyError, AttributeError):
					hasPendingOverride = False
				if not addon.isCompatible:
					if hasOverride or hasPendingOverride:
						pass
					elif override:
						canOverride = getattr(addon, 'canOverrideCompatibility', False)
						if canOverride:
							try:
								if hasattr(addon, 'enableCompatibilityOverride'):
									addon.enableCompatibilityOverride()
								else:
									state[AddonStateCategory.PENDING_OVERRIDE_COMPATIBILITY].add(addon.name)
									state[AddonStateCategory.BLOCKED].discard(addon.name)
									state[AddonStateCategory.DISABLED].discard(addon.name)
								state.save()
							except RuntimeError:
								pass
						else:
							raise addonHandler.AddonError(f"Cannot override compatibility for {addon.name}")
					else:
						raise addonHandler.AddonError(f"Add-on {addon.name} is not compatible")
				addon.enable(True)
				return True
		return False

	@staticmethod
	def installAddon(path: str, silent: bool = False) -> bool:
		try:
			from gui import addonGui
			if silent:
				try:
					bundle = addonHandler.AddonBundle(path)
					addonHandler.installAddonBundle(bundle)
				except (AttributeError, TypeError):
					with open(path, "rb") as f:
						addonHandler.installAddonBundle(f)
				return True
			else:
				addonGui.handleRemoteAddonInstall(path)
				return True
		except Exception as e:
			log.error(f"Error al instalar complemento {path}: {e}")
			return False

	@staticmethod
	def uninstallAddon(name: str) -> bool:
		name_lower = name.lower()
		for addon in addonHandler.getAvailableAddons():
			if addon.manifest['name'].lower() == name_lower:
				addon.requestRemove()
				return True
		return False

	@staticmethod
	def createBackup(path: str = None, dirDatos: str = None) -> str:
		installed = AddonManager.getInstalledAddonsDict()
		backup_data = {
			'date': time.strftime("%Y-%m-%d %H:%M:%S"),
			'addons': [
				{'name': v['realName'], 'version': v['version'], 'summary': v['summary']}
				for n, v in installed.items()
			]
		}
		backup_file = path if path else os.path.join(dirDatos or "", "addons_backup.json")
		with open(backup_file, "w", encoding="utf-8") as f:
			json.dump(backup_data, f, ensure_ascii=False, indent=2)
		return backup_file

	@staticmethod
	def getIndicatorExplanation(indicator: str, source: str = "") -> str:
		explanations = {
			"[I]": _("El complemento está instalado y activo."),
			"[U]": _("Hay una actualización disponible para este complemento."),
			"[U-I]": _("Hay una actualización disponible pero no es compatible con su versión de NVDA."),
			"[D]": _("El complemento está instalado pero deshabilitado."),
			"[R]": _("El complemento está pendiente de eliminar. Requiere reiniciar NVDA."),
			"[I-I]": _("El complemento está instalado pero bloqueado por incompatibilidad con su versión de NVDA."),
			"[X]": _("El complemento no es compatible con su versión de NVDA y no está instalado."),
			"": _("El complemento no está instalado.")
		}
		explanation = explanations.get(indicator, _("Estado desconocido."))
		if source:
			source_info = {
				"nvda_es": _("Fuente: Tienda NVDA.ES (comunidad hispana)"),
				"oficial": _("Fuente: Tienda Oficial de NVDA"),
				"unificada": _("Fuente: Tienda Unificada de Complementos")
			}
			source_text = source_info.get(source, "")
			if source_text:
				explanation = f"{explanation}\n{source_text}"
		return explanation

	@staticmethod
	def getAddonStatusIndicator(name: str, serverVersion: str = None, minNVDA: str = None, lastTested: str = None, installedDict: Dict = None) -> str:
		installed = installedDict if installedDict is not None else AddonManager.getInstalledAddonsDict()
		name_lower = name.lower()
		is_installed = name_lower in installed
		if is_installed:
			addon = installed[name_lower]
			if addon['isPendingRemove']:
				return "[R]"
			if addon.get('isBlocked', False):
				return "[I-I]"
			if addon['isDisabled']:
				return "[D]"
			if not serverVersion:
				return "[I]"
			try:
				v_server = version_utils.parse(serverVersion)
				v_local = version_utils.parse(addon['version'])
				if v_server > v_local:
					if minNVDA and lastTested:
						try:
							if not version_utils.isAddonCompatible(
								version_utils.getAPIVersionTupleFromString(minNVDA),
								version_utils.getAPIVersionTupleFromString(lastTested)
							):
								return "[U-I]"
						except:
							pass
					return "[U]"
				elif v_server == v_local:
					return "[I]"
				else:
					return ""
			except:
				return "[I]"
		if not is_installed and minNVDA and lastTested:
			try:
				if not version_utils.isAddonCompatible(
					version_utils.getAPIVersionTupleFromString(minNVDA),
					version_utils.getAPIVersionTupleFromString(lastTested)
				):
					return "[X]"
			except:
				pass
		return ""

	@staticmethod
	def checkDependencies(manifest: Dict) -> List[str]:
		missing = []
		deps = manifest.get('dependencies')
		if deps:
			installed = AddonManager.getInstalledAddonsDict()
			for dep in deps:
				if dep not in installed:
					missing.append(dep)
		return missing

	@staticmethod
	def getOrphanedAddons(serverAddonNames: List[str]) -> List[Dict]:
		installed = AddonManager.getInstalledAddonsDict()
		orphans = []
		server_set = set(n.lower() for n in serverAddonNames)
		for name, addon in installed.items():
			if name.lower() not in server_set:
				orphans.append(addon)
		return orphans
