# 08. Crawler de Wikipedia con `getLinks()`

Este crawler:

1. Empieza en Kevin Bacon.
2. Obtiene los enlaces de ese artículo.
3. Elige uno al azar.
4. Entra al nuevo artículo.
5. Repite el proceso.

## Código

```python
from urllib.request import Request, urlopen
from urllib.parse import quote, urljoin

from bs4 import BeautifulSoup

import random
import re


BASE_URL = "https://en.wikipedia.org"


def getLinks(articleUrl):
    # Convierte /wiki/Articulo en una URL completa.
    url = urljoin(BASE_URL, articleUrl)

    # Codifica caracteres especiales como ç, ñ o –.
    url = quote(url, safe=":/?#=&%")

    request = Request(
        url,
        headers={
            "User-Agent": "GersonWebScrapingPractice/1.0"
        }
    )

    html = urlopen(request)
    bs = BeautifulSoup(html, "html.parser")

    bodyContent = bs.find("div", {"id": "bodyContent"})

    articleLinks = []

    for link in bodyContent.find_all("a", href=True):
        href = link.attrs["href"]

        # Convierte el href encontrado en una URL completa.
        completeUrl = urljoin(url, href)

        # Conserva solo la ruta /wiki/Articulo.
        articleUrl = completeUrl.replace(BASE_URL, "", 1)

        # Acepta artículos normales y descarta File:, Special:, etc.
        if re.fullmatch(r"/wiki/[^:]+", articleUrl):
            link.attrs["href"] = articleUrl
            articleLinks.append(link)

    return articleLinks


links = getLinks("/wiki/Kevin_Bacon")


while len(links) > 0:
    newArticle = links[
        random.randint(0, len(links) - 1)
    ].attrs["href"]

    print(newArticle)

    links = getLinks(newArticle)
```

## Variables importantes

| Variable | Representa |
|---|---|
| `BASE_URL` | Dominio fijo de Wikipedia |
| `articleUrl` | Ruta de un artículo, como `/wiki/Footloose` |
| `url` | URL completa de la página actual |
| `link` | Una etiqueta `<a>` completa |
| `href` | El valor del atributo `href` |
| `completeUrl` | URL completa del enlace encontrado |
| `articleLinks` | Lista de enlaces válidos encontrados |
| `links` | Lista devuelta por `getLinks()` |
| `newArticle` | Próximo artículo elegido aleatoriamente |

## Transformación de un enlace

Etiqueta encontrada:

```html
<a href="./Footloose">Footloose</a>
```

La variable `href` contiene:

```text
./Footloose
```

Después de `urljoin()`:

```text
https://en.wikipedia.org/wiki/Footloose
```

Después de eliminar `BASE_URL`:

```text
/wiki/Footloose
```

## Función `getLinks()`

```python
def getLinks(articleUrl):
```

Recibe una ruta:

```text
/wiki/Kevin_Bacon
```

y devuelve una lista de etiquetas `<a>` que enlazan a otros artículos.

## Bucle `while`

```python
while len(links) > 0:
```

Mientras existan enlaces:

1. Se genera una posición aleatoria.
2. Se obtiene la etiqueta guardada en esa posición.
3. Se extrae su `href`.
4. Se imprime el nuevo artículo.
5. Se reemplaza `links` con los enlaces de la nueva página.

La línea:

```python
links = getLinks(newArticle)
```

es la que permite avanzar:

```text
Kevin Bacon → Footloose → otro artículo → otro artículo
```

## `quote()`

```python
url = quote(url, safe=":/?#=&%")
```

Codifica caracteres que no pueden enviarse directamente en una URL.

Ejemplo:

```text
/wiki/François_de_Roubaix
```

se convierte en:

```text
/wiki/Fran%C3%A7ois_de_Roubaix
```
