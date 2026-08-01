# Manejo de excepciones en web scraping

Durante el web scraping no podemos asumir que todo funcionará correctamente. Una página puede desaparecer, el servidor puede estar caído o el contenido HTML puede cambiar.

Sin manejo de errores, una sola falla puede detener todo el programa y evitar que el scraper continúe recopilando datos.

## Problemas al abrir una página

La siguiente instrucción intenta conectarse con una página:

```python
html = urlopen(url)
```

Principalmente pueden ocurrir dos tipos de problemas:

1. El servidor responde, pero devuelve un error.
2. No es posible encontrar o contactar el servidor.

## `HTTPError`

Un `HTTPError` ocurre cuando Python logra contactar el servidor, pero este responde con un código de error.

Algunos ejemplos son:

- `404 Not Found`: la página solicitada no existe.
- `403 Forbidden`: el servidor rechaza el acceso.
- `500 Internal Server Error`: el servidor presenta un problema interno.

Ejemplo:

```python
from urllib.request import urlopen
from urllib.error import HTTPError

try:
    html = urlopen("https://ejemplo.com/pagina-inexistente")
except HTTPError as e:
    print("El servidor respondió con un error:")
    print(e)
```

En esta línea:

```python
except HTTPError as e:
```

`HTTPError` indica el tipo de error que queremos capturar y `as e` guarda la información del error en una variable llamada `e`.

El nombre `e` es una convención. También podría escribirse:

```python
except HTTPError as error:
    print(error)
```

## `URLError`

Un `URLError` ocurre cuando Python no puede encontrar o contactar el servidor.

Puede suceder porque:

- el dominio no existe;
- el dominio fue escrito incorrectamente;
- el servidor está caído;
- no existe conexión de red.

```python
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

try:
    html = urlopen("https://dominioquenoexiste.com")
except HTTPError as e:
    print("El servidor respondió con un error:", e)
except URLError as e:
    print("No se pudo encontrar o contactar el servidor:", e)
else:
    print("La página se obtuvo correctamente")
```

## Funcionamiento de `try`, `except` y `else`

```text
Intentar abrir la página
          ↓
¿Ocurrió HTTPError?
 Sí → ejecutar except HTTPError
 No
          ↓
¿Ocurrió URLError?
 Sí → ejecutar except URLError
 No
          ↓
     ejecutar else
```

- `try` contiene el código que puede fallar.
- `except` indica qué hacer cuando ocurre un error determinado.
- `else` se ejecuta únicamente cuando el bloque `try` termina sin errores.

## Cuando una etiqueta no existe

Aunque la página se descargue correctamente, el contenido esperado puede no estar presente.

Imaginemos este producto:

```html
<div class="producto">
    <h2 class="nombre">Laptop ASUS</h2>
    <span class="precio">S/ 3,500</span>
</div>
```

Beautiful Soup puede buscar el precio:

```python
precio = bs.find("span", class_="precio")

print(precio)
print(precio.get_text())
```

Resultado:

```text
<span class="precio">S/ 3,500</span>
S/ 3,500
```

La búsqueda funcionó porque la etiqueta existe.

La variable `precio` contiene un objeto de clase `Tag`, que representa una etiqueta HTML concreta. Por eso puede utilizar el método `.get_text()`.

## `None` y `AttributeError`

Ahora imaginemos que el producto está agotado y no tiene una etiqueta de precio:

```html
<div class="producto">
    <h2 class="nombre">Laptop ASUS</h2>
    <span class="estado">Producto agotado</span>
</div>
```

La búsqueda sigue siendo:

```python
precio = bs.find("span", class_="precio")
```

Como la etiqueta no existe, Beautiful Soup devuelve:

```python
None
```

`None` significa que no se encontró ningún objeto.

El error aparece si intentamos ejecutar:

```python
print(precio.get_text())
```

Como `precio` contiene `None`, Python interpreta algo equivalente a:

```python
None.get_text()
```

Pero `None` no representa una etiqueta y no posee el método `get_text()`. Por eso aparece:

```text
AttributeError: 'NoneType' object has no attribute 'get_text'
```

## Forma segura de comprobar el resultado

Antes de utilizar `.get_text()`, debemos comprobar que la búsqueda encontró una etiqueta:

```python
precio = bs.find("span", class_="precio")

if precio is None:
    print("Precio no disponible")
else:
    print(precio.get_text())
```

## Clase, objeto y `Tag`

Una clase representa el tipo al que pertenece un valor:

```python
nombre = "Pedro"
edad = 67
```

- `"Pedro"` es un objeto de clase `str`.
- `67` es un objeto de clase `int`.

Cuando Beautiful Soup procesa el HTML, convierte sus etiquetas en objetos de Python.

```python
titulo = bs.h1
```

Si encuentra un `<h1>`, `titulo` contiene un objeto de clase `Tag`:

```python
print(type(titulo))
```

Resultado aproximado:

```text
<class 'bs4.element.Tag'>
```

```text
HTML original:
<h1>Curso de Python</h1>
          ↓
Beautiful Soup procesa el HTML
          ↓
titulo contiene un objeto Tag
```

`Tag` es la clase utilizada por Beautiful Soup para representar una etiqueta HTML concreta.

## Lo que aprendí

- Un `HTTPError` ocurre cuando el servidor responde con un error HTTP.
- Un `URLError` ocurre cuando no se puede encontrar o contactar el servidor.
- `try` contiene código que puede fallar.
- `except` permite capturar y manejar un error.
- `as e` guarda la información del error en una variable.
- Beautiful Soup devuelve `None` cuando no encuentra una etiqueta.
- Usar `.get_text()` sobre `None` produce un `AttributeError`.
