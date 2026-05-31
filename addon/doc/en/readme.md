# TiendaNVDA)Add-on store for NVDA)

> **⚠️ Important notice for beta testers:**
> If you have tested the **TiendaNVDA_Modern** add-on, please **uninstall it before installing this version**. That version was a test and beta version that should not co-exist with this final version. To remove it, go to NVDA menu → Tools → Add-on Store, select "TiendaNVDA_Modern" and remove it. Restart NVDA and then proceed to install this new version.

Unified Add-on Store for NVDA: Integrates the **Spanish Community Store (NVDA.ES)** and the **Official NV Access Store** into a single, accessible interface.

**Author:** Hector J. Benitez Corredera  
**License:** GNU General Public License v2  
**Version:** 2026.05.10  
**Compatibility:** NVDA 2025.1 - NVDA 2026.1  
**Repository:** [https://github.com/hxebolax/Tienda-para-NVDA](https://github.com/hxebolax/Tienda-para-NVDA)

---

## Contents

1. [Introduction](#introduccion)
2. [Install](#instalacion)
3. [First steps](#primeros-pasos)
4. [Three shops](#las-tres-tiendas)
5. [Store interface](#la-interfaz-de-la-tienda)
6. [Status indicators](#indicadores-de-estado)
7. [Hotkeys and special functions](#teclas-rapidas-y-funciones-especiales)
8. [Context menu](#menu-contextual)
9. [Manage installed add-ons](#gestion-de-complementos-instalados)
10. [Add-on packer](#empaquetador-de-complementos)
11. [Search for updates](#buscar-actualizaciones)
12. [Options panel](#panel-de-opciones)
13. [Caching system](#sistema-de-cache)
14. [Offline mode](#modo-offline)
15. [Backup and restore](#backup-y-restauracion)
16. [Translation of descriptions](#traduccion-de-descripciones)
17. [Custom servers](#servidores-personalizados)
18. [Notes and protections](#observaciones-y-protecciones)
19. [Hotkey summary](#resumen-de-teclas-rapidas)
20. [Change log](#registro-de-cambios)

---

<a name="introduccion"></a>
## Introduction

**NVDA Add-on Store** is a complete evolution of the old NVDA.ES Store, redesigned from the ground up to provide a modern, fast, and unified experience.

### What's new compared to the previous version?

- **One-stop shop:** View add-ons from NVDA.ES and the official NV Access store in one window.
- **Status indicators:** Each add-on shows its status in real time: installed, update available, disabled, incompatible, etc.
- **Local Control:** Disable, enable or remove add-ons without leaving the store.
- **Multi-level caching system:** Server cache, translation cache and list cache for super-fast loading.
- **Offline Mode:** Browse the store without an internet connection using the saved cache data.
- **Backup and Restore:** Back up your add-ons and restore them when you change computers.- **Packager:** Create `.nvda-addon` files from any installed add-on.
- **Silent installation:** Install add-ons in the background without any intermediate dialogs.
- **Smart Reboot:** The store detects whether something was actually installed before offering a reboot.
- **Check Dependencies:** Checks if the add-on's dependencies are satisfied before installing.
- **Cached Translation:** Instantly translate descriptions using the F3 key, and the translations are saved so you don't have to repeat the request.
- **Improved notifications:** Update notifications now indicate the source (NVDA.ES or official) and the names of the add-ons.

---

<a name="instalacion"></a>
## Installation

1. Download the `.nvda-addon` file from the [repository releases](https://github.com/hxebolax/Tienda-para-NVDA/releases) page.
2. Open the downloaded file or drag it onto the NVDA window.
3. Confirm installation when NVDA prompts you to do so.
4. Restart NVDA to activate the add-on.

---

<a name="primeros-pasos"></a>
## First steps

The add-on comes **without assigned keyboard shortcuts**. You can assign your combinations to:

**NVDA Menu → Options → Input Gestures → NVDA Add-on Store**

Here you will find the following available actions:

- Show a window with all NVDA.ES add-ons
- Check for updates to installed add-ons in NVDA.ES
- Show a window with all the additions of the official store
- Check for updates to official add-ons
- Show one-stop shop with all add-on sources

### Access via menu

You can also access all functions through the NVDA menu:

**NVDA Menu → Tools → NVDA Add-on Store**

Here you will find the following submenus:

- **NVDA.ES Store:** List of add-ons and search for updates from the Spanish-speaking community.
- **Official NVDA Store:** List of add-ons and search for updates to the official store.
- **One Stop Shop (All Sources):** Shows all add-ons from all sources in one list.
- **Add-on packer:** Allows you to pack installed add-ons into `.nvda-addon` files.
- **Add-on Documentation:** Opens this documentation in your default browser.

---

<a name="las-tres-tiendas"></a>
## Three stores

The new version integrates three add-on viewing modes:

### NVDA.ES Store

This is a Hispanic community store. It gets additions from the [https://nvda.es](https://nvda.es) server and any custom servers you add.

### Official NVDA Store

Provides access to the official NV Access add-on store ([https://addons.nvda-project.org](https://addons.nvda-project.org)). Add-ons from this source are obtained directly through the official store API and are displayed with all compatibility information.

### One-stop shop

This is a combined view that shows **all add-ons from all sources** in one list.Add-ons are tagged with `[ES]` (Spanish Community) and `[OF]` (Official Store) so you know where each one comes from.

---

<a name="la-interfaz-de-la-tienda"></a>
## Store interface

When you open any of the stores, a window is displayed divided into two panels:

### Left panel (work area)

1. **Search Box:** When opening a store, the focus is here. Type any term and press Enter to filter the list. To show all add-ons again, clear the search field and press Enter with a blank field.

2. **Add-on List:** Shows all available add-ons with their status indicator in square brackets (eg: `[I]`, `[U]`). Navigation with Up/Down keys.

3. **Action Button (Install/Update):** This button is dynamic; its text automatically changes depending on the state of the selected add-on:
   - If the add-on is not installed, **"Install"** is displayed.
   - If an update is available, **"Update"** is displayed.

### Right panel (information tab)

As you move through the list of add-ons, this panel is filled with complete information about the selected add-on:

- Name and short description
- Version available on the server
- Installed version (if applicable)
- Author
- Full description
- NVDA compatible (minimum version and latest tested)
- Number of downloads (when available)
- Installation status

---

<a name="indicadores-de-estado"></a>
## Status indicators

As you navigate through the list of add-ons, NVDA announces letters in square brackets indicating the state of each add-on:

| Indicator | Meaning |
|:----------|:-----------|
| **[I]** | **Installed:** The add-on is installed and active. |
| **[U]** | **Update:** New version available. Update yourself! |
| **[U-I]** | **Incompatible Update:** A new version is available, but it is not compatible with your version of NVDA. |
| **[D]** | **Disabled:** The add-on is installed but manually deactivated. |
| **[R]** | **Pending removal:** Will be removed when NVDA is restarted. |
| **[I-I]** | **Incompatible Installed:** The add-on is installed but blocked due to incompatibility with your version of NVDA. |
| **[X]** | **Incompatible:** The add-on is not compatible with your version of NVDA. |

The **One Stop Shop** also displays the origin:

| Tag | Origin |
|:---------|:-----------|
| **[ES]** | NVDA.ES Servers (Spanish Community) |
| **[OF]** | Official NV Access store |

---

<a name="teclas-rapidas-y-funciones-especiales"></a>
## Hotkeys and special functions

These keys work when the focus is in the Add-ons list:

### F1 - Current position

Press **F1** to have NVDA tell you where you are on the list: "You are on expansion 15 of 200."

### Ctrl+F1 — Explain the indicator

Don't remember what the `[I]` or `[U]` brackets mean? Press **Ctrl+F1**,and NVDA will explain in clear language the status of the selected add-on.

### F2 - Read full card

Press **F2** to have NVDA read the entire tech sheet and add-on description in one go **without having to go to the right panel**. Works in all stores.

### F3 — Translate description

Is the description in English or another language? Press **F3** and the store will translate it into your configured language (default is Spanish). A sound signal will be played when the translation begins and ends.

> **Note:** To use F3, you must first activate the translator in the add-on options. Internet connection required.

---

<a name="menu-contextual"></a>
## Context menu

In the add-ons list, press **App Key** (or **Shift+F10**) to open a context menu with the following options:

### Filters

- **Show all add-ons:** Shows the full list (default option).
- **Show Addons by API Compatibility:** Filters only addons that are compatible with a specific version of NVDA.
- **Show additions sorted by author:** Sorts the list by author name.
- **Show downloads in descending order:** Sorts by popularity.

> **Note:** Filters do not add up. Each filter is applied individually, and the window title changes to indicate the active filter. Filter options are retained until NVDA is restarted.

### Copy to clipboard

- **Copy information:** Copies the entire card of the selected add-on.
- **Copy webpage link:** Copies the official URL of the add-on.
- **Copy download link:** Submenu with available development branches to copy their direct download link.

---

<a name="gestion-de-complementos-instalados"></a>
## Manage installed add-ons

One of the most powerful innovations: if the add-on is already installed, you can manage it **without leaving the store**.

1. Select the add-on marked as `[I]`, `[D]` or `[U]` in the list.
2. Press **Application Key** (or right mouse button).
3. In the **Manage Installations** submenu you will find:

- **Disable / Enable:** Temporarily activates or deactivates the add-on.
- **Delete:** Marks the add-on for removal (will take effect after restarting NVDA).
- **View Documentation:** Opens the add-on documentation in the browser. If the documentation is in your language, it will open in your language; otherwise, in the default extension language.

---

<a name="empaquetador-de-complementos"></a>
## Add-on packer

The packer allows you to create `.nvda-addon` files from add-ons you already have installed. It is ideal for:

- Transfer the add-on to another person without having to look for it in the store.
- Creating backup copies of specific add-ons.
- Saving a specific version of the add-on before updating it.

**To pack the add-on:**

1.Go to **NVDA Menu → Tools → NVDA Add-on Store → Add-on Packer**.
2. Select the add-on you want to pack from the list.
3. Select the directory where you want to save the file.
4. The `.nvda-addon` file will be automatically created in the format: `name_version_Gen.nvda-addon`.

---

<a name="buscar-actualizaciones"></a>
## Search for updates

The add-on offers two ways to search for updates:

### Manual search

In the Tools menu, select **Check for updates** in any of the stores (NVDA.ES or official). A window will appear with add-ons for which updates are available.

In this window you can:

- **Select add-ons individually:** Use spacebar to check/uncheck.
- **Alt+S:** Select all add-ons to update.
- **Alt+D:** Deselect all add-ons.
- **Alt+A:** Start updating the selected add-ons.
- **Alt+C / Escape / Alt+F4:** Close the window.

### Automatic check

When you activate automatic verification in options:

- The store will look for updates in the background at the specified interval.
- A system notification will be displayed indicating the number of updates and their source.
- The search automatically stops after 10 checks without results or 5 checks after detecting updates, so as not to overload the server.

Now notifications have become more informative:

```
3 updates found.
• 
NVDA.ES (2): Appendix A, Appendix B
• 
Official Store (1): Supplement C
Run a check for add-on updates.
```

---

<a name="panel-de-opciones"></a>
## Options panel

The add-on settings are accessed through:

**NVDA Menu → Options → Options → NVDA Add-on Store**

### A. NVDA.ES Store

- **Select add-on server:** Selects the default server from the configured ones.
- **Manage Add-on Servers:** Opens a manager where you can add, edit or delete custom servers.

### B. NVDA Official Store

- **Enable Official NVDA Store:** Activates or deactivates integration with the official NV Access Store.
- **Allow incompatible add-ons from the official store:** Allows you to try to install add-ons marked as incompatible. **Use at your own risk.**

### C. Updates

- **Activate automatic check for updates:** Enables background search.
- **Update check time:** Selects the interval between checks:
  - 15 minutes, 30 minutes, 45 minutes, 1 hour, 12 hours, 1 day, 1 week.
- **Enable updates from the official store:** Adds updates from the official store to the automatic check.

### D. Translation

- **Activate Translator for Descriptions:** Enables the use of the F3 key for translation.
- **Language for translation of descriptions:** Allows you to choose from 12 languages: German, Arabic, Croatian, Spanish, French, English, Italian, Polish, Portuguese, Russian, Turkish and Ukrainian.### E. General Options

- **Sort add-ons alphabetically:** Sorts the list from A to Z.
- **Install add-ons after downloading:** Automatically opens the installation wizard when the download is complete.
- **Silent installation:** Add-ons are installed in the background without intermediate dialogs. It only requests a reboot when finished.
- **Enable server cache:** Saves add-on lists to disk for faster loading.
- **Update cache every...:** Configures the cache update interval.
- **Use cache for translations:** Translations made using F3 are saved so as not to repeat the request to Google.
- **Enable offline mode:** Allows you to browse the store without an Internet connection, using cached data.

### F. Backup and Restore

- **Backup Addons:** Creates a JSON file listing all your installed addons.
- **Restore from Backup:** Loads the backup file and allows you to reinstall the listed add-ons.

### G. Installed add-ons present on the server

At the bottom of the options is a list of your add-ons that are also on the server. From here you can:

1. Select an add-on and press **Space**.
2. In the pop-up menu, select **update channel** (Stable, Beta, Development, etc.) or **Reject updates** so that the store stops notifying about this add-on.

> **Important:** Changes are only saved when you click OK or Apply in the options dialog.

---

<a name="sistema-de-cache"></a>
## Caching system

The store implements a multi-level caching system for maximum performance:

### Server cache

Saves add-on lists to disk. When opening a store, if the cache has not expired, it is loaded directly from disk instead of sending a request to the server.

- Configured via: **Enable server cache** in options.
- The update interval is configurable.

### Translation cache

Translations made using F3 are saved to a permanent JSON file. The next time you request the same translation, it will be loaded instantly from the cache.

- Configured via: **Use cache for translations** in options.

### In-memory cache

In addition to the disk cache, the store maintains an in-memory cache for the most frequent requests, completely eliminating disk access during the session.

---

<a name="modo-offline"></a>
## Offline mode

Offline mode allows you to browse the store **without an Internet connection**, using data previously saved in the cache.

To use it:

1. Make sure that the **Enable server cache** and **Enable offline mode** options are activated in the settings.
2. Browse the store at least once while connected to the Internet so that the cache is formed.
3. The next time you open a store without the Internet, the data will be loaded from the cache.

> **Note:** While offline you will not be able to download or install add-ons.but you will be able to view information about add-ons that you visited previously.

---

<a name="backup-y-restauracion"></a>
## Backup and restore

### Create a backup

1. Go to **Options → NVDA Add-ons Store → Back up add-ons**.
2. Select a name and location for the `.json` file.
3. A file will be created listing all of your installed add-ons, including name, version, and short description.

### Automatic backup on exit

The store automatically creates a backup copy when closing NVDA (configurable in options).

### Restoring from a backup

1. Go to **Options → NVDA Add-ons Store → Restore from Backup**.
2. Select the backup `.json` file.
3. The store will launch a wizard that will find the latest versions of each add-on on the servers and allow you to install them in batches.

> **Ideal for:** Transferring add-ons to a new computer or restoring your configuration after reinstalling NVDA.

---

<a name="traduccion-de-descripciones"></a>
## Translation of descriptions

The store includes a built-in translator based on Google Translate:

1. **Activate the translator** in the add-on options.
2. **Select your target language** (default is Spanish).
3. **Press F3** on any add-on in the list to translate its description.

Features:

- A beep at the beginning and end to indicate the transfer is complete.
- Translations are saved in a cache to avoid repeating requests.
- The translation is lost when changing the add-on; press F3 again if you need it.
- Internet connection required.

---

<a name="servidores-personalizados"></a>
## Custom servers

You can add third-party add-on repositories that use an NVDA.ES compatible format.

### Adding a server

1. Go to **Options → NVDA Add-on Store → Manage Add-on Servers**.
2. Click **Add**.
3. Enter a descriptive name and server URL.
4. Confirm and the server will appear in the server selection list.

### Example: Russian-speaking community server

- **Name:** Russian-speaking community
- **URL:** `https://nvda-addons.ru/get.php?addonslist`

### Quick server change

From the main window of the NVDA.ES store, press **Alt+C** or the **Change Server** button to open a menu with all configured servers. The change occurs instantly and temporarily (it is not saved as standard until you change it in the options).

> **Note:** The default server for the Spanish-speaking community cannot be changed or deleted.

---

<a name="observaciones-y-protecciones"></a>
## Notes and protections

The supplement includes many protections to ensure safe use:

1. **Additions pending removal:** Automatically excluded from update checks.
2. **Check API Compatibility:** Even if the version on the server is newer, if it is not compatible with your version of NVDA, the update will not be offered.
3.**Notification about installation errors:** If any add-on failed to update, its name is reported.
4. **Blocked after update:** The store does not allow you to search for further updates if the update has already been performed and NVDA has not been restarted.
5. **Notification after reboot:** If the automatic check detects that NVDA has not been restarted after the update, a reminder notification is issued.
6. **Offline Protection:** If libraries cannot be loaded due to a lack of connection, information is written to the NVDA log and a voice message is issued when attempting to access the store.
7. **Smart Reboot:** The store automatically detects whether the add-on has actually been installed. If you cancel the installation, it won't ask you to reboot unnecessarily.
8. **Checking Dependencies:** Checks if all required dependencies are satisfied before installation.

---

<a name="resumen-de-teclas-rapidas"></a>
## Shortcut Key Summary

### Main store window

| Action | Key |
|:-------|:------|
| Go to search field | `Alt+B` |
| Go to add-ons list | `Alt+L` |
| Install / Update | `Alt+I` |
| Go to add-on information | `Alt+I` (right panel) |
| Go to add-on web page | `Alt+P` |
| Change server (NVDA.ES only) | `Alt+C` |
| Close store | `Alt+S` / `Escape` / `Alt+F4` |

### In the list of add-ons

| Action | Key |
|:-------|:------|
| Find out the current position in the list | `F1` |
| Explain status indicator | `Ctrl+F1` |
| Read Full Addition Card | `F2` |
| Translate description | `F3` |
| Context menu (filters, copy, control) | `Application key` / `Shift+F10` |

### Update window

| Action | Key |
|:-------|:------|
| Select all add-ons | `Alt+S` |
| Deselect all | `Alt+D` |
| Start update | `Alt+A` |
| Close window | `Alt+C` / `Escape` / `Alt+F4` |

---

<a name="registro-de-cambios"></a>
## Changelog

### Version 2026.05.10

* Added Turkish language (Umut Korkmaz)

### Version 2026.05.09

* The first version of the unified Add-on Store for NVDA.
* Full integration of the NVDA.ES Store and the Official NV Access Store.
* New system of status indicators: [I], [U], [D], [R], [I-I], [U-I], [X].
* Local add-on management: disable, enable and delete without leaving the store.
* Multi-level caching system: server cache, translation cache and list cache.
* Offline mode: Browse the store without an Internet connection using cached data.
* Backup and restore installed add-ons.
* Add-on packer: create .nvda-addon files from installed add-ons.
* Smart dependency and API compatibility checking.
* Quiet installation with smart reboot.
* Translation of descriptions with saving in cache via Google Translate.
* Support for custom add-on servers.* Interface with hot keys F1, Ctrl+F1, F2, F3 for quick access to functions.
* Detailed notifications indicating the source of updates (ES / Official).

### Previous versions (Store for NVDA.ES)

Previously, this repository contained the classic version of **Store for NVDA.ES** (versions 0.1 - 0.10). Starting with version 2026.05.09, the repository has been replaced by the new **Unified Add-on Store for NVDA**, which is a complete rework of the add-on.

If you want to view the source code or documentation of an older version, you can do so by navigating the repository's commit history on GitHub:

1. Go to [https://github.com/hxebolax/Tienda-para-NVDA](https://github.com/hxebolax/Tienda-para-NVDA).
2. Click on the **commits** link (or the commit counter at the top of the repository).
3. Find any commit prior to **May 9, 2026** to access the code and classic store releases.
4. While on the desired commit, you can click **"Browse files"** to see the full state of the repository at that time.

Alternatively, older releases with their `.nvda-addon` files will still be available in the [Releases](https://github.com/hxebolax/Tienda-para-NVDA/releases) section of the repository unless they are manually removed.

---

Enjoy the NVDA Add-ons Store!

**With respect:** Hector J. Benitez Corredera.