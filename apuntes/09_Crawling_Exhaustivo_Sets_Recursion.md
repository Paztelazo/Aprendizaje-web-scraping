# 09. Crawling exhaustivo, sets y recursividad

Un **crawler exhaustivo** intenta recorrer gran parte o todo un sitio web siguiendo sus enlaces internos.

Puede ser útil cuando:

- Quieres obtener un mapa completo del sitio.
- No tienes acceso a un sitemap.
- Necesitas descubrir todas las páginas internas.
- Quieres recopilar artículos, títulos, fechas, blogs u otro contenido para crear un buscador o prototipo.

---

## Cómo funciona un crawl exhaustivo

Normalmente se empieza desde una página principal, por ejemplo:

```text
https://ejemplo.com
```

Luego:

1. Se buscan sus enlaces internos.
2. Se visitan esos enlaces.
3. En cada nueva página se vuelven a buscar enlaces.
4. Se repite el proceso.

Ejemplo:

```text
Inicio
├── Productos
│   ├── Producto A
│   └── Producto B
├── Nosotros
└── Contacto
```

El problema es que la cantidad de páginas puede crecer muy rápido.

Si cada página tuviera 10 enlaces internos y el sitio tuviera 5 niveles:

```text
10^5 = 100000
```

Además, muchos enlaces pueden repetirse.

Por ejemplo:

```text
/inicio
/productos
/contacto
/inicio
/inicio
```

Por eso es importante evitar visitar la misma página varias veces.

---

# Evitar páginas repetidas con `set`

Un `set` es una colección que guarda valores **únicos**.

```python
enlaces = {
    "/inicio",
    "/productos",
    "/contacto",
    "/inicio"
}

print(enlaces)
```

Resultado aproximado:

```python
{
    "/inicio",
    "/productos",
    "/contacto"
}
```

Aunque `"/inicio"` aparezca dos veces, el `set` solo lo guarda una vez.

---

## Diferencia con una lista

Una lista sí permite elementos duplicados:

```python
enlaces = [
    "/inicio",
    "/productos",
    "/contacto",
    "/inicio"
]
```

Aquí `"/inicio"` aparece dos veces.

Por eso para un crawler se puede usar:

```python
paginas_visitadas = set()
```

Antes de visitar una URL:

```python
if url not in paginas_visitadas:
    paginas_visitadas.add(url)
    visitar_pagina(url)
```

La lógica es:

```text
¿Ya visité esta página?
        ↓
      NO
        ↓
guardarla en el set
        ↓
visitarla
```

Si ya existe en el set, no se vuelve a procesar.

---

# Normalizar URLs

Un mismo recurso puede aparecer escrito de diferentes formas:

```text
https://ejemplo.com/productos
https://ejemplo.com/productos/
https://ejemplo.com/productos#precios
/productos
```

Para una persona pueden representar prácticamente la misma página.

Pero Python los considera strings diferentes.

Por eso conviene **normalizar los enlaces** antes de guardarlos.

---

## `urljoin()`

```python
from urllib.parse import urljoin

base = "https://ejemplo.com"

url = urljoin(base, "/productos")

print(url)
```

Resultado:

```text
https://ejemplo.com/productos
```

`urljoin()` permite convertir enlaces relativos en URLs completas.

---

# Recursividad

Una función recursiva es una función que se llama a sí misma.

Ejemplo:

```python
def visitar_pagina(url):
    enlaces = obtener_enlaces(url)

    for enlace in enlaces:
        visitar_pagina(enlace)
```

La función:

1. Visita una página.
2. Obtiene enlaces.
3. Llama nuevamente a la misma función con cada enlace.

Esto permite recorrer páginas conectadas.

---

## Advertencia sobre recursión

Python tiene un límite de recursión.

Por defecto suele estar alrededor de:

```text
1000 llamadas
```

Si una función recursiva se llama demasiadas veces sin terminar, puede producir:

```text
RecursionError
```

---

# Crawler recursivo de Wikipedia

```python
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re


# Crea un conjunto vacío para guardar las páginas
# que ya fueron encontradas.
pages = set()


def getLinks(pageUrl):
    # Indica que queremos usar el set `pages`
    # creado fuera de la función.
    global pages

    # Si pageUrl es "/wiki/Python",
    # la URL final será:
    # https://en.wikipedia.org/wiki/Python
    url = "https://en.wikipedia.org" + pageUrl

    request = Request(
        url,
        headers={
            "User-Agent": "GersonLearningCrawler/1.0"
        }
    )

    html = urlopen(request)

    # Convierte el HTML descargado en un objeto
    # que BeautifulSoup puede analizar.
    bsObj = BeautifulSoup(html, "html.parser")

    # Busca todas las etiquetas <a> cuyo href
    # comience con /wiki/.
    for link in bsObj.find_all(
        "a",
        href=re.compile(r"^/wiki/")
    ):
        # Obtiene la ruta guardada en href.
        newPage = link.attrs["href"]

        # Solo continúa si la página todavía
        # no fue encontrada.
        if newPage not in pages:
            print(newPage)

            # Guarda la ruta para no procesarla
            # nuevamente.
            pages.add(newPage)

            # La función se llama a sí misma
            # con la nueva página.
            getLinks(newPage)


# Inicia el crawler.
# Como pageUrl es una cadena vacía,
# la primera URL será:
# https://en.wikipedia.org
getLinks("")
```

---

# Flujo del crawler

Supongamos:

```text
Página A
├── Página B
└── Página C
```

El crawler hace:

```text
getLinks(A)
    ↓
encuentra B
    ↓
guarda B en pages
    ↓
getLinks(B)
    ↓
encuentra nuevas páginas
    ↓
continúa recursivamente
```

El set:

```python
pages
```

evita que una página ya encontrada vuelva a procesarse.

---

# Idea principal

Un crawler exhaustivo necesita principalmente:

```text
1. Encontrar enlaces internos
2. Normalizar las URLs
3. Guardar páginas visitadas
4. Evitar duplicados con set()
5. Repetir el proceso
6. Controlar la recursión
```

La combinación de:

```python
set()
```

y:

```python
getLinks(newPage)
```

permite recorrer muchas páginas sin visitar constantemente los mismos enlaces.
