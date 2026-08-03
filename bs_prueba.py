from urllib.request import urlopen
from bs4 import BeautifulSoup

http = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
bs = BeautifulSoup(http.read(), "html.parser")
# Con este objeto, puedes encontrar todos los elementos de la página web que tengan un tag específico.
# Por ejemplo, para encontrar todos los elementos con el tag "span", puedes usar el método findAll() de BeautifulSoup

nameList = bs.find_all("span", {"class": "green"})
for name in nameList:
    print(name.get_text())

#Te devolverá iterando todos los elementos con el tag "span" y la clase "green" en la página web, 
# y luego imprimirá el texto contenido en cada uno de ellos.


