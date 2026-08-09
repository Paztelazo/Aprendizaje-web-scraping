# 10. Recolectar datos de un sitio web

Un crawler no solamente puede recorrer páginas.

También puede **extraer información de cada página que visita**.

Por ejemplo:

- título de la página;
- primer párrafo;
- enlaces internos;
- enlace de edición;
- fechas;
- autor;
- categorías;
- cualquier otro dato presente en el HTML.

En este ejemplo se usa Wikipedia.

---

# Código

```python
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re


pages = set()


def getLinks(pageUrl):
    global pages

    url = "https://en.wikipedia.org" + pageUrl

    request = Request(
        url,
        headers={
            "User-Agent": "GersonLearningCrawler/1.0"
        }
    )

    html = urlopen(request)

    bsObj = BeautifulSoup(
        html,
        "html.parser"
    )

    try:
        # Obtiene el título de la página.
        print(
            bsObj.h1.get_text()
        )

        # Obtiene el primer párrafo del contenido.
        print(
            bsObj.find(
                id="mw-content-text"
            ).find_all("p")[0]
        )

        # Obtiene el enlace de edición de la página.
        print(
            bsObj.find(
                id="ca-edit"
            ).find(
                "span"
            ).find(
                "a"
            ).attrs["href"]
        )

    except (AttributeError, IndexError):
        print(
            "Esta página le falta algo, "
            "continuando con la siguiente página..."
        )

    # Busca enlaces internos de Wikipedia.
    for link in bsObj.find_all(
        "a",
        href=re.compile(r"^/wiki/")
    ):

        if "href" in link.attrs:

            # Comprueba si la ruta todavía
            # no fue encontrada.
            if link.attrs["href"] not in pages:

                # Guarda la nueva ruta.
                newPage = link.attrs["href"]

                print(newPage)

                # Agrega la ruta al set.
                pages.add(newPage)

                # Visita la nueva página.
                getLinks(newPage)


# Comienza desde la página principal.
getLinks("")
```

---

# Objetivo del código

Antes nuestro crawler principalmente hacía esto:

```text
entrar a una página
        ↓
buscar enlaces
        ↓
entrar a otra página
```

Ahora hace algo adicional:

```text
entrar a una página
        ↓
extraer información
        ↓
buscar enlaces
        ↓
entrar a otra página
        ↓
extraer información
        ↓
repetir
```

Es decir, combina:

```text
Web Crawler
+
Web Scraper
```

El crawler descubre páginas.

El scraper extrae datos de esas páginas.

---

# `pages = set()`

```python
pages = set()
```

Crea un conjunto vacío.

Se utiliza para guardar las rutas que ya fueron encontradas.

Ejemplo:

```python
pages = {
    "/wiki/Python",
    "/wiki/Java",
    "/wiki/Linux"
}
```

Un `set` no permite duplicados.

Esto evita procesar constantemente la misma página.

---

# `getLinks(pageUrl)`

```python
def getLinks(pageUrl):
```

La función recibe una ruta.

Por ejemplo:

```text
/wiki/Python
```

Dentro de la función se convierte en:

```text
https://en.wikipedia.org/wiki/Python
```

---

# `global pages`

```python
global pages
```

Indica que la función utilizará la variable:

```python
pages
```

que fue creada fuera de la función.

Esto permite hacer:

```python
pages.add(newPage)
```

y conservar las páginas encontradas entre diferentes llamadas de `getLinks()`.

---

# Crear la URL

```python
url = "https://en.wikipedia.org" + pageUrl
```

Si:

```python
pageUrl = "/wiki/Python"
```

entonces:

```python
url
```

será:

```text
https://en.wikipedia.org/wiki/Python
```

---

# Crear la solicitud

```python
request = Request(
    url,
    headers={
        "User-Agent": "GersonLearningCrawler/1.0"
    }
)
```

`Request` prepara la solicitud HTTP.

El `User-Agent` identifica al programa que realiza la petición.

---

# Descargar el HTML

```python
html = urlopen(request)
```

Envía la solicitud y recibe el HTML de la página.

---

# Analizar el HTML

```python
bsObj = BeautifulSoup(
    html,
    "html.parser"
)
```

BeautifulSoup convierte el HTML en un objeto que podemos buscar y recorrer.

---

# Recolectar información

La extracción de información se encuentra dentro de:

```python
try:
```

porque no todas las páginas de Wikipedia tienen exactamente la misma estructura.

---

## Obtener el título

```python
print(
    bsObj.h1.get_text()
)
```

Busca la etiqueta:

```html
<h1>
```

y extrae su texto.

Por ejemplo:

```html
<h1>Python</h1>
```

Resultado:

```text
Python
```

---

# Obtener el primer párrafo

```python
print(
    bsObj.find(
        id="mw-content-text"
    ).find_all("p")[0]
)
```

Primero busca:

```python
bsObj.find(
    id="mw-content-text"
)
```

Es decir, el elemento HTML cuyo `id` sea:

```text
mw-content-text
```

Después:

```python
.find_all("p")
```

busca todos los párrafos `<p>` dentro de ese contenido.

Podría devolver:

```python
[
    <p>Primer párrafo</p>,
    <p>Segundo párrafo</p>,
    <p>Tercer párrafo</p>
]
```

Finalmente:

```python
[0]
```

selecciona el primer párrafo:

```html
<p>Primer párrafo</p>
```

---

# Obtener el enlace de edición

```python
print(
    bsObj.find(
        id="ca-edit"
    ).find(
        "span"
    ).find(
        "a"
    ).attrs["href"]
)
```

Se realizan varias búsquedas consecutivas.

Primero:

```python
bsObj.find(id="ca-edit")
```

busca el elemento relacionado con la opción de editar.

Después:

```python
.find("span")
```

busca un `<span>` dentro.

Luego:

```python
.find("a")
```

busca el enlace `<a>`.

Finalmente:

```python
.attrs["href"]
```

extrae su dirección.

Ejemplo:

```html
<a href="/w/index.php?title=Python&action=edit">
    Edit
</a>
```

Resultado:

```text
/w/index.php?title=Python&action=edit
```

---

# ¿Por qué usamos `try`?

```python
try:
```

Porque no todas las páginas tienen:

```text
<h1>
mw-content-text
<p>
ca-edit
```

Por ejemplo, algunas páginas especiales pueden no tener enlace de edición.

Entonces alguna búsqueda puede devolver:

```python
None
```

o una lista vacía:

```python
[]
```

---

# `except`

```python
except (AttributeError, IndexError):
```

Captura dos errores comunes.

## `AttributeError`

Puede ocurrir cuando:

```python
bsObj.find(id="ca-edit")
```

devuelve:

```python
None
```

y después intentamos hacer:

```python
None.find(...)
```

---

## `IndexError`

Puede ocurrir con:

```python
find_all("p")[0]
```

si no existe ningún párrafo.

Por ejemplo:

```python
parrafos = []

parrafos[0]
```

produce:

```text
IndexError
```

Por eso capturamos ambos errores:

```python
except (AttributeError, IndexError):
```

---

# Buscar enlaces internos

```python
for link in bsObj.find_all(
    "a",
    href=re.compile(r"^/wiki/")
):
```

Busca todas las etiquetas `<a>` cuyo `href` comience con:

```text
/wiki/
```

Ejemplo:

```html
<a href="/wiki/Python">Python</a>
```

---

# Comprobar `href`

```python
if "href" in link.attrs:
```

Comprueba que la etiqueta tenga un atributo:

```text
href
```

En este caso es una comprobación redundante porque `find_all()` ya está buscando enlaces mediante `href`.

Pero se puede mantener para entender claramente qué se está comprobando.

---

# Evitar páginas repetidas

```python
if link.attrs["href"] not in pages:
```

Pregunta:

> ¿Esta ruta todavía no está guardada en `pages`?

Si no está, continúa.

---

# Guardar la nueva ruta

```python
newPage = link.attrs["href"]
```

Ejemplo:

```python
newPage = "/wiki/Python"
```

---

# Mostrarla

```python
print(newPage)
```

Muestra la ruta encontrada.

---

# Agregarla al set

```python
pages.add(newPage)
```

Guarda la ruta para evitar procesarla nuevamente.

---

# Recursividad

```python
getLinks(newPage)
```

La función se llama a sí misma usando la nueva página.

Por ejemplo:

```text
getLinks("")
        ↓
encuentra /wiki/Python
        ↓
getLinks("/wiki/Python")
        ↓
encuentra /wiki/Programming_language
        ↓
getLinks("/wiki/Programming_language")
        ↓
...
```

Esto es recursividad.

---

# Inicio del crawler

```python
getLinks("")
```

La primera llamada utiliza:

```python
pageUrl = ""
```

Entonces:

```python
url = "https://en.wikipedia.org" + ""
```

Resultado:

```text
https://en.wikipedia.org
```

El crawler comienza desde la página principal de Wikipedia.

---

# Flujo completo

```text
getLinks("")
        ↓
Página principal
        ↓
extrae título
        ↓
extrae primer párrafo
        ↓
intenta extraer enlace de edición
        ↓
busca enlaces /wiki/
        ↓
elige una página todavía no registrada
        ↓
la guarda en pages
        ↓
getLinks(newPage)
        ↓
repite todo
```

---

# Idea principal

Este código ya no solamente descubre páginas.

También intenta **recolectar información específica de cada página visitada**.

```text
Crawler
→ descubre páginas

Scraper
→ obtiene información

Crawler + Scraper
→ recorre páginas y extrae información de cada una
```

La información que se extrae actualmente es:

```text
1. Título
2. Primer párrafo
3. Enlace de edición
```

Pero la misma lógica se puede utilizar para extraer:

```text
fechas
autores
categorías
imágenes
tablas
enlaces
descripciones
otros datos del sitio
```
