# -*- coding: UTF-8 -*-

# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.


# Since some strings in `addon_info` are translatable,
# we need to include them in the .po files.
# Gettext recognizes only strings given as parameters to the `_` function.
# To avoid initializing translations in this module we simply roll our own "fake" `_` function
# which returns whatever is given to it as an argument.
def _(arg):
	return arg


# Add-on information variables
addon_info = {
	# add-on Name/identifier, internal for NVDA
	"addon_name": "TiendaNVDA",
	# Add-on summary, usually the user visible name of the addon.
	# Translators: Summary for this add-on
	# to be shown on installation and add-on information found in Add-ons Manager.
	"addon_summary": _("Tienda para NVDA.ES"),
	# Add-on description
	# Translators: Long description to be shown for this add-on on add-on information from add-ons manager
	"addon_description": _("Tienda de complementos no oficial de https://www.nvda.es"),
	# version
	"addon_version": "0.5.1",
	# Author(s)
	"addon_author": u"Héctor J. Benítez Corredera <xebolax@gmail.com>",
	# URL for the add-on documentation support
	"addon_url": "https://github.com/hxebolax/Tienda-para-NVDA",
	# Documentation file name
	"addon_docFileName": "readme.html",
	# Minimum NVDA version supported (e.g. "2018.3.0", minor version is optional)
	"addon_minimumNVDAVersion": "2019.3.0",
	# Last NVDA version supported/tested (e.g. "2018.4.0", ideally more recent than minimum version)
	"addon_lastTestedNVDAVersion": "2021.1.0",
	# Add-on update channel (default is None, denoting stable releases,
	# and for development releases, use "dev".)
	# Do not change unless you know what you are doing!
	"addon_updateChannel": None,
}

import os.path

# Define the python files that are the sources of your add-on.
# You can either list every file (using ""/") as a path separator,
# or use glob expressions.
# For example to include all files with a ".py" extension from the "globalPlugins" dir of your add-on
# the list can be written as follows:
# pythonSources = ["addon/globalPlugins/*.py"]
# For more information on SCons Glob expressions please take a look at:
# https://scons.org/doc/production/HTML/scons-user/apd.html
pythonSources = [os.path.join("addon", "globalPlugins", "TiendaNVDA", "*.py")]

# Files that contain strings for translation. Usually your python sources
i18nSources = ["buildVars.py"] + pythonSources

# Files that will be ignored when building the nvda-addon file
# Paths are relative to the addon directory, not to the root directory of your addon sources.
excludedFiles = []

# Base language for the NVDA add-on
# If the source code, add-on interface and readme file located in the root folder are written in a language other than english, modify this variable as appropriate.
# For example, set baseLanguage to "es" if your add-on is primarily in spanish
baseLanguage = "es"
