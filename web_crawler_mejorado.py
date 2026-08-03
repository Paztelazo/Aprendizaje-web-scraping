from urllib.request import urlopen, Request
from urllib.parse import urljoin, quote
from bs4 import BeautifulSoup
import random
import re


BASE_URL = "https://en.wikipedia.org"


def getLinks(articleUrl):
    # Forma la URL completa del artículo.
    url = urljoin(BASE_URL, articleUrl)
    
    # Convierte caracteres especiales para que puedan usarse en una URL.
    # Por ejemplo:
    # ç se convierte en %C3%A7
    # – se convierte en %E2%80%93
    url = quote(url, safe=":/?#=&%")

    # Agrega un User-Agent para que Wikipedia acepte la solicitud.
    request = Request(
        url,
        headers={
            "User-Agent": "GersonWebScrapingPractice/1.0"
        }
    )

    # Descarga y analiza la página.
    html = urlopen(request)
    bs = BeautifulSoup(html, "html.parser")

    # Busca el contenido principal del artículo.
    bodyContent = bs.find("div", {"id": "bodyContent"})

    articleLinks = []

    # Recorre todos los enlaces encontrados.
    for link in bodyContent.find_all("a", href=True):
        href = link.attrs["href"]

        # Convierte el enlace en una URL completa.
        completeUrl = urljoin(url, href)

        # Elimina el dominio para conservar solo /wiki/Articulo.
        articleUrl = completeUrl.replace(BASE_URL, "", 1)

        # Acepta artículos normales y descarta páginas como
        # File:, Special:, Category:, etc.
        if re.fullmatch(r"/wiki/[^:]+", articleUrl):
            link.attrs["href"] = articleUrl
            articleLinks.append(link)

    return articleLinks


# Empieza obteniendo los enlaces del artículo de Kevin Bacon.
links = getLinks("/wiki/Kevin_Bacon")


while len(links) > 0:
    # Mientras haya enlaces, selecciona uno al azar.

    newArticle = links[
        random.randint(0, len(links) - 1)
    ].attrs["href"]

    # Muestra el artículo seleccionado.
    print(newArticle)

    # Obtiene los enlaces del nuevo artículo
    # y vuelve a comenzar el while.
    links = getLinks(newArticle)