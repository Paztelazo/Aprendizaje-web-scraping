import requests
from bs4 import BeautifulSoup


# ---------------------------------------------------------
# MODELO COMÚN PARA EL CONTENIDO EXTRAÍDO
# ---------------------------------------------------------

class Content:

    def __init__(self, url, title, body):
        # __init__ es un método especial que se ejecuta
        # automáticamente cada vez que creamos un objeto Content.
        #
        # La idea es:
        #
        # "Cada vez que alguien cree un objeto de esta clase,
        # quiero que empiece teniendo:
        #
        # - una URL
        # - un título
        # - un cuerpo"
        #
        # __init__ es un "dunder method":
        # double underscore method.
        #
        # self representa al objeto específico que se está creando.
        #
        # Por ejemplo:
        #
        # articulo = Content(url, title, body)
        #
        # durante __init__:
        #
        # self -> articulo

        # Guarda la URL recibida dentro del objeto.
        self.url = url

        # Guarda el título recibido dentro del objeto.
        self.title = title

        # Guarda el contenido recibido dentro del objeto.
        self.body = body


# ---------------------------------------------------------
# DESCARGAR Y ANALIZAR UNA PÁGINA
# ---------------------------------------------------------

def getPage(url):

    # requests.get(url) hace una solicitud HTTP GET
    # a la URL recibida.
    #
    # En una sola línea:
    # 1. prepara la solicitud,
    # 2. la envía al servidor,
    # 3. recibe la respuesta.
    #
    # Por eso esta variable sería más claro llamarla "response".
    response = requests.get(url)

    # response contiene toda la respuesta HTTP del servidor.
    #
    # Por ejemplo:
    # response.status_code -> código HTTP, como 200 o 404
    # response.headers     -> encabezados de la respuesta
    # response.url         -> URL final
    # response.text        -> contenido de la respuesta como texto
    #
    # Si la respuesta es una página web HTML,
    # response.text contiene ese HTML como string.

    # BeautifulSoup recibe el HTML en texto
    # y lo analiza usando el parser "html.parser".
    #
    # Devuelve un objeto BeautifulSoup que luego podemos recorrer con:
    # find()
    # find_all()
    # .text
    # etc.
    return BeautifulSoup(
        response.text,
        "html.parser"
    )
# ---------------------------------------------------------
# SCRAPER ESPECÍFICO PARA THE NEW YORK TIMES
# ---------------------------------------------------------

def scrapeNYTimes(url):

    # Descarga la página y obtiene un objeto BeautifulSoup.
    bs = getPage(url) #Ejecuta getPage() y guarda el resultado de ese return en la variable bs.

    # Busca la etiqueta <h1> y extrae solamente su texto.
    #
    # Ejemplo:
    #
    # <h1>Una noticia importante</h1>
    #
    # title será:
    #
    # "Una noticia importante"
    title = bs.find("h1").text 

    # Busca todos los párrafos <p>
    # que tengan la clase "story-content".
    #
    # Podría devolver algo como:
    #
    # [
    #     <p class="story-content">Párrafo 1</p>,
    #     <p class="story-content">Párrafo 2</p>,
    #     <p class="story-content">Párrafo 3</p>
    # ]
    lines = bs.find_all(
        "p",
        {"class": "story-content"}
    )

    # Extrae el texto de cada párrafo y luego
    # los une utilizando un salto de línea.
    #
    # Primero:
    #
    # [line.text for line in lines]
    #
    # produce algo como:
    #
    # [
    #     "Párrafo 1",
    #     "Párrafo 2",
    #     "Párrafo 3"
    # ]
    #
    # Después:
    #
    # "\n".join(...)
    #
    # produce:
    #
    # Párrafo 1
    # Párrafo 2
    # Párrafo 3
    body = "\n".join(
        [line.text for line in lines]
    ) 
    #line.text for line in lines es una lista de comprensión que recorre cada elemento de
    #lines y extrae su texto. Por ejemplo, si lines contiene tres párrafos, esta lista de comprensión devolverá 
    # una lista con los textos de esos tres párrafos.
    #y line.text es el texto de cada párrafo, sin las etiquetas HTML.
    #Primera vuelta:
    #line = <p>Hola</p>
    #line.text = "Hola"

    #Segunda vuelta:
    #line = <p>Me llamo Gerson</p>
    #line.text = "Me llamo Gerson"

    #Tercera vuelta:
    #line = <p>Estoy aprendiendo Python</p>
    #line.text = "Estoy aprendiendo Python"

#.join une varios strings en uno solo, utilizando el string que lo llama como separador.
# En este caso, "\n" es el separador, por lo que los textos de los párrafos se unirán con un salto de línea entre ellos.



    # Finalmente crea un objeto Content.
    #
    # No devuelve BeautifulSoup.
    # No devuelve solamente el título.
    #
    # Devuelve un objeto estándar con:
    #
    # Content
    # ├── url
    # ├── title
    # └── body
    return Content(
        url,
        title,
        body
    )


# ---------------------------------------------------------
# SCRAPER ESPECÍFICO PARA BROOKINGS
# ---------------------------------------------------------

def scrapeBrookings(url):

    # Descarga y analiza la página.
    bs = getPage(url)

    # Obtiene el título desde <h1>.
    title = bs.find("h1").text

    # Busca todos los párrafos <p> de la página.
    lines = bs.find_all("p")

    # Extrae el texto de cada párrafo
    # y los une con saltos de línea.
    body = "\n".join(
        [line.text for line in lines]
    )

    # Aunque Brookings tiene un HTML diferente a NYTimes,
    # al final también devuelve el mismo tipo de objeto:
    #
    # Content(url, title, body)
    return Content(
        url,
        title,
        body
    )


# ---------------------------------------------------------
# PROBAR EL SCRAPER DE BROOKINGS
# ---------------------------------------------------------

url = (
    "https://www.brookings.edu/blog/future-development/"
    "2018/01/26/delivering-inclusive-urban-access-3-unc"
    "omfortable-truths/"
)

# scrapeBrookings() devuelve un objeto Content.
content = scrapeBrookings(url) #obtiene titulo y cuerpo del artículo de Brookings y lo guarda en la variable content.


# Accedemos a los atributos guardados
# dentro del objeto Content.

print(
    "Title: {}".format(
        content.title
    )
)

print(
    "URL: {}\n".format(
        content.url
    )
)

print(content.body)


# ---------------------------------------------------------
# PROBAR EL SCRAPER DE NEW YORK TIMES
# ---------------------------------------------------------

url = (
    "https://www.nytimes.com/"
    "2018/01/25/opinion/sunday/"
)

# Ahora utilizamos otro scraper.
#
# Este scraper entiende el HTML de NYTimes,
# pero también devuelve un Content.
content = scrapeNYTimes(url)


print(
    "Title: {}".format(
        content.title
    )
)

print(
    "URL: {}\n".format(
        content.url
    )
)

print(content.body)