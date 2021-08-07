# Manual de Tienda para NVDA
## Modo de uso

El complemento viene sin atajos y podemos otorgarle dos que son:

* Muestra la ventana con todos los complementos y su información: Se nos mostrara una ventana con todos los complementos que hay en https:www.nvda.es

* Busca actualizaciones de los complementos instalados: Analizara los complementos que tenemos y de los que encuentre actualización nos ofrecerá la posibilidad de actualizarlos de manera automática.

### Muestra la ventana con todos los complementos y su información

En esta pantalla tendremos todos los complementos junto a una ficha y la posibilidad de ir a su repositorio y descargar.

Si recorremos la ventana tendremos una lista con todos los complementos, un cuadro de solo lectura con la ficha del complemento que tengamos seleccionado, un botón descargar, un botón para ir a la pagina del complemento y un botón cerrar.

Además tendremos un cuadro de búsqueda en el cual podremos poner lo que deseemos buscar y si pulsamos intro se mostrara los resultados en la lista.

Bien para volver a tener toda la lista de complementos solo tendremos que volver al campo de búsqueda y borrar y pulsar intro con el campo vacío.

En el campo de la ficha en el caso que el complemento tenga más de una rama de desarrollo también se nos mostrara la información.

El botón descargar nos desplegara un menú con las distintas ramas de desarrollo del complemento, tendremos que elegir una para descargar. En caso que solo tenga una solo se nos dará esa opción.

En esta pantalla tenemos las siguientes teclas rápidas para movernos por la interface:

* Alt+B: Ir al cuadro de búsqueda.
* Alt+L: Ir a la lista de complementos.
* Alt+I: Ir al campo de la ficha para ver la información del complemento seleccionado.
* Alt+D: Ejecutar el botón descargar.
* Alt+P: Ir a la página del complemento.
* Alt+C, Escape, Alt+F4: Cerrar la ventana.

###  Busca actualizaciones de los complementos instalados

Nos dejara actualizar aquellos complementos que en https://www.nvda.es sean más nuevos que los que tenemos en nuestro equipo.

En esta pantalla podremos seleccionar en caso de que hubiese actualizaciones aquellos complementos que deseemos actualizar.

Tendremos que marcar con espacio el complemento y darle a Actualizar.

Actualmente solo se permite actualizar la rama principal del complemento. Si tenemos un complemento que tiene varias ramas y estamos en la rama de desarrollo tendremos que actualizar de manera manual.

En caso que solo sea un complemento que tenga rama de desarrollo y sea su única rama se podrá actualizar sin problemas.

Solo se actualizara la rama principal del complemento.

Se esta trabajando para poder ofrecer el elegir que rama deseamos para cada complemento.

En esta pantalla tenemos las siguientes teclas:

* Alt+A: Empezara la actualización de aquellos complementos que tengamos seleccionados.
* Alt+C, Alt+F4 o Escape: Cerrara la ventana.

### Panel de opciones

Podremos configurar algunos aspectos de la tienda en NVDA / Preferencias / Opciones y buscar la categoría Tienda NVDA.ES.

Actualmente podremos seleccionar si deseamos Activar o desactivar la comprobación de actualizaciones.

Si activamos esta casilla se activará un cuadro combinado en el cual podremos elegir cuanto tiempo transcurrirá entre una comprobación y otra.

Decir que Activar o desactivar la comprobación de actualizaciones viene desactivado por defecto.

El comportamiento de esta opción es simple, buscara en el servidor si existen actualizaciones en el rango de tiempo dado y nos notificara con una notificación de sistema diciendo cuantas actualizaciones hay y que abramos la correspondiente opción de la tienda para actualizar.

Decir que si esta opción se activa buscara 10 veces el rango del tiempo dado y luego se desactivara. Esto es para no saturar a llamadas al servidor.

Por lo tanto, si tenemos 15 minutos asignados y no encuentra actualizaciones a las 2h 30 min dejara de buscar actualizaciones.

En caso de que si haya actualizaciones buscara 5 veces más el rango de tiempo dado y luego se desactivara, cada vez nos avisara de que se encontraron actualizaciones hasta que actualicemos.

## Observaciones

Se agrego una protección la cual no permitirá seguir buscando actualizaciones si ya hemos realizado una actualización de un complemento o de varios y no hemos decidido reiniciar NVDA.
Si tenemos activada la búsqueda de actualizaciones automática cada vez que busque y detecte que no hemos reiniciado NVDA se nos notificara con una notificación de sistema.

Igualmente, si intentamos activar la pantalla de buscar actualizaciones y no hemos reiniciado NVDA el lector nos hablara el mensaje que tenemos que reiniciar el NVDA para aplicar las actualizaciones.

Este complemento esta en fase de prueba por lo que le pedimos que entienda que pueden haber errores.

Le agradecemos se ponga en contacto para reportarlos y poder solucionarlos a la mayor brevedad.

