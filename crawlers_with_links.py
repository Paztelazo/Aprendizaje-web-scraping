"""Qué enlaces seguir y cuáles no seguir.

    Este módulo explica el patrón targetPattern que se puede usar
    para filtrar URLs mediante expresiones regulares.

    Ejemplo:
        targetPattern = r"^/articles/"
        - /about                    -> no
        - /contact                  -> no
        - /login                    -> no
        - /articles/python          -> sí
        - /articles/security        -> sí
        - /articles/linux           -> sí

“Yo quiero darle a mi programa un sitio web concreto, recorrer su página principal, 
encontrar dentro de ella únicamente los enlaces que tienen la estructura que me interesa,
evitar visitar dos veces el mismo enlace, entrar a cada página válida,
extraer de ella el título y el contenido, y finalmente mostrar esa información.”
"""

import re
import requests
from bs4 import BeautifulSoup


class Website:
    def __init__(self, name, baseUrl, startUrl, targetPattern, absoluteUrl, titleTag, bodyTag):
        self.name = name
        self.baseUrl = baseUrl
        self.startUrl = startUrl
        self.targetPattern = targetPattern
        self.absoluteUrl=absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag
        
class Content:
    def __init__(self, url, title, body): 
        self.url = url
        self.title = title
        self.body = body

    def print(self):
        print("URL: {}".format(self.url))
        print("TITLE: {}".format(self.title))
        print("BODY:\n{}".format(self.body))

class Crawler:
    def __init__(self, site): #Ahora usa init para inicializar el objeto Crawler con un sitio web específico.
        self.site = site
        self.visited = [] #ya no visites lo mismo
        
    def getPage(self, url): 
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None        
        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join([elem.get_text() for
                elem in selectedElems])
        return ''   
    
    def parse(self, url):
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, self.site.titleTag)
            body = self.safeGet(bs, self.site.bodyTag)
            if title != '' and body != '':
                content = Content(url, title, body)
                content.print()    

    def crawl(self): #como descubro los enlaces que quiero seguir y cuáles no, para eso uso targetPattern
        """
        Get pages from website home page
        """
        bs = self.getPage(self.site.startUrl)
        targetPages = bs.find_all('a',
            href=re.compile(self.site.targetPattern))
        for targetPage in targetPages:
            targetPage = targetPage.attrs['href']
            if targetPage not in self.visited:
                self.visited.append(targetPage)
                if not self.site.absoluteUrl:
                    targetPage = '{}{}'.format(self.site.baseUrl, targetPage)
                self.parse(targetPage)    

falabella = Website(

    "Falabella Perú",

    # DOMINIO BASE
    "https://www.falabella.com.pe",

    # PÁGINA DESDE DONDE COMENZAMOS
    "https://www.falabella.com.pe/falabella-pe/category/cat40712/Laptops",

    # SOLO QUEREMOS URLs DE PRODUCTOS
    r"^/falabella-pe/product/",

    # Las URLs encontradas son relativas
    False,

    # Título del producto
    "h1",

    # Por ahora extraemos el contenido general
    # de la página para comprobar que funciona
    "body"

)


crawler = Crawler(
    falabella
)


crawler.crawl()