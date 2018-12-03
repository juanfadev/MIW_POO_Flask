# Python Flask Server

Desplegado en: https://miwpooflask.herokuapp.com/

Caracteristicas a tener en cuenta:
* Flask-cors extension añadida
* Añadido servidor gunicorn
* Leer/Escribir JSON
* Manual parse JSON a object
* Negociación de contenido (JSON/text-plain/text-html)
* Script JSON-LD en cabecera de HTML bien formado.

Algunos de los endpoint devuelven JSON o texto plano. Sin embargo, todas las entidades (Ejemplo: https://miwpooflask.herokuapp.com/Places/1) devuelven un JSON o un HTML bien formado con un JSON-LD en la cabecera.

Se valida que el tipo de entidad sea correcta, y sea un JSON válido, sino no se puede escribir. El resto de validación de campos se hace contra el servicio de Google desde el cliente.
