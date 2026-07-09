# NVDA Add-ons Store (Add-on store for NVDA)

> **⚠️ Important notice for beta testers:**
> If you have been testing the **NVDA Modern Store** plugin, please **uninstall it before installing this version**. That version was a testing and beta version that should not coexist with this final version. To uninstall it, go to NVDA menu → Tools → Add-on Store, select “NVDA Modern Store” and delete it. Restart NVDA and then proceed to install this new version.

Unified Add-on Store for NVDA: integrates the **Spanish-speaking Community Store (NVDA.ES)** and the **Official NV Access Store** in a single accessible interface.

**Author:** Héctor J. Benítez Corredera  
**License:** GNU General Public License v2  
**Version:** 2026.05.09  
**Compatibility:** NVDA 2025.1 to NVDA 2026.1  
**Repository:** [https://github.com/hxebolax/Tienda-para-NVDA](https://github.com/hxebolax/Tienda-para-NVDA)

---

## Table of content

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [First steps](#first-steps)
4. [The three stores](#the-three-stores)
5. [The store interface](#the-store-interface)
6. [Status Indicators](#status-indicators)
7. [Hotkeys and special functions](#hotkeys-and-special-functions)
8. [Contextual menu](#contextual-menu)
9. [Management of installed plugins](#management-of-installed-plugins)
10. [Plugin Packager](#plugin-packer)
11. [Check for updates](#check-for-updates)
12. [Options Panel](#options-panel)
13. [Cache system](#cache-system)
14. [Offline-mode](#offline-mode)
15. [Backup and restoration](#backup-and-restoration)
16. [Translation of descriptions](#translation-of-descriptions)
17. [Custom servers](#custom-servers)
18. [Observations and protections](#observations-and-protections)
19. [Hotkey Summary](#hotkey-summary)
20. [Collaborators](#collaborators)
21. [Changelog](#changelog)

---

<a name="introduction"></a>
## Introduction

The **NVDA Add-ons Store** is a complete evolution of the old NVDA.ES Store, redesigned from the ground up to offer a modern, fast and unified experience.

### What's new compared to the previous version?

- **Unified Store:** Browse NVDA.ES add-ons and the official NV Access store from a single window.
- **Status Indicators:** Each plugin shows its status in real time: installed, updatable, disabled, incompatible, etc.
- **Local Management:** Disable, enable or uninstall plugins without leaving the store.
- **Multi-level caching system:** Server cache, translation cache and list cache for ultra-fast loading.
- **Offline mode:** Browse the store without an internet connection using cached data.
- **Backup and restoration:** Create backups of your plugins and restore them when changing devices.
- **Packager:** Generate `.nvda-addon` files from any installed plugin.
- **Silent installation:** Installs plugins in the background without intermediate dialogs.
- **Smart reboot:** The store detects if something was actually installed before asking to reboot.
- **Dependency Check:** Verify that the plugin dependencies are satisfied before installing.
- **Translation with cache:** Translate descriptions instantly with the F3 key, and the translations are saved so as not to repeat the query.
- **Improved Notifications:** Update notifications now indicate the origin (NVDA.ES or Official) and the names of the add-ons.

---

<a name="installation"></a>
## Installation

1. Download the `.nvda-addon` file from the [repository releases] page(https://github.com/hxebolax/Tienda-para-NVDA/releases).
2. Open the downloaded file or drag it onto the NVDA window.
3. Accept the installation when prompted by NVDA.
4. Restart NVDA to activate the plugin.

---

## Getting started

The plugin comes **without assigned keyboard shortcuts**. You can assign custom shortcuts from:

**NVDA Menu → Preferences → Input Gestures → NVDA Add-on Store**

Here you will find the following actions available:

- Show the window with all NVDA.ES plugins
- Check for updates to installed plugins on NVDA.ES
- Show the window with all the plugins from the official store
- Check for updates to official plugins
- Show unified store with all plugin sources

### Access from the menu

You can also access all functions from the NVDA menu:

**NVDA Menu → Tools → NVDA Addons Store**

Here you will find the following submenus:

- **NVDA.ES Store:** List of add-ons and search for updates from the Spanish-speaking community.
- **NVDA Official Store:** List of add-ons and search for updates from the official store.
- **Unified Store (All Sources):** Displays all plugins from all sources in a single list.
- **Add-on packager:** Allows you to package installed add-ons as `.nvda-addon` files.
- **Plugin Documentation:** Open this documentation in your default browser.

---

<a name="the-three-stores"></a>
## The three stores

The new version integrates three plugin display modes:

### NVDA.ES Store

It is the store for the Spanish-speaking community. Gets the plugins from the [https://nvda.es](https://nvda.es) server and any custom servers you added.

### NVDA Official Store

Access the official NV Access add-on store ([https://addons.nvda-project.org](https://addons.nvda-project.org)).Plugins from this source are pulled directly from the official store API and are displayed with all their compatibility information.

### Unified Store

It is the combined view that shows **all plugins from all sources** in a single list. The plugins are identified with the tags `[ES]` (Spanish-speaking community) and `[OF]` (official store) so you know where each one comes from.

---

<a name="the-store-interface"></a>
## The store interface

When you open any of the stores, a window divided into two panels is displayed:

### Left panel (work area)

1. **Search box:** When you open the store, the focus is placed here. Type any term and press Enter to filter the list. To show all plugins again, clear the search field and press Enter with the field empty.

2. **Plugin List:** Displays all available plugins with their status indicator in square brackets (ex: `[I]`, `[U]`). Navigate with the Up/Down arrows.

3. **Action Button (Install/Update):** This button is dynamic; changes your text automatically based on the state of the selected plugin:
   - If you don't have the plugin installed, show **"Install"**.
   - If an update is available, displays **"Update"**.

### Right panel (information sheet)

As you move through the list of plugins, this panel populates with the complete information for the selected plugin:

- Name and summary
- Version available on the server
- Installed version (if applicable)
- Author
- Full description
- NVDA support (minimum and latest version tested)
- Number of downloads (when available)
- Installation status

---

<a name="status-indicators"></a>
## Status indicators

As you move through the list of add-ons, NVDA announces letters in square brackets that indicate the status of each add-on:

| Indicator | Meaning |
|:----------|:------------|
| **[I]** | **Installed:** The plugin is installed and active. |
| **[U]** | **Update:** A new version is available. Update! |
| **[U-I]** | **Incompatible update:** There is a new version but it is not compatible with your version of NVDA. |
| **[D]** | **Disabled:** The plugin is installed but disabled manually. |
| **[R]** | **Pending removal:** Will be removed upon restart of NVDA. |
| **[I-I]** | **Incompatible installed:** The plugin is installed but blocked due to incompatibility with your version of NVDA. |
| **[X]** | **Not supported:** The plugin is not compatible with your version of NVDA. |

In the **Unified Store** the origin is also shown:

| Tag | Origin |
|:---------|:------------|
| **[EN]** | NVDA servers.ES (Spanish-speaking community) |
| **[OF]** | NV Access Official Store |

---

<a name="hotkeys-and-special-functions"></a>
## Hotkeys and special functions

These keys work when focus is on the plugin list:

### F1 — Current position

Press **F1** to have NVDA tell you where you are in the list: "You are at complement 15 of 200."

### Ctrl+F1 — Explain indicator

Don't remember what the square brackets `[I]` or `[U]` mean? Press **Ctrl+F1** and NVDA will explain in clear language the status of the selected add-on.

### F2 — Read complete file

Press **F2** so that NVDA reads the entire data sheet and description of the add-on in one go **without having to tab to the right panel**. It works in all stores.

### F3 — Translate description

Is the description in English or another language? Press **F3** and the store will translate it to the language you have configured (by default, Spanish). A sound will be played when the translation starts and ends.

> **Note:** To use F3, you must previously activate the translator in the plugin options. Requires internet connection.

---

<a name="contextual-menu"></a>
## Context menu

In the list of add-ons, press the **Applications Key** (or **Shift+F10**) to display the context menu with the following options:

### Filters

- **Show all plugins:** Shows the entire list (default).
- **Show Plugins by API Compatibility:** Filters only plugins compatible with a specific version of NVDA.
- **Show plugins sorted by author:** Sort the list by author name.
- **Show by downloads from highest to lowest:** Sort by popularity.

> **Note:** Filters are not cumulative. Each filter runs individually and the window title changes to inform you of the active filter. Filter options are maintained as long as NVDA is not restarted.

### Copy to clipboard

- **Copy information:** Copy the complete file of the selected plugin.
- **Copy link to web page:** Copy the official URL of the plugin.
- **Copy download link:** Submenu with the development branches available to copy their direct download URL.

---

<a name="management-of-installed-plugins"></a>
##Management of installed plugins

One of the most powerful new features: if a plugin is already installed, you can manage it **without leaving the store**.

1. Select a plugin marked `[I]`, `[D]` or `[U]` in the list.
2. Press the **Applications Key** (or right click).
3. In the **Installed Management** submenu you will find:

- **Disable / Enable:** Activate or deactivate the plugin temporarily.
- **Uninstall:** Mark the plugin for removal (will take effect upon restarting NVDA).
- **See documentation:** Open the plugin documentation in the browser.If there is documentation in your language, it will open in your language; otherwise, in the plugin's default language.

---

<a name="plugin-packager"></a>
## Plugin Packager

The packager allows you to generate `.nvda-addon` files from add-ons you already have installed. It is ideal for:

- Share a plugin with another person without having to search for it in the store.
- Create backups of specific plugins.
- Keep a particular version of a plugin before updating it.

**To package a plugin:**

1. Go to **NVDA Menu → Tools → NVDA Addon Store → Addon Packager**.
2. Select the plugin you want to package from the list.
3. Choose the directory where you want to save the file.
4. The `.nvda-addon` file will be automatically generated in the format: `version name Gen.nvda-addon`.

---

<a name="check-for-updates"></a>
## Check for updates

The plugin offers two ways to check for updates:

### Manual search

From the tools menu, select **Check for updates** in any of the stores (NVDA.ES or Official). A window will be displayed with the plugins that have updates available.

In this window you can:

- **Select plugins individually:** Use the space bar to check/uncheck.
- **Alt+S:** Select all plugins to update.
- **Alt+D:** Deselect all plugins.
- **Alt+A:** Start updating the selected plugins.
- **Alt+C / Escape / Alt+F4:** Close the window.

### Automatic check

When you activate automatic checking in the options:

- The store will check for updates in the background based on the configured interval.
- It will show a system notification indicating how many updates there are and what source they come from.
- The search stops automatically after 10 checks without results, or 5 checks after finding updates, so as not to overwhelm the server.

Notifications are now more informative:

```
3 updates found.
- NVDA.ES (2): Complement A, Complement B
- Official Store (1): Complement C

Run Check for plugin updates.
```

---

<a name="options-panel"></a>
## Options panel

Access the plugin settings from:

**NVDA Menu → Preferences → Options → NVDA Add-on Store**

### A. NVDA.ES Store

- **Select a plugin server:** Choose the default server from those you have configured.
- **Manage Plugin Servers:** Opens the manager where you can add, edit or delete custom servers.

### B. NVDA Official Store

- **Enable NVDA official store:** Enable or disable the integration with the official NV Access store.- **Allow incompatible plugins from the official store:** Allows you to try to install plugins marked as incompatible. **Use at your own risk.**

### C. Updates

- **Activar comprobación automática de actualizaciones:** Activa la búsqueda en segundo plano.
- **Time to check for updates:** Choose the interval between checks:
  - 15 minutes, 30 minutes, 45 minutes, 1 hour, 12 hours, 1 day, 1 week.
- **Include official store updates:** Adds official store updates to the automatic check.

### D. Translation

- **Enable translator for descriptions:** Enables the use of the F3 key to translate.
- **Language to translate descriptions:** Choose from 12 languages: German, Arabic, Croatian, Spanish, French, English, Italian, Polish, Portuguese, Russian, Turkish and Ukrainian.

### E. General Options

- **Ordenar complementos alfabéticamente:** Ordena la lista de la A a la Z.
- **Install plugins after downloading:** Opens the installation wizard automatically when the download is complete.
- **Install silently:** Plugins are installed in the background without intermediate dialogs. It only asks to restart when finished.
- **Enable Server Cache:** Stores plugin lists on disk for faster loading.
- **Refresh cache every...:** Configures the cache refresh interval.
- **Use cache for translations:** Translations made with F3 are saved so as not to repeat the query to Google.
- **Enable offline mode:** Allows you to browse the store without an internet connection, using cached data.

### F. Backup and restore

- **Create Plugin Backup:** Generate a JSON file with the list of all your installed plugins.
- **Restore from Backup:** Loads a backup file and allows you to reinstall the listed plugins.

### G. Complementos instalados que hay en el servidor

At the bottom of the options is a list of your plugins that are also on the server. From here you can:

1. Select a plugin and press **Space bar**.
2. In the pop-up menu, choose the **update channel** (Stable, Beta, Development, etc.) or **Discard updates** so that the store stops notifying about that plugin.

> **Important:** Changes are only saved when you click OK or Apply in the options dialog.

---

<a name="cache-system"></a>
## Cache system

The store implements a multi-level caching system to maximize performance:

### Server Cache

Stores plugin lists to disk. When you open the store, if the cache has not expired, it is loaded directly from disk instead of making a request to the server.

- It is configured from: **Enable server cache** in the options.
- The update interval is configurable.### Translation cache

Translations performed with F3 are saved in a persistent JSON file. The next time you request the same translation, it will be loaded instantly from the cache.

- It is configured from: **Use cache for translations** in the options.

### In-memory cache

In addition to the disk cache, the store maintains a RAM cache for the most frequent queries, completely eliminating disk access during the session.

---

<a name="offline-mode"></a>
## Offline mode

Offline mode allows you to browse the store **without an internet connection**, using the data previously stored in the cache.

To use it:

1. Make sure you have **Enable Server Cache** and **Enable Offline Mode** enabled in the options.
2. Browse the store at least once online for the cache to be generated.
3. The next time you open the store without internet, the data will be loaded from the cache.

> **Note:** In offline mode you will not be able to download or install add-ons, but you will be able to consult the information of the add-ons you previously visited.

---

<a name="backup-and-restoration"></a>
## Backup and restore

### Create backup

1. Go to **Options → NVDA Add-on Store → Create Add-on Backup**.
2. Choose a name and location for the `.json` file.
3. A file will be generated with the list of all your installed plugins, including name, version and summary.

### Automatic backup upon exit

The store automatically creates a backup when closing NVDA (configurable in the options).

### Restore from backup

1. Go to **Options → NVDA Add-on Store → Restore from Backup**.
2. Select the backup `.json` file.
3. The store will display a wizard that will search the servers for the latest versions of each plugin and allow you to install them in batches.

> **Ideal for:** Migrating plugins to a new computer or recovering your settings after reinstalling NVDA.

---

<a name="translation-of-descriptions"></a>
## Translation of descriptions

The store includes an integrated translator based on Google Translate:

1. **Activate the translator** from the plugin options.
2. **Select the destination language** (Spanish by default).
3. **Press F3** on any plugin in the list to translate its description.

Features:

- Start and end sound to indicate that the translation is being carried out.
- Translations are cached to avoid repeating queries.
- The translation is lost when changing plugins; Press F3 again if you need it again.
- Requires internet connection.

---

<a name="custom-servers"></a>
## Custom servers

You can add third-party plugin repositories that use the NVDA.ES compatible format.

### Add a server

1.Go to **Options → NVDA Add-on Store → Manage Add-on Servers**.
2. Press **Add**.
3. Enter a friendly name and the server URL.
4. Accept and the server will appear in the server selector.

### Example: Russian Community Server

- **Name:** Russian Community
- **URL:** `https://nvda-addons.ru/get.php?addonslist`

### Switch servers quickly

From the main window of the NVDA.ES store, press **Alt+C** or the **Change server** button to display a menu with all the configured servers. The change is immediate and temporary (it is not saved as default until you change it in the options).

> **Note:** The default Spanish-speaking community server cannot be modified or deleted.

---

<a name="observations-and-protections"></a>
## Observations and protections

The plugin includes multiple protections to ensure a safe experience:

1. **Add-ons pending uninstall:** They are automatically excluded from update checks.
2. **API Compatibility Validation:** Even if the server version is newer, if it is not compatible with your version of NVDA the update will not be offered.
3. **Installation error notification:** If any plugin could not be updated, it is reported with its name.
4. **Clock after update:** The store does not allow you to check for more updates if an update has already been performed and NVDA has not been restarted.
5. **Post-reboot notification:** If the self-check detects that NVDA has not been rebooted after updating, it issues a reminder notification.
6. **Protection without internet:** If the libraries cannot be loaded due to lack of connection, it is reported in the NVDA registry and is notified with a spoken message when trying to access the store.
7. **Smart Restart:** The store automatically detects whether a plugin has actually been installed. If you cancel the installer, it will not ask you to reboot unnecessarily.
8. **Dependency Check:** Before installing, verify that all required dependencies are satisfied.

---

<a name="hotkey-summary"></a>
## Hotkey summary

### Main store window

| Action | Key |
|:------|:------|
| Go to search box | `Alt+B` |
| Go to plugin list | `Alt+L` |
| Install / Update | `Alt+I` |
| Go to plugin information | `Alt+I` (right panel) |
| Go to the plugin web page | `Alt+P` |
| Change server (NVDA.ES only) | `Alt+C` |
| Close the store | `Alt+S` / `Escape` / `Alt+F4` |

### In the list of plugins

| Action | Key |
|:------|:------|
| Know current position in the list | `F1` |
| Explain status indicator | `Ctrl+F1` |
| Read complete complement sheet | `F2` |
| Translate description | `F3` |
| Context menu (filters, copy,management) | `Applications Key` / `Shift+F10` |

### Updates window

| Action | Key |
|:------|:------|
| Select all plugins | `Alt+S` |
| Deselect all | `Alt+D` |
| Start update | `Alt+A` |
| Close window | `Alt+C` / `Escape` / `Alt+F4` |

---
<a name="collaborators"></a>
## Collaborators

* Turkish language (Umut Korkmaz)
* Russian language (Valentín N. Kupriyanov)
* Polish language (Kazimierz Parzych)
*English language (Hoang-Long2012)
* Ukrainian language (George-br)

<a name="change-log"></a>
## Changelog

### Version 2026.05.20

*Fixed plugin's silent language updater (in beta)

Javi Dominguez improvements added (PR #1 and #2)

### Version 2026.05.13

*Fixed plugin's silent language updater (in beta)

### Version 2026.05.11

*Added silent plugin language updater (in beta)
* Added Russian language (Valentín N. Kupriyanov)

### Version 2026.05.10

* Added Turkish language (Umut Korkmaz)

### Version 2026.05.09

* First version of the Unified Add-on Store for NVDA.
* Complete integration of the NVDA.ES Store and the Official NV Access Store.
* New system of status indicators: [I], [U], [D], [R], [I-I], [U-I], [X].
* Local plugin management: disable, enable and uninstall without leaving the store.
* Multi-level cache system: server cache, translation cache and list cache.
* Offline mode: browsing the store without an internet connection using cached data.
* Backup and restoration of installed plugins.
* Addon Packager - Generate .nvda-addon files from installed plugins.
* Smart dependency checking and API compatibility.
* Silent installation with smart reboot.
* Translation of descriptions with persistent cache via Google Translate.
* Support for custom plugin servers.
* Interface with hotkeys F1, Ctrl+F1, F2, F3 for quick access to functions.
* Detailed notifications indicating origin of updates (ES / Official).

### Previous versions (Store for NVDA.ES)

This repository previously contained the classic version of the **Store for NVDA.ES** (versions 0.1 to 0.10). As of version 2026.05.09, the repository has been replaced by the new **Unified Plugin Store for NVDA**, which is a complete rewrite of the plugin.

If you want to consult the source code or documentation of the old version, you can do so by browsing the repository's commit history on GitHub:

1. Go to [https://github.com/hxebolax/Tienda-para-NVDA](https://github.com/hxebolax/Tienda-para-NVDA).
2. Click the **commits** link (or click on the commit counter at the top of the repository).
3.Search for any commits older than **May 9, 2026** to access classic store code and releases.
4. Once in the desired commit, you can press **"Browse files"** to see the complete status of the repository at that moment.

Alternatively, older releases with their `.nvda-addon` files will still be available in the [Releases](https://github.com/hxebolax/Tienda-para-NVDA/releases) section of the repository, as long as they are not manually removed.

---

Enjoy the NVDA Add-ons Store!

**With love:** Héctor J. Benítez Corredera.