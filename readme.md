# Manual de Tienda para NVDA
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

Podremos configurar algunos aspectos del complemento TiendaNVDA yendo al menú de NVDA / Preferencias / Opciones y buscar la categoría Tienda NVDA.ES.

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

3º El complemento Tienda NVDA no permitirá seguir buscando actualizaciones si ya hemos realizado una actualización de un complemento o de varios y no hemos decidido reiniciar NVDA.

4º Si tenemos activada la opción llamada "Busca actualizaciones de los complementos instalados" cada vez que busque y detecte que no hemos reiniciado NVDA se nos notificara con una notificación de sistema.

5º Igualmente, si intentamos activar la opción llamada “Busca actualizaciones de los complementos instalados" y no hemos reiniciado NVDA el lector nos verbalizara el mensaje que tenemos que reiniciar el NVDA para aplicar las actualizaciones.

6º En el peor de los casos si las librerías no dejan cargar porque no tengamos internet, se nos mostrara mensajes de información en el registro de NVDA y además si intentamos acceder a la tienda se nos avisara con un mensaje hablado.

Se mejoro la función que busca actualizaciones, ahora es mucho más fiable y además añade a su vez las protecciones mencionadas con anterioridad.

Se hicieron muchas mejoras internas para hacerlo más robusto.

Este complemento esta en fase de prueba por lo que le pedimos que entienda que puede haber errores.

Le agradecemos se ponga en contacto para reportarlos y poder solucionarlos a la mayor brevedad.

¡Disfruta de la Tienda para NVDA!
