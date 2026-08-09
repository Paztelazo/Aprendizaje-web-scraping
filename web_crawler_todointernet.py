from urllib.request import urlopen, Request, HTTPError, URLError
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import random


# Este set venía del crawler anterior.
# En este código actualmente no se está utilizando.
pages = set()


# ---------------------------------------------------------
# OBTENER LINKS INTERNOS
# ---------------------------------------------------------

def getInternalLinks(bs, includeUrl):

    # Se queda solamente con:
    # protocolo + dominio
    #
    #
    # Ejemplo:
    #
    # https://www.ejemplo.com/productos/celulares
    #
    # urlparse(...).scheme  -> https
    # urlparse(...).netloc  -> www.ejemplo.com
    #
    # Resultado:
    #
    # https://www.ejemplo.com

    includeUrl = "{}://{}".format(
        urlparse(includeUrl).scheme,
        urlparse(includeUrl).netloc
    )

    # Lista donde se guardarán los links internos.
    internalLinks = []


    # Busca etiquetas <a> cuyo href:
    #
    # 1. Empiece con /
    #
    #    Ejemplo:
    #    /productos
    #
    # 2. O contenga el dominio actual.
    #
    #    Ejemplo:
    #    https://www.ejemplo.com/productos

    for link in bs.find_all(
        "a",
        href=re.compile(
            r"^(/|.*" + re.escape(includeUrl) + r")"
        )
    ):

        # Extrae solamente el valor del href.
        #
        # Ejemplo:
        #
        # <a href="/productos">Productos</a>
        #
        # href será:
        #
        # /productos

        href = link.attrs["href"]


        # Evita guardar el mismo link más de una vez.
        if href not in internalLinks:


            # Si empieza con /, es una ruta relativa.
            #
            # Ejemplo:
            #
            # /productos
            #
            # Se le agrega el dominio:
            #
            # https://www.ejemplo.com/productos

            if href.startswith("/"):

                internalLinks.append(
                    includeUrl + href
                )


            # Si ya viene como URL completa,
            # se agrega tal como está.
            #
            # Ejemplo:
            #
            # https://www.ejemplo.com/productos

            else:
                internalLinks.append(href)


    # Devuelve todos los links internos encontrados.
    return internalLinks



# ---------------------------------------------------------
# OBTENER LINKS EXTERNOS
# ---------------------------------------------------------

def getExternalLinks(bs, excludeUrl):

    # Lista donde se guardarán los links externos.
    externalLinks = []


    # Busca etiquetas <a> cuyo href:
    #
    # 1. Empiece con http o www
    #
    # 2. NO contenga el dominio actual.
    #
    # Ejemplo:
    #
    # Si excludeUrl es:
    #
    # en.wikipedia.org
    #
    # acepta:
    #
    # https://google.com
    # https://github.com
    #
    # pero intenta excluir:
    #
    # https://en.wikipedia.org/wiki/Python

    for link in bs.find_all(
        "a",
        href=re.compile(
            r"^(http|www)((?!" +
            re.escape(excludeUrl) +
            r").)*$"
        )
    ):

        # Extrae el href.
        href = link.attrs["href"]


        # Si el link viene así:
        #
        # www.ejemplo.com
        #
        # le agrega:
        #
        # https://
        #
        # Resultado:
        #
        # https://www.ejemplo.com

        if href.startswith("www."):
            href = "https://" + href


        # Evita duplicados.
        if href not in externalLinks:
            externalLinks.append(href)


    # Devuelve los links externos encontrados.
    return externalLinks



# ---------------------------------------------------------
# BUSCAR UN LINK EXTERNO ALEATORIO
# ---------------------------------------------------------

def getRandomExternalLink(startingPage):

    # Prepara la solicitud HTTP.
    #
    # startingPage es la página que estamos
    # visitando actualmente.

    request = Request(
        startingPage,
        headers={
            "User-Agent": "GersonLearningCrawler/1.0"
        }
    )


    # Descarga el HTML de la página.
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


    # BeautifulSoup analiza el HTML.
    bs = BeautifulSoup(
        html,
        "html.parser"
    )


    # Busca los links externos de la página.
    #
    # urlparse(startingPage).netloc
    # devuelve solamente el dominio.
    #
    # Ejemplo:
    #
    # startingPage:
    # https://en.wikipedia.org/wiki/Python
    #
    # netloc:
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


        # Obtiene solamente:
        #
        # protocolo + dominio
        #
        # Ejemplo:
        #
        # https://ejemplo.com/blog/articulo
        #
        # se convierte en:
        #
        # https://ejemplo.com

        domain = "{}://{}".format(
            urlparse(startingPage).scheme,
            urlparse(startingPage).netloc
        )


        # Como no encontramos links externos,
        # buscamos links internos.

        internalLinks = getInternalLinks(
            bs,
            domain
        )


        # Si tampoco encontramos links internos,
        # no hay ninguna página por donde continuar.

        if len(internalLinks) == 0:
            return None


        # Escoge un link interno al azar.
        #
        # Después vuelve a ejecutar esta misma función
        # desde esa nueva página.
        #
        # Esto es recursividad.

        return getRandomExternalLink(
            random.choice(internalLinks)
        )


    # -------------------------------------------------
    # CASO 2: SÍ HAY LINKS EXTERNOS
    # -------------------------------------------------

    else:

        # Devuelve uno de los links externos
        # de manera aleatoria.

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


    # Si no se encontró ningún link,
    # termina el crawler.

    if externalLink is None:
        print("No se encontraron más enlaces.")
        return


    # Muestra el link externo encontrado.

    print(
        "Random external link is: {}".format(
            externalLink
        )
    )


    # Entra al nuevo sitio y vuelve
    # a ejecutar la misma función.
    #
    # Esto también es recursividad.

    followExternalOnly(externalLink)



# ---------------------------------------------------------
# INICIO DEL CRAWLER
# ---------------------------------------------------------

followExternalOnly(
    "http://oreilly.com"
)