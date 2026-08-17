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
    bsObj = BeautifulSoup(html, "html.parser")

    try:
        print(bsObj.h1.get_text()) #h1 es el titulo de la pagina, que se encuentra en la etiqueta <h1>
        print(bsObj.find(id="mw-content-text").find_all("p")[0]) #mw-content-text es el id del div 
        #que contiene el contenido de la pagina, y find_all("p")[0] devuelve el primer parrafo de la pagina.
        print(bsObj.find(id="ca-edit").find("span").find("a").attrs['href']) #ca-edit es el id del div que contiene el enlace 
        #para editar la pagina, y find("span").find("a").attrs['href'] devuelve el href del enlace.
    except AttributeError:
        print("Esta pagina le falta algo, continuando con la siguiente pagina...")



    for link in bsObj.find_all("a", href=re.compile(r"^/wiki/")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                # Agrega la ruta al conjunto de páginas visitadas.
                newPage = link.attrs['href']
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)
getLinks("") #Llamada inicial a la función getLinks con la página principal de Wikipedia.
