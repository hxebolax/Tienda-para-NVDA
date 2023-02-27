# Manual de Tienda para NVDA.ES
## Modo de uso

El complemento viene sin atajos asignados y podemos otorgarle dos que son:

* Muestra la ventana con todos los complementos y su información: Se nos mostrara una ventana con todos los complementos que hay en https:www.nvda.es

* Busca actualizaciones de los complementos instalados: Analizará los complementos que tenemos y de los que encuentre actualización nos ofrecerá la posibilidad de actualizarlos de manera automática.

Podemos asignar un gesto de entrada para estas dos opciones yendo al menú de NVDA / Preferencias / Gestos de entrada y buscar Tienda para NVDA.ES.

### Muestra la ventana con todos los complementos y su información

En esta pantalla tendremos todos los complementos junto a una ficha y la posibilidad de ir a su repositorio y descargar.

Si recorremos la ventana tendremos una lista con todos los complementos, un cuadro de solo lectura con la ficha del complemento que tengamos seleccionado, un botón llamado "Descargar complemento", un botón llamado "Visitar página WEB" para ir a la pagina del complemento y un botón llamado "Salir".

Además, tendremos un cuadro de búsqueda en el cual podremos poner lo que deseemos buscar y si pulsamos Intro se mostrara los resultados en la lista.

Bien para volver a tener toda la lista de complementos solo tendremos que volver al campo de búsqueda y borrar su contenido y pulsar Intro con el campo vacío.

En el campo de la ficha en el caso que el complemento tenga más de una rama de desarrollo también se nos mostrara la información.

El botón llamado "Descargar complemento", nos desplegara un menú con las distintas ramas de desarrollo del complemento, tendremos que elegir una para descargar. En caso de que solo tenga una solo se nos dará esa opción.

En esta pantalla tenemos las siguientes teclas rápidas para movernos por la interface:

* Alt+B: Ir al cuadro de búsqueda.
* Alt+L: Ir a la lista de complementos.
* Alt+I: Ir al campo de la ficha para ver la información del complemento seleccionado.
* Alt+D: Ejecutar el botón "Descargar complemento".
* Alt+P: Ir a la página del complemento.
* Alt+S, Escape, Alt+F4: Cerrar la ventana.

#### Menú contextual en la lista de complementos

En la lista de complementos podemos desplegar un menú contextual ya sea con la tecla Aplicaciones de nuestro teclado o bien Shift + F10 para aquellos teclados que no dispongan de la tecla Aplicaciones.

Dicho menú consta de dos submenús:

Filtros y Copiar al portapapeles.

En el submenú "Filtros" tenemos las siguientes opciones:

* Mostrar todos los complementos: Esta opción es la predefinida siempre que el complemento se ejecute por primera vez.

Dicha opción nos mostrara todos los complementos que hay en la base de datos.

Igualmente esta opción está supeditada si tenemos marcada la casilla de verificación "Ordenar por orden alfabético los complementos de la tienda y las búsquedas", por lo tanto si dicha casilla de verificación en opciones está marcada la lista se ordenara alfabéticamente al igual que las búsquedas en dicha lista.

* Mostrar los complementos con compatibilidad de API 2022: Esta opción nos mostrara solo aquellos complementos que en el manifiesto estén marcados con dicha compatibilidad.

* Mostrar los complementos con compatibilidad de API 2021: Esta opción nos mostrara solo aquellos complementos que en el manifiesto estén marcados con dicha compatibilidad.

Igualmente esta opción está supeditada si tenemos marcada la casilla de verificación "Ordenar por orden alfabético los complementos de la tienda y las búsquedas", por lo tanto si dicha casilla de verificación en opciones está marcada la lista se ordenara alfabéticamente al igual que las búsquedas en dicha lista.

Advertir que en esta lista se omitirán aquellos complementos que los autores en su manifiesto han ignorado la buena praxis y han puesto compatibilidad con APIS que todavía no han llegado.

* Mostrar los complementos ordenados por autor: Esta opción nos mostrara la lista de complementos pero se ordenara por nombre de autor.

* Mostrar por descargas de mayor a menor: Esta opción nos mostrara todos los complementos pero será ordenada por el número de descargas que tenga el complemento.

Estas opciones se ejecutan individualmente no siendo acumulable su resultado.

Cada opción cuando la elijamos cambiara el titulo de la ventana para informarnos que filtro esta activo.

Las opciones se mantienen para las siguientes veces que se active la tienda hasta que NVDA sea reiniciado. Una vez reiniciado el complemento vuelve a su valor predefinido y la lista cargada por primera vez será "Mostrar todos los complementos"

Salvo la opción "Mostrar todos los complementos", el resto de opciones solo se filtra por la primera rama de desarrollo. Si un complemento tiene más de una rama no se tendrán en cuenta salvo la rama principal para filtrar los resultados en cada opción.

En el submenú "Copiar al portapapeles" tenemos las siguientes opciones:

* Copiar información: Si elegimos esta opción se copiara la ficha entera del complemento que tengamos elegido al portapapeles.

* Copiar enlace a la página web del complemento: Si elegimos esta opción se copiara la URL de la página oficial del complemento al portapapeles.

* Copiar enlace de descarga del complemento: Bien esto es un submenú que contendrá dentro las ramas de desarrollo del complemento. Cuando elijamos alguna si tiene más de una nos copiara al portapapeles la URL para poder descargar el complemento.

### Busca actualizaciones de los complementos instalados

Nos dejara actualizar aquellos complementos que en https://www.nvda.es sean más nuevos que los que tenemos en nuestro equipo.

En esta pantalla podremos seleccionar en caso de que hubiese actualizaciones aquellos complementos que deseemos actualizar.

Tendremos que marcar con la barra espaciadora el complemento deseado y darle al botón "Actualizar".

En esta pantalla se nos mostrara la actualización correspondiente si la hay a la rama que tengamos elegida yendo al menú de NVDA / Preferencias / Opciones / Tienda NVDA.ES y allí podremos elegir si hay más de una rama de desarrollo la que deseemos (explicado bien en el siguiente apartado)

En esta pantalla tenemos las siguientes teclas:

* Alt+S: Seleccionara todos los complementos de la lista para instalar todas las actualizaciones de nuestros complementos que tengamos instalados en nuestra computadora.
* Alt+D: Nos deseleccionara de la lista todas las actualizaciones de todos los complementos si habían sido marcados previamente.
* Alt+A: Empezara la actualización de aquellos complementos que tengamos seleccionados en la lista.
* Alt+C, Alt+F4 o Escape: Cerrara la ventana.

### Panel de opciones

Podremos configurar algunos aspectos del complemento "TiendaNVDA" yendo al menú de NVDA / Preferencias / Opciones y buscar la categoría Tienda NVDA.ES.

* Activar o desactivar la comprobación de actualizaciones.

Si activamos esta casilla de verificación se activará un cuadro combinado en el cual podremos elegir cuanto tiempo transcurrirá entre una comprobación y otra.

Decir que la casilla de verificación "Activar o desactivar la comprobación de actualizaciones" viene desactivado por defecto.

El comportamiento de esta opción es simple, buscara en el servidor si existen actualizaciones en el rango de tiempo dado y nos notificara con una notificación de sistema diciendo cuantas actualizaciones hay y que abramos la correspondiente opción en el complemento Tienda NVDA para actualizar.

Decir que si esta opción se activa buscara 10 veces el rango del tiempo dado y luego se desactivara. Esto es para no saturar las llamadas al servidor.

Por lo tanto, si tenemos 15 minutos asignados y no encuentra actualizaciones a las 2h 30 min dejara de buscar actualizaciones.

En caso de que si haya actualizaciones buscara 5 veces más el rango de tiempo dado y luego se desactivara, cada vez nos avisara de que se encontraron actualizaciones hasta que actualicemos.

* Ordenar por orden alfabético los complementos de la tienda y las búsquedas.

Si marcamos esta casilla de verificación, cuando abramos la tienda se nos mostrara los complementos por orden alfabético. También si buscamos algún complemento los resultados de las búsquedas se mostrarán en orden alfabético.

* Instalar complementos después de descargar.

Si marcamos esta casilla de verificación, cuando se termine de descargar un complemento nos pedirá desde el asistente de instalación de complementos de NVDA que si queremos instalar.

* Complementos instalados que hay en el servidor.

Bien en esta lista se nos mostrarán aquellos complementos que tengamos instalados y que a su vez se encuentren en el servidor.

Solo se mostrarán aquellos que además tengan compatibilidad con la Api actual de NVDA.

En esta lista podremos elegir que rama de actualización queremos para el complemento. Si pulsamos barra espaciadora encima de un complemento se nos desplegara todas las ramas de desarrollo para ese complemento. Podremos elegir la que deseemos con Intro y se nos quedara guardada la selección en la lista.

ADVERTENCIA: Los cambios en la lista solo se guardarán si damos al botón aceptar o Aplicar del dialogo de opciones.

Esta lista se actualiza cada vez que reiniciemos NVDA añadiendo si hay nuevos complementos o eliminando aquellos que ya no estén.

Por lo tanto, si eliminamos un complemento y luego lo volvemos a instalar tendremos que volver a seleccionar la rama que deseamos de nuevo.

Esta lista tanto la primera vez que se genere como cada vez que se agregue un complemento siempre pondrá por defecto la primera rama de desarrollo que hay en el servidor.

## Observaciones

Cuando compruebe si hay actualizaciones ahora tiene dos protecciones:

1º Comprobara si hay complementos que van a ser desinstalados.

Si es así esos complementos se excluyen, aunque haya actualizaciones.

2º Se validará que el complemento que hay en el servidor cumple con los requisitos de API del NVDA que tenemos instalado.

Si esto no se cumple, el complemento no podrá ser instalado, aunque la versión del servidor sea más nueva y el servidor nos ofrezca ese complemento.

A la hora de instalar se han incluido también varias protecciones:

1º Ahora nos avisará si algún complemento no a podido ser actualizado y nos dará su nombre.

2º En este paso también se comprobará si el complemento para instalar tiene la versión mínima para ser usado en el NVDA que tengamos instalado.

3º El complemento "TiendaNVDA" no permitirá seguir buscando actualizaciones si ya hemos realizado una actualización de un complemento o de varios y no hemos decidido reiniciar NVDA.

4º Si tenemos activada la opción llamada "Busca actualizaciones de los complementos instalados" cada vez que busque y detecte que no hemos reiniciado NVDA se nos notificara con una notificación de sistema.

5º Igualmente, si intentamos activar la opción llamada “Busca actualizaciones de los complementos instalados" y no hemos reiniciado NVDA el lector nos verbalizara el mensaje que tenemos que reiniciar el NVDA para aplicar las actualizaciones.

6º En el peor de los casos si las librerías no dejan cargar porque no tengamos internet, se nos mostrara mensajes de información en el registro de NVDA y además si intentamos acceder a la tienda se nos avisara con un mensaje hablado.

Se mejoro la función que busca actualizaciones, ahora es mucho más fiable y además añade a su vez las protecciones mencionadas con anterioridad.

Se hicieron muchas mejoras internas para hacerlo más robusto.

Este complemento esta en fase de prueba por lo que le pedimos que entienda que puede haber errores.

Le agradecemos se ponga en contacto para reportarlos y poder solucionarlos a la mayor brevedad.

¡Disfruta de la Tienda para NVDA.ES!
# Registro de cambios.
## Versión 0.9.1

* Solucionado problemas con complementos grandes.

En esta versión se implementa una nueva manera de descargar y guardar los archivos de complementos.

Ahora en complementos mayores de 20 MB no dará el tamaño que lleva descargado y nos dará un mensaje de complemento grande.

Podremos seguir el porcentaje de lo que llevamos descargado del complemento grande gracias a la barra de progreso.

Esto ahora ya debería solucionar los problemas que algunos les ocasionaba el actualizar o descargar complementos grandes dándoles error y bloqueando o reiniciando NVDA.

Esto se aplica a las descargas individuales que hagamos de complementos como a las actualizaciones que encuentre el complemento y su posterior descarga.

## Versión 0.9

* Compatibilidad API 2023

## Versión 0.8.5

* Solución de errores con la mala praxis de los desarrolladores que no siguen los estándares de los manifiestos.

Ejemplo:

minimumNVDAVersion = None (MUY MAL) no cuesta nada un simple 2019.3.0 son simplemente 8 caracteres puñetas.

## Versión 0.8.4.

* Solucionado problema con versiones tipo fecha

* Actualizados idiomas turco y inglés automático

* Sizers actualizados para su correcta visualización

## Versión 0.8.3.

* Solucionado el problema al cargar la tienda Expecting value: line 1 column 1 (char 0).

* Agregado botón Buscar y botón Acciones.

Ahora en la pantalla principal de la Tienda tendremos dos nuevos botones.

- Buscar que hará lo mismo que si diésemos intro en el campo de búsqueda pero que se agrega para personas que usen la voz, pantallas táctiles y otros problemas de movilidad.

Dicho botón tiene el atajo Alt+U:

- También se agrego el botón Acción el cual nos mostrara el menú contextual del complemento que tengamos seleccionado en la lista de complementos.

Desde dicho menú podremos acceder a los filtros o copiado al portapapeles.

Se agrego por los mismos motivos que el botón Buscar.

Dicho botón tiene el atajo Alt+A.

* Agregada la posibilidad de ver la documentación de complementos instalados

En la pantalla principal de la Tienda en la lista de complementos si pulsamos tecla Aplicaciones, Shift+F10 o el botón Acción Alt+A y el complemento que esta en el foco lo tenemos instalado en el menú que se ofrece nos saldrá una nueva opción.

Dicha opción es Ver documentación del complemento instalado, si pulsamos hay nos abrirá nuestro navegador con la documentación del complemento.

Decir que si la documentación esta en nuestro idioma se abrirá en nuestro idioma de lo contrario se abrirá en el idioma definido por el complemento.

Igualmente hay complementos que no traen documentación en este caso no se mostrara dicha opción ni en aquellos que no tengamos instalados.

* Agregada posibilidad de lanzar la documentación del complemento fácilmente.

Ahora desde el menú de NVDA Herramientas / Tienda NVDA.ES tendremos una nueva opción que es Documentación del complemento.

Si le damos se abrirá en nuestro navegador predeterminado la documentación de la Tienda en nuestro idioma si esta o en defecto la documentación en Español.

## Versión 0.8.2.

* Actualizado idioma y documentación en Ucraniano.

* Solucionado problema con compatibilidad de complementos.

Ahora debería solo ofrecer actualizaciones que además sean compatible con nuestra API de NVDA.

Aunque la versión del complemento en el servidor sea mayor que la que tenemos instalada si la compatibilidad de API no es correcta no se nos ofrecerá dicha actualización.

* Solucionado la actualización de la lista de complementos instalados que hay en el servidor.

Ahora ya guarda bien la lista cuando instalamos un complemento y comprueba correctamente si esta en el servidor.

En la ultima versión no guardaba los nuevos complementos instalados.

## Versión 0.8.1.

* Solucionado problema al conectarse a un servidor sin complementos.

* Solucionado las descargas desde nuevos servidores

* Solucionado la conexión a servidores Onion tanto públicos como privados a través de Proxy

## Versión 0.8.

* Añadida la posibilidad de agregar URLs personalizadas de repositorios de complementos.

Esta nueva función vendrá bien para agregar aquellos repositorios que usen el gestor de complementos que usa nvda.es para más información visitar el repositorio de Github:

[https://github.com/nvda-es/advancedAddonFiles](https://github.com/nvda-es/advancedAddonFiles)

Bien quien use dicha aplicación para crear un repositorio ahora podrá agregar su URL a la Tienda.

En las opciones de la Tienda tendremos nada más entrar un cuadro combinado donde podremos elegir el servidor que deseamos por defecto.

La primera vez que iniciemos las opciones solo estará el servidor de la comunidad hispanohablante, decir que este servidor no puede ser modificado ni borrado por lo que siempre estará presente.

Si tabulamos tendremos un botón para gestionar los servidores y si lo pulsamos se abrirá una ventana donde podremos añadir, editar o borrar servidores.

Si pulsamos añadir se abre una ventana donde tendremos que rellenar el nombre que deseamos para el servidor y la url del servidor.

Si editamos se abre una ventana con los datos del servidor que tengamos seleccionado en la lista para poder ser modificados.

Si borramos se nos advertirá con un mensaje que la acción no es reversible por lo que si damos a si se borrara el servidor que tengamos seleccionado.

Una vez agregados servidores y cerrada la ventana de gestión de servidores podremos elegir en el cuadro combinado el que deseemos. Cuando seleccionemos un servidor se actualizará el estado de Complementos instalados que hay en el servidor añadiendo a dicho cuadro solo los complementos que en ese momento el servidor sirva y nosotros tengamos instalados.

Decir que este cuadro es para cada servidor por lo que si en la comunidad hispanohablante tenemos configuraciones personalizadas en nuestros complementos como por ejemplo evitar la actualización de alguno u otro canal de actualización solo será para cuando elijamos dicho servidor.

Las demás opciones de la Tienda son globales.

El servidor que elijamos en las opciones de la tienda será el predefinido cada vez que arranquemos NVDA y la Tienda.

También se agrego en la ventana principal de la Tienda la posibilidad de cambiar rápidamente de servidor sin necesidad de entrar en opciones.

Para ello se agrego el atajo Alt+C el cual desplegará un menú con los servidores que tenemos y estará marcado el que actualmente este definido. Igualmente podemos tabular hasta encontrar en la interface el botón llamado Cambiar de servidor para desplegar dicho menú.

En dicho menú podemos elegir el que deseemos y automáticamente cambiaremos a dicho servidor.

Si cambiamos desde la pantalla principal dicho ajuste no se guardará cuando iniciemos de nuevo NVDA siempre será el servidor predefinido el que tengamos configurado en opciones.

## Versión 0.7.1.

* Agregada opción para poder traducir las descripciones de los complementos.

Ahora pulsando F3 desde la lista de complementos o desde la ficha de un complemento se traducirá la descripción al idioma que tengamos configurado en opciones.

Esta nueva característica viene desactivada por defecto, para activarla tendremos que ir a las opciones de la Tienda y activar la opción Activar o desactivar el traductor para las descripciones de los complementos.

A continuación tabulamos y elegimos el idioma que deseamos que se traduzcan las descripciones.

Cuando pulsemos F3 sonara un sonido de inicio y otro de fin para anunciar que se terminó de traducir. Estos sonidos son diferentes entre sí.

Cuando cambiemos de complemento la traducción se pierde por lo que si deseamos de nuevo ver la traducción de la descripción tendremos que volver a pulsar F3.

Esta opción requiere de internet para ser usada.

* Solucionado un problema al recargar los complementos.

## Versión 0.7.

* Solucionado problema con los filtros.

En ocasiones no dejaba regresar del filtro por descargas al filtro todos los complementos.

* Añadidos nuevos tiempos para buscar actualizaciones.

Se añadió 12 horas, 1 día y 1 semana.

Estos tiempos irán bien para ordenadores que se reinicien muy poco.

* Añadida la posibilidad de no buscar actualizaciones para un complemento.

Esta opción podremos usarla de la siguiente manera, en opciones de la tienda en la lista que nos da con los Complementos instalados que hay en el servidor podremos ponernos encima del complemento que deseemos que no se busquen actualizaciones y dar espacio.

En el menú desplegable ahora aparte de poder elegir el canal que deseamos tener de actualizaciones podremos elegir Descartar actualizaciones.

Cuando lo seleccionemos y demos a aceptar los complementos que tengan el valor de Descartar actualizaciones no buscaran actualizaciones en el servidor.

Para revertir este aspecto tendremos que volver a la misma lista y dar espacio y elegir el canal de actualización que deseamos.
