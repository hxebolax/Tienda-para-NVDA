# Tienda de Complementos para NVDA

> **⚠️ Aviso importante para testers de la versión beta:**
> Si has estado probando el complemento **TiendaNVDA_Modern**, por favor **desinstálalo antes de instalar esta versión**. Aquella versión era una versión de pruebas y beta que no debe coexistir con esta versión final. Para desinstalarlo, ve al menú de NVDA → Herramientas → Tienda de complementos, selecciona "TiendaNVDA_Modern" y elimínalo. Reinicia NVDA y después procede a instalar esta nueva versión.

Tienda Unificada de Complementos para NVDA: integra la **Tienda de la Comunidad Hispanohablante (NVDA.ES)** y la **Tienda Oficial de NV Access** en una única interfaz accesible.

**Autor:** Héctor J. Benítez Corredera  
**Licencia:** GNU General Public License v2  
**Versión:** 2026.05.09  
**Compatibilidad:** NVDA 2025.1 a NVDA 2026.1  
**Repositorio:** [https://github.com/hxebolax/Tienda-para-NVDA](https://github.com/hxebolax/Tienda-para-NVDA)

---

## Índice

1. [Introducción](#introduccion)
2. [Instalación](#instalacion)
3. [Primeros pasos](#primeros-pasos)
4. [Las tres tiendas](#las-tres-tiendas)
5. [La interfaz de la tienda](#la-interfaz-de-la-tienda)
6. [Indicadores de estado](#indicadores-de-estado)
7. [Teclas rápidas y funciones especiales](#teclas-rapidas-y-funciones-especiales)
8. [Menú contextual](#menu-contextual)
9. [Gestión de complementos instalados](#gestion-de-complementos-instalados)
10. [Empaquetador de complementos](#empaquetador-de-complementos)
11. [Buscar actualizaciones](#buscar-actualizaciones)
12. [Panel de opciones](#panel-de-opciones)
13. [Sistema de caché](#sistema-de-cache)
14. [Modo offline](#modo-offline)
15. [Backup y restauración](#backup-y-restauracion)
16. [Traducción de descripciones](#traduccion-de-descripciones)
17. [Servidores personalizados](#servidores-personalizados)
18. [Observaciones y protecciones](#observaciones-y-protecciones)
19. [Resumen de teclas rápidas](#resumen-de-teclas-rapidas)
20. [Colaboradores](#colaboradores)
21. [Registro de cambios](#registro-de-cambios)

---

<a name="introduccion"></a>
## Introducción

La **Tienda de Complementos para NVDA** es una evolución completa de la antigua Tienda para NVDA.ES, rediseñada desde cero para ofrecer una experiencia moderna, rápida y unificada.

### ¿Qué hay de nuevo respecto a la versión anterior?

- **Tienda Unificada:** Navega por los complementos de NVDA.ES y la tienda oficial de NV Access desde una sola ventana.
- **Indicadores de estado:** Cada complemento muestra su estado en tiempo real: instalado, actualizable, deshabilitado, incompatible, etc.
- **Gestión local:** Deshabilita, habilita o desinstala complementos sin salir de la tienda.
- **Sistema de caché multinivel:** Caché de servidores, caché de traducciones y caché de listas para una carga ultrarrápida.
- **Modo offline:** Navega por la tienda sin conexión a internet usando datos almacenados en caché.
- **Backup y restauración:** Crea copias de seguridad de tus complementos y restáuralos al cambiar de equipo.
- **Empaquetador:** Genera archivos `.nvda-addon` desde cualquier complemento instalado.
- **Instalación silenciosa:** Instala complementos en segundo plano sin diálogos intermedios.
- **Reinicio inteligente:** La tienda detecta si realmente se instaló algo antes de pedir reiniciar.
- **Comprobación de dependencias:** Verifica que las dependencias del complemento estén satisfechas antes de instalar.
- **Traducción con caché:** Traduce descripciones al instante con la tecla F3, y las traducciones se guardan para no repetir la consulta.
- **Notificaciones mejoradas:** Las notificaciones de actualización ahora indican el origen (NVDA.ES u Oficial) y los nombres de los complementos.

---

<a name="instalacion"></a>
## Instalación

1. Descarga el archivo `.nvda-addon` desde la página de [releases del repositorio](https://github.com/hxebolax/Tienda-para-NVDA/releases).
2. Abre el archivo descargado o arrástralo sobre la ventana de NVDA.
3. Acepta la instalación cuando NVDA te lo solicite.
4. Reinicia NVDA para activar el complemento.

---

## Primeros pasos

El complemento viene **sin atajos de teclado asignados**. Puedes asignar atajos personalizados desde:

**Menú de NVDA → Preferencias → Gestos de entrada → Tienda de Complementos NVDA**

Aquí encontrarás las siguientes acciones disponibles:

- Mostrar la ventana con todos los complementos de NVDA.ES
- Buscar actualizaciones de los complementos instalados en NVDA.ES
- Mostrar la ventana con todos los complementos de la tienda oficial
- Buscar actualizaciones de los complementos oficiales
- Mostrar la tienda unificada con todas las fuentes de complementos

### Acceso desde el menú

También puedes acceder a todas las funciones desde el menú de NVDA:

**Menú NVDA → Herramientas → Tienda de Complementos NVDA**

Aquí encontrarás los siguientes submenús:

- **Tienda NVDA.ES:** Listado de complementos y búsqueda de actualizaciones de la comunidad hispanohablante.
- **Tienda Oficial NVDA:** Listado de complementos y búsqueda de actualizaciones de la tienda oficial.
- **Tienda Unificada (Todas las fuentes):** Muestra todos los complementos de todas las fuentes en una sola lista.
- **Empaquetador de complementos:** Permite empaquetar complementos instalados como archivos `.nvda-addon`.
- **Documentación del complemento:** Abre esta documentación en el navegador predeterminado.

---

<a name="las-tres-tiendas"></a>
## Las tres tiendas

La nueva versión integra tres modos de visualización de complementos:

### Tienda NVDA.ES

Es la tienda de la comunidad hispanohablante. Obtiene los complementos del servidor de [https://nvda.es](https://nvda.es) y de cualquier servidor personalizado que hayas añadido.

### Tienda Oficial NVDA

Accede a la tienda oficial de complementos de NV Access ([https://addons.nvda-project.org](https://addons.nvda-project.org)). Los complementos de esta fuente se obtienen directamente del API de la tienda oficial y se muestran con toda su información de compatibilidad.

### Tienda Unificada

Es la vista combinada que muestra **todos los complementos de todas las fuentes** en una sola lista. Los complementos se identifican con las etiquetas `[ES]` (comunidad hispanohablante) y `[OF]` (tienda oficial) para que sepas de dónde proviene cada uno.

---

<a name="la-interfaz-de-la-tienda"></a>
## La interfaz de la tienda

Al abrir cualquiera de las tiendas se muestra una ventana dividida en dos paneles:

### Panel izquierdo (zona de trabajo)

1. **Cuadro de búsqueda:** Al abrir la tienda, el foco se sitúa aquí. Escribe cualquier término y pulsa Enter para filtrar la lista. Para volver a mostrar todos los complementos, borra el campo de búsqueda y pulsa Enter con el campo vacío.

2. **Lista de complementos:** Muestra todos los complementos disponibles con su indicador de estado entre corchetes (ej: `[I]`, `[U]`). Navega con las flechas Arriba/Abajo.

3. **Botón de acción (Instalar/Actualizar):** Este botón es dinámico; cambia su texto automáticamente según el estado del complemento seleccionado:
   - Si no tienes el complemento instalado, muestra **"Instalar"**.
   - Si hay una actualización disponible, muestra **"Actualizar"**.

### Panel derecho (ficha informativa)

A medida que te mueves por la lista de complementos, este panel se rellena con la información completa del complemento seleccionado:

- Nombre y resumen
- Versión disponible en el servidor
- Versión instalada (si aplica)
- Autor
- Descripción completa
- Compatibilidad con NVDA (versión mínima y última probada)
- Número de descargas (cuando esté disponible)
- Estado de instalación

---

<a name="indicadores-de-estado"></a>
## Indicadores de estado

Al moverte por la lista de complementos, NVDA anuncia unas letras entre corchetes que indican el estado de cada complemento:

| Indicador | Significado |
|:----------|:------------|
| **[I]** | **Instalado:** El complemento está instalado y activo. |
| **[U]** | **Actualización:** Hay una versión nueva disponible. ¡Actualiza! |
| **[U-I]** | **Actualización incompatible:** Hay una versión nueva pero no es compatible con tu versión de NVDA. |
| **[D]** | **Deshabilitado:** El complemento está instalado pero desactivado manualmente. |
| **[R]** | **Pendiente de eliminar:** Se eliminará al reiniciar NVDA. |
| **[I-I]** | **Instalado incompatible:** El complemento está instalado pero bloqueado por incompatibilidad con tu versión de NVDA. |
| **[X]** | **No compatible:** El complemento no es compatible con tu versión de NVDA. |

En la **Tienda Unificada** también se muestra la procedencia:

| Etiqueta | Procedencia |
|:---------|:------------|
| **[ES]** | Servidores de NVDA.ES (comunidad hispanohablante) |
| **[OF]** | Tienda oficial de NV Access |

---

<a name="teclas-rapidas-y-funciones-especiales"></a>
## Teclas rápidas y funciones especiales

Estas teclas funcionan cuando el foco está en la lista de complementos:

### F1 — Posición actual

Pulsa **F1** para que NVDA te diga en qué posición de la lista te encuentras: "Estás en el complemento 15 de 200".

### Ctrl+F1 — Explicar indicador

¿No recuerdas qué significan los corchetes `[I]` o `[U]`? Pulsa **Ctrl+F1** y NVDA te explicará en lenguaje claro el estado del complemento seleccionado.

### F2 — Leer ficha completa

Pulsa **F2** para que NVDA lea de un tirón toda la ficha técnica y la descripción del complemento **sin necesidad de tabular al panel derecho**. Funciona en todas las tiendas.

### F3 — Traducir descripción

¿La descripción está en inglés u otro idioma? Pulsa **F3** y la tienda la traducirá al idioma que tengas configurado (por defecto, español). Se reproducirá un sonido al iniciar y al terminar la traducción.

> **Nota:** Para usar F3, debes activar previamente el traductor en las opciones del complemento. Requiere conexión a internet.

---

<a name="menu-contextual"></a>
## Menú contextual

En la lista de complementos, pulsa la **Tecla Aplicaciones** (o **Shift+F10**) para desplegar el menú contextual con las siguientes opciones:

### Filtros

- **Mostrar todos los complementos:** Muestra la lista completa (opción predeterminada).
- **Mostrar complementos por compatibilidad de API:** Filtra solo los complementos compatibles con una versión específica de NVDA.
- **Mostrar complementos ordenados por autor:** Ordena la lista por nombre de autor.
- **Mostrar por descargas de mayor a menor:** Ordena por popularidad.

> **Nota:** Los filtros no son acumulables. Cada filtro se ejecuta individualmente y el título de la ventana cambia para informar del filtro activo. Las opciones de filtro se mantienen mientras NVDA no se reinicie.

### Copiar al portapapeles

- **Copiar información:** Copia la ficha completa del complemento seleccionado.
- **Copiar enlace a la página web:** Copia la URL oficial del complemento.
- **Copiar enlace de descarga:** Submenú con las ramas de desarrollo disponibles para copiar su URL de descarga directa.

---

<a name="gestion-de-complementos-instalados"></a>
## Gestión de complementos instalados

Una de las novedades más potentes: si un complemento ya está instalado, puedes gestionarlo **sin salir de la tienda**.

1. Selecciona un complemento marcado como `[I]`, `[D]` o `[U]` en la lista.
2. Pulsa la **Tecla Aplicaciones** (o clic derecho).
3. En el submenú **Gestión instalado** encontrarás:

- **Deshabilitar / Habilitar:** Activa o desactiva el complemento temporalmente.
- **Desinstalar:** Marca el complemento para eliminación (se hará efectiva al reiniciar NVDA).
- **Ver documentación:** Abre la documentación del complemento en el navegador. Si hay documentación en tu idioma, se abrirá en tu idioma; de lo contrario, en el idioma por defecto del complemento.

---

<a name="empaquetador-de-complementos"></a>
## Empaquetador de complementos

El empaquetador permite generar archivos `.nvda-addon` a partir de complementos que ya tienes instalados. Es ideal para:

- Compartir un complemento con otra persona sin necesidad de buscarlo en la tienda.
- Crear copias de seguridad de complementos específicos.
- Conservar una versión particular de un complemento antes de actualizarlo.

**Para empaquetar un complemento:**

1. Ve a **Menú NVDA → Herramientas → Tienda de Complementos NVDA → Empaquetador de complementos**.
2. Selecciona el complemento que deseas empaquetar de la lista.
3. Elige el directorio donde quieres guardar el archivo.
4. El archivo `.nvda-addon` se generará automáticamente con el formato: `nombre_versión_Gen.nvda-addon`.

---

<a name="buscar-actualizaciones"></a>
## Buscar actualizaciones

El complemento ofrece dos formas de buscar actualizaciones:

### Búsqueda manual

Desde el menú de herramientas, selecciona **Buscar actualizaciones** en cualquiera de las tiendas (NVDA.ES u Oficial). Se mostrará una ventana con los complementos que tienen actualizaciones disponibles.

En esta ventana puedes:

- **Seleccionar complementos individualmente:** Usa la barra espaciadora para marcar/desmarcar.
- **Alt+S:** Seleccionar todos los complementos para actualizar.
- **Alt+D:** Deseleccionar todos los complementos.
- **Alt+A:** Iniciar la actualización de los complementos seleccionados.
- **Alt+C / Escape / Alt+F4:** Cerrar la ventana.

### Comprobación automática

Cuando actives la comprobación automática en las opciones:

- La tienda buscará actualizaciones en segundo plano según el intervalo configurado.
- Mostrará una notificación del sistema indicando cuántas actualizaciones hay y de qué fuente provienen.
- La búsqueda se detiene automáticamente después de 10 comprobaciones sin resultados, o 5 comprobaciones después de encontrar actualizaciones, para no saturar el servidor.

Las notificaciones ahora son más informativas:

```
Se encontraron 3 actualizaciones.
- NVDA.ES (2): Complemento A, Complemento B
- Tienda Oficial (1): Complemento C

Ejecute Buscar actualizaciones de complementos.
```

---

<a name="panel-de-opciones"></a>
## Panel de opciones

Accede a la configuración del complemento desde:

**Menú NVDA → Preferencias → Opciones → Tienda de Complementos NVDA**

### A. Tienda NVDA.ES

- **Seleccione un servidor de complementos:** Elige el servidor predeterminado entre los que tengas configurados.
- **Gestionar Servidores de complementos:** Abre el gestor donde puedes añadir, editar o eliminar servidores personalizados.

### B. Tienda Oficial NVDA

- **Habilitar tienda oficial de NVDA:** Activa o desactiva la integración con la tienda oficial de NV Access.
- **Permitir complementos incompatibles de la tienda oficial:** Permite intentar instalar complementos marcados como incompatibles. **Úsalo bajo tu responsabilidad.**

### C. Actualizaciones

- **Activar comprobación automática de actualizaciones:** Activa la búsqueda en segundo plano.
- **Tiempo para comprobar actualizaciones:** Elige el intervalo entre comprobaciones:
  - 15 minutos, 30 minutos, 45 minutos, 1 hora, 12 horas, 1 día, 1 semana.
- **Incluir actualizaciones de la tienda oficial:** Añade las actualizaciones de la tienda oficial a la comprobación automática.

### D. Traducción

- **Activar traductor para descripciones:** Habilita el uso de la tecla F3 para traducir.
- **Idioma para traducir descripciones:** Elige entre 12 idiomas: Alemán, Árabe, Croata, Español, Francés, Inglés, Italiano, Polaco, Portugués, Ruso, Turco y Ucraniano.

### E. Opciones Generales

- **Ordenar complementos alfabéticamente:** Ordena la lista de la A a la Z.
- **Instalar complementos después de descargar:** Abre el asistente de instalación automáticamente al terminar la descarga.
- **Instalar en silencio:** Los complementos se instalan en segundo plano sin diálogos intermedios. Solo pide reiniciar al finalizar.
- **Habilitar caché de servidores:** Almacena las listas de complementos en disco para una carga más rápida.
- **Actualizar caché cada...:** Configura el intervalo de renovación de la caché.
- **Usar caché para traducciones:** Las traducciones hechas con F3 se guardan para no repetir la consulta a Google.
- **Habilitar modo offline:** Permite navegar por la tienda sin conexión a internet, usando los datos guardados en caché.

### F. Backup y restauración

- **Crear Backup de complementos:** Genera un archivo JSON con la lista de todos tus complementos instalados.
- **Restaurar desde Backup:** Carga un archivo de backup y permite reinstalar los complementos listados.

### G. Complementos instalados que hay en el servidor

En la parte inferior de las opciones se muestra una lista de tus complementos que también están en el servidor. Desde aquí puedes:

1. Seleccionar un complemento y pulsar **Barra espaciadora**.
2. En el menú emergente, elegir el **canal de actualización** (Estable, Beta, Desarrollo, etc.) o **Descartar actualizaciones** para que la tienda deje de avisar sobre ese complemento.

> **Importante:** Los cambios solo se guardan al pulsar Aceptar o Aplicar en el diálogo de opciones.

---

<a name="sistema-de-cache"></a>
## Sistema de caché

La tienda implementa un sistema de caché multinivel para maximizar el rendimiento:

### Caché de servidores

Almacena las listas de complementos en disco. Cuando abres la tienda, si la caché no ha expirado, se carga directamente desde disco en lugar de hacer una petición al servidor.

- Se configura desde: **Habilitar caché de servidores** en las opciones.
- El intervalo de actualización es configurable.

### Caché de traducciones

Las traducciones realizadas con F3 se guardan en un archivo JSON persistente. La próxima vez que pidas la misma traducción, se cargará instantáneamente desde la caché.

- Se configura desde: **Usar caché para traducciones** en las opciones.

### Caché en memoria

Además de la caché en disco, la tienda mantiene una caché en memoria RAM para las consultas más frecuentes, eliminando completamente el acceso a disco durante la sesión.

---

<a name="modo-offline"></a>
## Modo offline

El modo offline permite navegar por la tienda **sin conexión a internet**, utilizando los datos almacenados previamente en la caché.

Para utilizarlo:

1. Asegúrate de tener activadas las opciones **Habilitar caché de servidores** y **Habilitar modo offline** en las opciones.
2. Navega por la tienda al menos una vez con conexión para que se genere la caché.
3. La próxima vez que abras la tienda sin internet, los datos se cargarán desde la caché.

> **Nota:** En modo offline no podrás descargar ni instalar complementos, pero sí podrás consultar la información de los complementos que visitaste previamente.

---

<a name="backup-y-restauracion"></a>
## Backup y restauración

### Crear backup

1. Ve a **Opciones → Tienda de Complementos NVDA → Crear Backup de complementos**.
2. Elige un nombre y ubicación para el archivo `.json`.
3. Se generará un archivo con la lista de todos tus complementos instalados, incluyendo nombre, versión y resumen.

### Backup automático al salir

La tienda crea automáticamente un backup al cerrar NVDA (configurable en las opciones).

### Restaurar desde backup

1. Ve a **Opciones → Tienda de Complementos NVDA → Restaurar desde Backup**.
2. Selecciona el archivo `.json` de backup.
3. La tienda mostrará un asistente que buscará las versiones más recientes de cada complemento en los servidores y te permitirá instalarlos por lotes.

> **Ideal para:** Migrar complementos a un nuevo equipo o recuperar tu configuración después de reinstalar NVDA.

---

<a name="traduccion-de-descripciones"></a>
## Traducción de descripciones

La tienda incluye un traductor integrado basado en Google Translate:

1. **Activa el traductor** desde las opciones del complemento.
2. **Selecciona el idioma destino** (Español por defecto).
3. **Pulsa F3** sobre cualquier complemento en la lista para traducir su descripción.

Características:

- Sonido de inicio y fin para indicar que la traducción se está realizando.
- Las traducciones se almacenan en caché para no repetir consultas.
- La traducción se pierde al cambiar de complemento; vuelve a pulsar F3 si la necesitas de nuevo.
- Requiere conexión a internet.

---

<a name="servidores-personalizados"></a>
## Servidores personalizados

Puedes añadir repositorios de complementos de terceros que usen el formato compatible con NVDA.ES.

### Añadir un servidor

1. Ve a **Opciones → Tienda de Complementos NVDA → Gestionar Servidores de complementos**.
2. Pulsa **Añadir**.
3. Introduce un nombre descriptivo y la URL del servidor.
4. Acepta y el servidor aparecerá en el selector de servidores.

### Ejemplo: Servidor de la comunidad rusa

- **Nombre:** Comunidad Rusa
- **URL:** `https://nvda-addons.ru/get.php?addonslist`

### Cambiar de servidor rápidamente

Desde la ventana principal de la tienda NVDA.ES, pulsa **Alt+C** o el botón **Cambiar de servidor** para desplegar un menú con todos los servidores configurados. El cambio es inmediato y temporal (no se guarda como predeterminado hasta que lo cambies en las opciones).

> **Nota:** El servidor predeterminado de la comunidad hispanohablante no puede ser modificado ni eliminado.

---

<a name="observaciones-y-protecciones"></a>
## Observaciones y protecciones

El complemento incluye múltiples protecciones para garantizar una experiencia segura:

1. **Complementos pendientes de desinstalar:** Se excluyen automáticamente de las comprobaciones de actualización.
2. **Validación de compatibilidad de API:** Aunque la versión del servidor sea más nueva, si no es compatible con tu versión de NVDA no se ofrecerá la actualización.
3. **Notificación de errores de instalación:** Si algún complemento no se pudo actualizar, se informa con su nombre.
4. **Bloqueo tras actualización:** La tienda no permite buscar más actualizaciones si ya se realizó una actualización y no se ha reiniciado NVDA.
5. **Notificación post-reinicio:** Si la comprobación automática detecta que no se ha reiniciado NVDA después de actualizar, emite una notificación recordatoria.
6. **Protección sin internet:** Si las librerías no se pueden cargar por falta de conexión, se informa en el registro de NVDA y se avisa con un mensaje hablado al intentar acceder a la tienda.
7. **Reinicio inteligente:** La tienda detecta automáticamente si realmente se instaló un complemento. Si cancelas el instalador, no te pedirá reiniciar innecesariamente.
8. **Comprobación de dependencias:** Antes de instalar, verifica que todas las dependencias requeridas estén satisfechas.

---

<a name="resumen-de-teclas-rapidas"></a>
## Resumen de teclas rápidas

### Ventana principal de la tienda

| Acción | Tecla |
|:-------|:------|
| Ir al cuadro de búsqueda | `Alt+B` |
| Ir a la lista de complementos | `Alt+L` |
| Instalar / Actualizar | `Alt+I` |
| Ir a la información del complemento | `Alt+I` (panel derecho) |
| Ir a la página web del complemento | `Alt+P` |
| Cambiar de servidor (solo NVDA.ES) | `Alt+C` |
| Cerrar la tienda | `Alt+S` / `Escape` / `Alt+F4` |

### En la lista de complementos

| Acción | Tecla |
|:-------|:------|
| Saber posición actual en la lista | `F1` |
| Explicar indicador de estado | `Ctrl+F1` |
| Leer ficha completa del complemento | `F2` |
| Traducir descripción | `F3` |
| Menú contextual (filtros, copiar, gestión) | `Tecla Aplicaciones` / `Shift+F10` |

### Ventana de actualizaciones

| Acción | Tecla |
|:-------|:------|
| Seleccionar todos los complementos | `Alt+S` |
| Deseleccionar todos | `Alt+D` |
| Iniciar actualización | `Alt+A` |
| Cerrar ventana | `Alt+C` / `Escape` / `Alt+F4` |

---
<a name="colaboradores"></a>
## Colaboradores

* Idioma turco (Umut Korkmaz)
* Idioma ruso (Valentín N. Kupriyanov)
* Idioma polaco (Kazimierz Parzych)

<a name="registro-de-cambios"></a>
## Registro de cambios

### Versión 2026.05.20

*Corregido  el actualizador silencioso de idiomas del complemento (en fase beta)

Agregadas las mejoras de Javi Dominguez (PR #1 y #2)

### Versión 2026.05.13

*Corregido  el actualizador silencioso de idiomas del complemento (en fase beta)

### Versión 2026.05.11

*Agregado un actualizador silencioso de idiomas del complemento (en fase beta)
* Agregado idioma ruso (Valentín N. Kupriyanov)

### Versión 2026.05.10

* Agregado idioma turco (Umut Korkmaz)

### Versión 2026.05.09

* Primera versión de la Tienda Unificada de Complementos para NVDA.
* Integración completa de la Tienda NVDA.ES y la Tienda Oficial de NV Access.
* Nuevo sistema de indicadores de estado: [I], [U], [D], [R], [I-I], [U-I], [X].
* Gestión local de complementos: deshabilitar, habilitar y desinstalar sin salir de la tienda.
* Sistema de caché multinivel: caché de servidores, caché de traducciones y caché de listas.
* Modo offline: navegación por la tienda sin conexión a internet usando datos almacenados en caché.
* Backup y restauración de complementos instalados.
* Empaquetador de complementos: genera archivos .nvda-addon desde complementos instalados.
* Comprobación inteligente de dependencias y compatibilidad de API.
* Instalación silenciosa con reinicio inteligente.
* Traducción de descripciones con caché persistente vía Google Translate.
* Soporte para servidores personalizados de complementos.
* Interfaz con teclas rápidas F1, Ctrl+F1, F2, F3 para acceso rápido a funciones.
* Notificaciones detalladas que indican origen de actualizaciones (ES / Oficial).

### Versiones anteriores (Tienda para NVDA.ES)

Este repositorio contenía anteriormente la versión clásica de la **Tienda para NVDA.ES** (versiones 0.1 a 0.10). A partir de la versión 2026.05.09, el repositorio ha sido reemplazado por la nueva **Tienda Unificada de Complementos para NVDA**, que es una reescritura completa del complemento.

Si deseas consultar el código fuente o la documentación de la versión antigua, puedes hacerlo navegando por el historial de commits del repositorio en GitHub:

1. Ve a [https://github.com/hxebolax/Tienda-para-NVDA](https://github.com/hxebolax/Tienda-para-NVDA).
2. Haz clic en el enlace de **commits** (o pulsa en el contador de commits que aparece en la parte superior del repositorio).
3. Busca cualquier commit anterior a la fecha **9 de mayo de 2026** para acceder al código y releases de la tienda clásica.
4. Una vez en el commit deseado, puedes pulsar **"Browse files"** para ver el estado completo del repositorio en ese momento.

Alternativamente, las releases antiguas con sus archivos `.nvda-addon` seguirán estando disponibles en la sección de [Releases](https://github.com/hxebolax/Tienda-para-NVDA/releases) del repositorio, siempre que no se eliminen manualmente.

---

¡Disfruta de la Tienda de Complementos para NVDA!

**Con cariño:** Héctor J. Benítez Corredera.
