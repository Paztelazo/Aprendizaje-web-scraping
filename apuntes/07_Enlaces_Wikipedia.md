# 07. Encontrar enlaces de artículos en Wikipedia

El objetivo es obtener enlaces que lleven a otros artículos de Wikipedia.

## Código

```python
import re
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup


url = "https://en.wikipedia.org/wiki/Kevin_Bacon"

request = Request(
    url,
    headers={
        "User-Agent": "GersonWebScrapingPractice/1.0"
    }
)

html = urlopen(request)
bs = BeautifulSoup(html, "html.parser")

body_content = bs.find("div", {"id": "bodyContent"})

links = body_content.find_all(
    "a",
    href=re.compile(
        r"^(?:https://en\.wikipedia\.org)?/wiki/[^:]+$"
    )
)

for link in links:
    print(link["href"])
```

## ¿Qué hace?

### `Request`

```python
request = Request(url, headers={...})
```

Prepara una solicitud con un `User-Agent`. Esto evita que Wikipedia rechace la solicitud como ocurrió con el error `403 Forbidden`.

### `bodyContent`

```python
body_content = bs.find("div", {"id": "bodyContent"})
```

Busca el bloque principal del artículo:

```html
<div id="bodyContent">
```

### Buscar etiquetas `<a>`

```python
body_content.find_all("a", href=...)
```

Busca etiquetas `<a>` que tengan un atributo `href`.

### Regex

```python
r"^(?:https://en\.wikipedia\.org)?/wiki/[^:]+$"
```

Acepta:

```text
/wiki/Philadelphia
https://en.wikipedia.org/wiki/Philadelphia
```

Rechaza páginas especiales que contienen `:`:

```text
/wiki/File:Imagen.jpg
/wiki/Special:Search
/wiki/Category:Actors
```

## Criterios usados

Los enlaces buscados:

1. Están dentro de `bodyContent`.
2. Son etiquetas `<a>` con `href`.
3. Llevan a rutas de artículos con `/wiki/`.
4. No contienen `:` en la ruta del artículo.

> No se trata de evitar comas. El carácter que se filtra es `:`.
