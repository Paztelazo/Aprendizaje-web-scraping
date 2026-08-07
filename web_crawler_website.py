# Crawler recursivo de Wikipedia

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re


# Crea un conjunto vacío para guardar las rutas que ya fueron encontradas.
#
# Un set almacena elementos únicos, por lo que una misma ruta
# no puede aparecer dos veces.
#
# Ejemplo:
# nombres = {"Juan", "Pedro", "Juan"}
# El resultado será: {"Juan", "Pedro"}
#
# En este crawler sirve para evitar visitar una página repetidamente.
pages = set()


def getLinks(pageUrl):
    """
    Recibe la ruta de una página de Wikipedia, descarga su HTML,
    busca enlaces internos y visita recursivamente los enlaces nuevos.

    Ejemplo de pageUrl:
    /wiki/Python
    """

    # Indica que pages se refiere a la variable creada fuera de la función.
    global pages

    # Une el dominio de Wikipedia con la ruta recibida.
    #
    # Si pageUrl es "/wiki/Python", la dirección final será:
    # http://en.wikipedia.org/wiki/Python
    url = "https://en.wikipedia.org" + pageUrl

    request = Request(
        url,
        headers={
            "User-Agent": "GersonLearningCrawler/1.0"
        }
    )

    html = urlopen(request)

    # Convierte el HTML descargado en un objeto que BeautifulSoup
    # puede analizar y recorrer.
    bsObj = BeautifulSoup(html, "html.parser")

    # Busca todas las etiquetas <a> cuyo atributo href
    # comience con "/wiki/".
    #
    # Ejemplo encontrado:
    # <a href="/wiki/Python">Python</a>
    for link in bsObj.find_all("a", href=re.compile(r"^/wiki/")):
        #Se han relajado los estandares de Wikipedia, 
        # y ahora hay enlaces que no son de artículos, sino de otras páginas internas.
        #Por ejemplo, comas, puntos, dos puntos, etc. Enlaces no relacionados con artículos de Wikipedia, pero si imagenes u otros.

        # Comprueba que la etiqueta tenga el atributo href.
        #
        # Esta comprobación es redundante en este caso,
        # porque find_all ya está buscando enlaces que tengan href.
        if "href" in link.attrs:

            # Obtiene la ruta guardada en el atributo href.
            #
            # Ejemplo:
            # newPage = "/wiki/Python"
            newPage = link.attrs["href"]

            # Solo continúa si la página todavía no fue encontrada.
            if newPage not in pages:

                # Muestra en pantalla la nueva ruta encontrada.
                print(newPage)

                # Guarda la ruta en el set para no procesarla nuevamente.
                pages.add(newPage)

                # La función se llama a sí misma con la nueva página.
                #
                # Esto es recursividad:
                # entra a la nueva página, busca sus enlaces y repite
                # el mismo proceso.
                getLinks(newPage)


# Inicia el crawler.
#
# Como pageUrl es una cadena vacía, la primera dirección será:
# http://en.wikipedia.org
getLinks("")