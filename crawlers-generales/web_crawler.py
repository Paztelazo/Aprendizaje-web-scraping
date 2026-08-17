import re
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/Kevin_Bacon"

request = Request(
    url,
    headers={
        "User-Agent": "GersonWebScrapingPractice/1.0"
    }
)
#request está configurado para hacer la solicitud HTTP a la URL de Wikipedia con un encabezado de agente de usuario personalizado.
#asi se evita que el servidor bloquee la solicitud por parecer un bot.

html = urlopen(request)
bs = BeautifulSoup(html, "html.parser")

body_content = bs.find("div", {"id": "bodyContent"})

links = body_content.find_all(
    "a",
    href=re.compile(
        r"^(?:https://en\.wikipedia\.org)?/wiki/[^:]+$"
        #este regex busca enlaces que comiencen con "/wiki/" y no contengan dos puntos (:) después de "/wiki/", 
        # lo que indica que son enlaces a artículos de Wikipedia y no a otras páginas como categorías o archivos.
    )
)
#se llego a cambiar el regex porque el original no estaba funcionando correctamente,
# ya que no estaba considerando los enlaces que comienzan con "https://en.wikipedia.org/wiki/".
for link in links:
    print(link["href"])