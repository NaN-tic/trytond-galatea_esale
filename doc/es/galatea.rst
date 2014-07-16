#:before:galatea/galatea:section:ficheros_estaticos#

.. inheritref:: galatea_esale/galatea:section:catalogo

--------
Catálogo
--------

Esta App dispone la funcionalidad de la visualización de nuestros productos en
formato de catálogo (al estilo de ecommerce o tienda electrónica).

La gestión de nuestro catálogo viene estructurado por:

* Menús (categorías). Árbol de navegación de nuestro catálogo.
* Productos.
* Imágenes. Adjuntos de los productos para visualizar imágenes.

.. inheritref:: galatea_esale/galatea:section:menus

Menús
-----

Para la gestión de menús accede a |menu_menu_tree|. Los menús se caracterizan en una
navegación al estilo de árbol.

* topmenu

 * Hogar

   * Neveras
   * Lavadoras

 * Ocio

   * TV
   * Música

 * Accesorios

Los menús son lo que en otras tiendas llaman categorías. En este caso evitamos usar el termino
categoría para no confundir con la categoría del producto que nos sirve esta categoría más
para tarifas de precios, impuestos o para la realización de informes. Los menús simplemente
es una categorización de los productos a nivel de navegación o usabilidad.

Como todo registro web deberá tener en cuenta:

* Slug: Es el ID o clave del vuestro registro. Sólo debe usar los caracteres az09-
  (sin acentos ni espacios). Este campo debe ser único ya que no pueden haber más
  de dos o más slugs en sus menús. Recuerde que es un campo multi idioma.
  Cuando introduzca un título se le propone un slug a partir del título que después
  lo podrá cambiar. Un slug podría ser 'ocio' y crearía una dirección como
  http://www.midominio.com/es/catalog/categoria/ocio
* SEO MetaKeyword. Introduce palabras clave de su artículo separados por comas
  (no más de 155 caracteres) que se usará para los buscadores. Un ejemplo de MetaKeyword
  podría ser "ocio,tv,música". Recuerde que es un campo multi idioma.
* SEO MetaDescription. Introduce una descripción breve del artículo (el resumen)
  (no más de 155 caracteres) que se usará para los buscadores. Un ejemplo de MetaDescription
  podría ser "El mejor ocio lo encontrará en MiTienda.com". Recuerde que es un
  campo multi idioma.
* SEO MetaTitle. Si el título del artículo en los buscadores desea que sea diferente del nombre
  del artículo puede usar este campo para cambiarlo. Recuerde que es un campo multi idioma.

A cada producto se le puede relacionar con X menús en la pestaña **eSale**. El orden de visualización
de los productos por cada menú vendrá decidido por el campo **Ordenación**:

* Por defecto.
* Posición (el campo secuencia del producto).
* Nombre.
* Precio.

Para acceder al listado de menús de nuestra web podemos acceder a la dirección:

* Español: http://www.midominio.com/es/catalog/categoria/
* Catalan: http://www.midominio.com/ca/catalog/categoria/
* Inglés: http://www.midominio.com/en/catalog/category/

Se nos listaran todas los menús en forma de árbol. Es la base para que buscadores
o usuarios accedan a nuestro catálogo de productos.

Para acceder al listado de productos en una categoría en nuestra web podemos
acceder a la dirección:

* Español: http://www.midominio.com/es/catalog/categoria/ejemplo-menu
* Catalan: http://www.midominio.com/ca/catalog/categoria/exemple-menu
* Inglés: http://www.midominio.com/en/catalog/category/menu-example

.. important:: Si cambia el nombre del menú, el slug se volverá a generar.
              Debe tener cuidado con esta acción pues si su página ya está indexada
              por los buscadores y cambia las urls o slugs, estas páginas ya no se van
              a encontrar y devolverá el "Error 404. Not Found". En el caso que desea cambiar
              las url's contacte con el administrador para que le active las redirecciones
              y evitar páginas no encontradas.

.. |menu_menu_tree| tryref:: product_esale.menu_menu_tree/complete_name

.. inheritref:: galatea_esale/galatea:section:productos

Productos
---------

Para la gestión de los productos lo haremos en los productos a |menu_template|.
Los productos activos al canal web deberán tener activado la opción **eSale**.

Como todo registro web deberá tener en cuenta:

* Slug: Es el ID o clave del vuestro producto. Sólo debe usar los caracteres az09-
  (sin acentos ni espacios). Este campo debe ser único ya que no pueden haber más
  de dos o más slugs en sus productos. Recuerde que es un campo multi idioma.
  Cuando introduzca un título se le propone un slug a partir del título que después
  lo podrá cambiar. Un slug podría ser 'mi-producto' y crearía una dirección como
  http://www.midominio.com/es/catalog/producto/mi-producto
* SEO MetaKeyword. Introduce palabras clave de su artículo separados por comas
  (no más de 155 carácteres) que se usará para los buscadores. Un ejemplo de MetaKeyword
  podría ser "ocio,mi producto,reproductor,fabricante". Recuerde que es un campo multi idioma.
* SEO MetaDescription. Introduce una descripción breve del artículo (el resumen)
  (no más de 155 carácteres) que se usará para los buscadores. Un ejemplo de MetaDescription
  podria ser "Mi producto disponible al mejor precio en MiTienda.com". Recuerde que es un
  campo multi idioma.
* SEO MetaTitle. Si el título del artículo en los buscadores desea que sea diferente del nombre
  del artículo puede usar este campo para cambiarlo. Recuerde que es un campo multi idioma.

A cada producto se le puede relacionar con X menús en la pestaña **eSale**. No olvide de
seleccionar los menús que estará disponible el producto.

Un producto puede estar visible en:

* Todo
* Sólo en búsquedas
* Sólo en el catálogo
* En ningún sitio

Para la descripción del producto usaremos los campos:

* Descripción corta. Smilar al campo SEO MetaDescription. Una descripción de unos
  80-100 caracteres. Estas descripciones se muestran en listados de productos.
* Descripción. El contenido o descripción del producto. Para el contenido de un producto puede
  usar los tags de Wiki para dar formato a su contendido. Los tags de wiki le permite formatear
  el texto para después sea mostrado con HTML. Para información de los tags de wiki puede consultar
  `MediaWiki <http://meta.wikimedia.org/wiki/Help:Editing>`_ Un recomendación es usar listas
  para la descripción de los productos. Y recuerden de añadir "palabras clave". Si nuestro producto
  es un reproductor y nos gusta que nos encuentren con la palabra "reproductor", en nuestro contenido
  debe aparecer la palabra "reproductor".

Los productos relacionados, ventas cruzadas o ventas sugeridas se usan para mostrar productos
similares en este productos. La visualización de estos contenidos ya viene definido según
el diseño y plantilla de nuestra web (técnico).

Para acceder al detalle o descripción de nuestro producto accederemos a la dirección:

* Español: http://www.midominio.com/es/catalog/producto/mi-producto
* Catalan: http://www.midominio.com/ca/catalog/producte/meu-producte
* Inglés: http://www.midominio.com/en/catalog/product/my-product

En esta sección verá el contenido del producto y su información. En el caso de que trabaje
en variantes de producto y disponga activado el carrito o cesta de la compra, se listarán
todas las variantes disponibles para la compra. En el caso que sólo trabaje en una sola variante
(productos simples) sólo se mostrará una variante.

Para desactivar un producto de nuestra web lo recomendable es desactivar la opción **Activo** de
la pestaña "eSale". En el caso de que se pueda comprar este producto quedará desactivado la compra
y un mensaje en el producto le informará que este producto ya no está disponible. No se recomienda
eliminar productos una vez publicados ya que en estos casos recibiremos por parte de los usuarios
o buscadores el "Error 404. Not Found". En el caso que desea eliminar el producto consulte con
su administrador para que le redireccione las direcciones antiguas por las nuevas y evitar perder
visitas.

.. important:: Si cambia el nombre del producto, el slug se volverá a generar.
              Debe tener cuidado con esta acción pues si su página ya está indexada
              por los buscadores y cambia las urls o slugs, estas páginas ya no se van
              a encontrar y devolverá el "Error 404. Not Found". En el caso que desea cambiar
              las url's contacte con el administrador para que le active las redirecciones
              y evitar páginas no encontradas.

.. |menu_template| tryref:: product.menu_template/complete_name

.. inheritref:: galatea_esale/galatea:section:tiendas

Tiendas
-------

Cada web es una tienda en nuestro ERP. De este modo podemos tener tiendas físicas
como tiendas virtuales (ecommerce o esale) en nuestro ERP.

.. important:: En nuestros productos, es importante que seleccione a que tienda
              desea que esté disponible el producto.

.. inheritref:: galatea_esale/galatea:section:precios

Precios
-------

La visualización de los precios de los productos dependerá de la configuración global de
nuestra web y la configuración de la web en relación con la tienda ( |menu_sale_shop| ).

El valor del precio vendrá decidido por las configuración de la tienda. En la configuración
de la tienda y precio disponemos:

* Precio venta. El precio de venta del producto.
* Tarifa. El precio se calcula según tarifa de la tienda. Si el usuario (tercero) se ha
  identificado (iniciado sesión) y dispone de una tarifa diferente de la tienda, se usará
  la tarifa del cliente (tercero).

.. |menu_sale_shop| tryref:: sale_shop.menu_sale_shop/complete_name

.. inheritref:: galatea_esale/galatea:section:imagenes

Imagenes
--------

En los productos como todo registro a Tryton se pueden usar adjuntos. Mediante los adjuntos
añadimos imágenes a nuestros productos. Podemos añadir tantas imágenes como queremos.

Para que los adjuntos o imágenes esten disponibles a nuestra web, deberemos marcar la opción
**Disponible eSale**. Si queremos publicar varias imágenes también podemos especificar que imagen
se usará como base, miniatura o no se va a mostrar.

.. important:: Las imágenes deberán ser en formato jpg o png, a 72 de resolución, no más
              grandes de 800x800 pixeles (recomendable formato cuadrado) y a RGB. También
              se recomienda los nombres de las imágenes no usar ni espacios ni acentos,
              sólo los caracteres az09- como el nombre del fichero todo en minúsculas.
              También se recomienda que el nombre del fichero tenga una relación con el producto.
              Un ejemplo seria: 0001-mi-producto.jpg
