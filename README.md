#ABCC

Programa ABCC (Alta-Baja-Cambio-Consulta) de artículos con los siguientes requisitos:
La interfaz deberá contar con los siguientes datos:
* Sku: Carácter tipo numérico con una longitud máxima de 6 dígitos.
* Artículo: Carácter tipo texto con una longitud máxima de 15 dígitos.
* Marca: Carácter tipo texto con una longitud máxima de 15 dígitos.
* Modelo: Carácter tipo texto con una longitud máxima de 20 dígitos.
* Departamento: Carácter numérico con una longitud de 1 dígitos.
* Clase: Carácter numérico con una longitud de 2 dígitos.
* Familia: Carácter numérico con una longitud de 3 dígitos.
* Fecha de Alta: Tipo fecha.
* Stock: Carácter tipo numérico con una longitud máxima de 9 dígitos.
* Cantidad: Carácter tipo numérico con una longitud máxima de 9 dígitos.
* Descontinuado: Carácter tipo numérico con una longitud máxima de 1 dígito.
* Fecha Baja: Tipo fecha.

Alta:
Al ingresar al programa el usuario sólo deberá poder capturar el Sku, una vez capturado se deberá validar si existe. En el caso de no existir, el usuario podrá ingresar los datos de Artículo, Marca, Modelo, Departamento, Clase, Familia, Cantidad y Stock; el resto de los datos no deberán mostrarse o deberán mostrarse desactivados.
Los datos Fecha de Alta, Descontinuado y Fecha Baja deberán guardarse de la siguiente forma:
Fecha de Alta: Fecha actual Descontinuado: 0
Fecha Baja: 1900-01-01

Baja:
Al ingresar al programa el usuario sólo deberá poder capturar el Sku, una vez capturado se deberá validar si existe. En el caso de existir, se deberá mostrar un botón con la opción para eliminar y al hacer uso de él se deberá solicitar una confirmación para realizar la acción.

Cambio:
Al ingresar al programa el usuario sólo deberá poder capturar el Sku, una vez capturado se deberá validar si existe. En el caso de existir, se deberá mostrar un botón con la opción paraactualizar y al hacer uso de él se deberán poder actualizar los datos Artículo, Marca, Modelo, Departamento, Clase, Familia, Cantidad, Stock y Descontinuado.

Consulta:
Al ingresar al programa el usuario sólo deberá poder capturar el Sku, una vez capturado se deberá validar si existe. En el caso de existir, se deberán mostrar los datos de Artículo, Marca, Modelo, Departamento, Clase, Familia, Fecha de Alta, Stock, Cantidad, Descontinuado, Fecha Baja.

Restricciones:
*La cantidad no debe ser mayor al stock.
*El departamento se deberá llenar al ingresar un Sku válido.
*La clase solo se podrá seleccionar si se encuentra un departamento seleccionado además solo deberá mostrar las clases pertenecientes a ese departamento.
*La familia solo se podrá seleccionar si se encuentra una clase seleccionada además solo deberá mostrar las familias pertenecientes a ese departamento-clase.
*La fecha baja se deberá actualizar al día actual cuando la clave de descontinuado se actualice a encendido.
*Toda alta, baja, cambio o consulta deberá realizarse a través de procedimientos almacenados.
*Todos los objetos de bases de datos deberán guardarse en un archivo para su revisión ya sea de manera individual o conjunta.



