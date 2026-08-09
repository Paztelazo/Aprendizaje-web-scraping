# 11. Crawling entre dominios

Hasta ahora los crawlers trabajaban principalmente dentro de un solo sitio web o dominio.

Por ejemplo:

```text
wikipedia.org
    ↓
/wiki/Python
    ↓
/wiki/Linux
    ↓
/wiki/Programming
```

Ahora la idea cambia:

> Ya no se ignoran los links externos. También se siguen.

El crawler puede pasar de un dominio a otro y construir un mapa de conexiones entre sitios web.

Ejemplo:

```text
oreilly.com
    ↓
youtube.com
    ↓
developers.google.com
    ↓
stackoverflow.com
    ↓
otro dominio
```

---

# Antes de construir un crawler entre dominios

Conviene preguntarse:

1. ¿Qué datos quiero recopilar?
2. ¿Puedo obtenerlos scrapeando sitios previamente definidos o necesito descubrir sitios que todavía no conozco?
3. Cuando llegue a un sitio, ¿debo pasar inmediatamente a otro dominio o recorrer primero parte del sitio actual?
4. ¿Hay páginas o dominios que no quiero scrapear?
5. ¿Me interesan páginas en otros idiomas?
6. ¿Cómo evitaré generar demasiadas solicitudes?
7. ¿Cómo manejaré posibles restricciones, términos de uso o bloqueos del sitio?

Es recomendable diseñar primero un diagrama del comportamiento esperado.

```text
Página actual
      ↓
buscar links externos
      ↓
¿hay externos?
   ↙       ↘
  sí        no
  ↓          ↓
elegir     buscar links
uno        internos
  ↓          ↓
visitar    elegir uno
otro         ↓
dominio    seguir buscando
```

---

# Separar el crawler en funciones

Es buena práctica separar el código en funciones pequeñas.

En este ejemplo tenemos:

```text
getInternalLinks()
→ encuentra links del mismo dominio

getExternalLinks()
→ encuentra links de otros dominios

getRandomExternalLink()
→ consigue un link externo aleatorio

followExternalOnly()
→ entra al link externo y repite el proceso
```

Esto facilita modificar el crawler después.

Por ejemplo, podríamos cambiar:

```text
seguir un link externo al azar
```

por:

```text
guardar todos los links externos encontrados
```

sin tener que rehacer todo el programa.

---

# Código

```python
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from bs4 import BeautifulSoup

import re
import random


# Este set venía del crawler anterior.
# En este ejemplo actualmente no se utiliza.
pages = set()


# ---------------------------------------------------------
# OBTENER LINKS INTERNOS
# ---------------------------------------------------------

def getInternalLinks(bs, includeUrl):

    # Se queda únicamente con:
    # protocolo + dominio
    #
    # Ejemplo:
    # https://www.ejemplo.com/productos/celulares
    #
    # scheme -> https
    # netloc -> www.ejemplo.com
    #
    # Resultado:
    # https://www.ejemplo.com

    includeUrl = "{}://{}".format(
        urlparse(includeUrl).scheme,
        urlparse(includeUrl).netloc
    )

    internalLinks = []

    # Busca etiquetas <a> cuyo href:
    #
    # 1. Empiece con /
    #    Ejemplo: /productos
    #
    # 2. O contenga el dominio actual.
    #    Ejemplo: https://www.ejemplo.com/productos

    for link in bs.find_all(
        "a",
        href=re.compile(
            r"^(/|.*" + re.escape(includeUrl) + r")"
        )
    ):

        # Extrae el valor del atributo href.
        href = link.attrs["href"]

        # Evita guardar duplicados.
        if href not in internalLinks:

            # Si empieza con /, es una ruta relativa.
            #
            # /productos
            # ↓
            # https://www.ejemplo.com/productos

            if href.startswith("/"):
                internalLinks.append(
                    includeUrl + href
                )

            # Si ya viene como URL completa,
            # se agrega tal como está.
            else:
                internalLinks.append(href)

    return internalLinks


# ---------------------------------------------------------
# OBTENER LINKS EXTERNOS
# ---------------------------------------------------------

def getExternalLinks(bs, excludeUrl):

    externalLinks = []

    # Busca etiquetas <a> cuyo href:
    #
    # 1. Empiece con http o www
    # 2. NO contenga el dominio actual.
    #
    # Si excludeUrl es:
    # en.wikipedia.org
    #
    # acepta:
    # https://google.com
    # https://github.com
    #
    # pero intenta excluir:
    # https://en.wikipedia.org/wiki/Python

    for link in bs.find_all(
        "a",
        href=re.compile(
            r"^(http|www)((?!" +
            re.escape(excludeUrl) +
            r").)*$"
        )
    ):

        href = link.attrs["href"]

        # Si aparece así:
        # www.ejemplo.com
        #
        # se convierte en:
        # https://www.ejemplo.com

        if href.startswith("www."):
            href = "https://" + href

        # Evita duplicados.
        if href not in externalLinks:
            externalLinks.append(href)

    return externalLinks


# ---------------------------------------------------------
# BUSCAR UN LINK EXTERNO ALEATORIO
# ---------------------------------------------------------

def getRandomExternalLink(startingPage):

    # startingPage representa la página
    # que se está visitando actualmente.

    request = Request(
        startingPage,
        headers={
            "User-Agent": "GersonLearningCrawler/1.0"
        }
    )

    # Intenta descargar la página.
    try:
        html = urlopen(request)

    except HTTPError as error:
        print(
            "No se pudo abrir:",
            startingPage,
            "- Error HTTP:",
            error.code
        )
        return None

    except URLError as error:
        print(
            "No se pudo conectar a:",
            startingPage,
            "-",
            error.reason
        )
        return None

    # BeautifulSoup analiza el HTML recibido.
    bs = BeautifulSoup(
        html,
        "html.parser"
    )

    # Busca links que pertenezcan a otros dominios.
    #
    # Ejemplo:
    # startingPage:
    # https://en.wikipedia.org/wiki/Python
    #
    # urlparse(startingPage).netloc:
    # en.wikipedia.org

    externalLinks = getExternalLinks(
        bs,
        urlparse(startingPage).netloc
    )

    # -------------------------------------------------
    # CASO 1: NO HAY LINKS EXTERNOS
    # -------------------------------------------------

    if len(externalLinks) == 0:

        print(
            "No external links, "
            "looking around the site for one"
        )

        # Obtiene protocolo + dominio.
        #
        # https://ejemplo.com/blog/articulo
        # ↓
        # https://ejemplo.com

        domain = "{}://{}".format(
            urlparse(startingPage).scheme,
            urlparse(startingPage).netloc
        )

        # Busca links internos.
        internalLinks = getInternalLinks(
            bs,
            domain
        )

        # Si tampoco hay links internos,
        # no hay por dónde continuar.
        if len(internalLinks) == 0:
            return None

        # Elige un link interno al azar
        # y vuelve a buscar desde esa página.
        #
        # Esto es recursividad.
        return getRandomExternalLink(
            random.choice(internalLinks)
        )

    # -------------------------------------------------
    # CASO 2: SÍ HAY LINKS EXTERNOS
    # -------------------------------------------------

    else:

        # Devuelve un link externo al azar.
        return random.choice(
            externalLinks
        )


# ---------------------------------------------------------
# SEGUIR LINKS EXTERNOS
# ---------------------------------------------------------

def followExternalOnly(startingSite):

    # Busca un link externo comenzando
    # desde startingSite.
    externalLink = getRandomExternalLink(
        startingSite
    )

    # Si no encontró ningún link,
    # termina el crawler.
    if externalLink is None:
        print("No se encontraron más enlaces.")
        return

    # Muestra el link encontrado.
    print(
        "Random external link is: {}".format(
            externalLink
        )
    )

    # Entra al nuevo sitio y repite.
    # También es recursividad.
    followExternalOnly(externalLink)


# ---------------------------------------------------------
# INICIO DEL CRAWLER
# ---------------------------------------------------------

followExternalOnly(
    "http://oreilly.com"
)
```

---

# `getInternalLinks()`

Su trabajo es encontrar enlaces que pertenezcan al mismo dominio.

Si estamos en:

```text
https://www.ejemplo.com/productos
```

estos son internos:

```text
/contacto
/productos/nuevo
https://www.ejemplo.com/servicios
```

La función convierte rutas relativas en URLs completas:

```text
/contacto
↓
https://www.ejemplo.com/contacto
```

---

# `getExternalLinks()`

Su trabajo es encontrar enlaces hacia otros dominios.

Si estamos en:

```text
en.wikipedia.org
```

esto no interesa como externo:

```text
https://en.wikipedia.org/wiki/Python
```

En cambio:

```text
https://github.com
```

sí es externo.

---

# `getRandomExternalLink()`

Su objetivo es conseguir un link externo aleatorio.

Primero busca:

```text
Página actual
    ↓
links externos
```

Si encuentra alguno:

```text
externalLinks
    ↓
random.choice()
    ↓
devuelve uno
```

Si no encuentra ninguno:

```text
Página actual
    ↓
no hay externos
    ↓
buscar links internos
    ↓
elegir uno al azar
    ↓
entrar a esa página
    ↓
volver a buscar externos
```

Por eso contiene:

```python
return getRandomExternalLink(
    random.choice(internalLinks)
)
```

La función se llama a sí misma. Eso es **recursividad**.

---

# `followExternalOnly()`

Esta función permite saltar continuamente entre dominios.

Hace:

```text
buscar link externo
        ↓
mostrarlo
        ↓
entrar al nuevo dominio
        ↓
volver a buscar
```

La parte:

```python
followExternalOnly(externalLink)
```

hace que el proceso se repita.

Ejemplo:

```text
oreilly.com
    ↓
youtube.com
    ↓
developers.google.com
    ↓
stackoverflow.com
    ↓
otro sitio
```

---

# Manejo de errores

Al recorrer Internet es normal encontrar sitios que:

- no existen;
- están caídos;
- bloquean crawlers;
- responden con `403 Forbidden`;
- responden con `404 Not Found`;
- tienen problemas de DNS.

Por eso se usa:

```python
try:
    html = urlopen(request)
```

con:

```python
except HTTPError:
```

para errores HTTP como:

```text
403 Forbidden
404 Not Found
```

Y:

```python
except URLError:
```

para problemas de conexión o resolución del dominio.

En vez de terminar con un traceback, la función devuelve:

```python
None
```

---

# Archivos que no son HTML

El crawler también puede encontrar enlaces como:

```text
.pdf
.jpg
.png
.zip
.mp4
```

Por ejemplo:

```text
https://sitio.com/documento.pdf
```

Si llega a un PDF, BeautifulSoup no encuentra una estructura HTML normal con enlaces `<a>`.

Puede ocurrir:

```text
PDF
↓
no hay links externos
↓
no hay links internos
↓
return None
↓
crawler termina
```

Más adelante se puede mejorar el crawler para filtrar esos tipos de archivo antes de visitarlos.

---

# Idea general

Antes:

```text
Crawler de un dominio

Wikipedia
↓
Wikipedia
↓
Wikipedia
```

Ahora:

```text
Crawler entre dominios

O'Reilly
↓
YouTube
↓
Google
↓
Stack Overflow
↓
otro sitio
```

El objetivo es empezar a construir un **mapa de conexiones entre páginas y dominios de Internet**.

---

# Buen hábito: diseñar antes de programar

Antes de escribir un crawler complejo, es útil dibujar su flujo.

```text
               PÁGINA ACTUAL
                     ↓
           buscar links externos
                     ↓
              ¿hay externos?
                /         \
              sí           no
              ↓             ↓
          elegir uno    buscar internos
              ↓             ↓
       visitar dominio   elegir uno
              ↓             ↓
              └──────→ repetir
```

Esto ayuda a identificar:

- qué funciones necesitas;
- qué condiciones pueden aparecer;
- qué datos vas a guardar;
- dónde puede detenerse el crawler;
- qué errores necesitas manejar.

Separar el programa en funciones pequeñas hace que después sea mucho más fácil modificarlo o reutilizarlo.
