from scrapy import Spider, Request


# Creamos nuestro Spider.
#
# ArticleSpider hereda de la clase Spider de Scrapy.
# Gracias a esa herencia, nuestro crawler obtiene toda la funcionalidad
# que Scrapy ya trae para manejar Requests, Responses, callbacks, etc.
class ArticleSpider(Spider):


    # Nombre interno del Spider.
    # Este nombre permite ejecutarlo, por ejemplo:
    # scrapy crawl article
    # "article" NO tiene por qué ser igual al nombre del archivo .py.
    name = "article"


    # start() es el método moderno que Scrapy utiliza al iniciar el Spider.
    # Su función es generar las primeras peticiones que Scrapy procesará.
    # Es "async" porque Scrapy actualmente trabaja con un sistema
    # asíncrono para manejar múltiples operaciones de red.
    async def start(self):


        # Guardamos las páginas que queremos visitar inicialmente
        # dentro de una lista.
        # IMPORTANTE:
        # En este momento solamente son strings.
        # Todavía NO se ha descargado ninguna página.
        urls = [

            "https://en.wikipedia.org/wiki/Python_%28programming_language%29",

            "https://en.wikipedia.org/wiki/Functional_programming",

            "https://en.wikipedia.org/wiki/Monty_Python"

        ]


        # Recorremos nuestra lista URL por URL.
        # Primera vuelta:
        # url = "https://...Python..."
        # Segunda vuelta:
        # url = "https://...Functional_programming"
        # Tercera vuelta:
        # url = "https://...Monty_Python"
        for url in urls:


            # Creamos un objeto Request de Scrapy.
            # Request representa:
            #
            # "Scrapy, quiero que visites esta URL."
            #
            # url=url
            # --------
            # Le pasamos la URL que estamos recorriendo actualmente.
            #
            #
            # callback=self.parse
            # -------------------
            # Le decimos a Scrapy:
            #
            # "Cuando hayas descargado esta página,
            #  envía la respuesta al método parse."
            #
            # IMPORTANTE:
            #
            # ponemos:
            #
            #     self.parse
            #
            # y NO:
            #
            #     self.parse()
            #
            # porque NO queremos ejecutar parse ahora.
            #
            # Solamente estamos indicándole a Scrapy
            # qué función deberá ejecutar DESPUÉS.
            request = Request(

                url=url,

                callback=self.parse

            )


            # yield entrega este Request a Scrapy.
            #
            # Es parecido a decir:
            #
            # "Scrapy, aquí tienes una petición para procesar."
            #
            # Scrapy recibe el Request y se encargará de:
            #
            # 1. conectarse a Wikipedia
            # 2. pedir la página
            # 3. recibir el HTML
            # 4. construir un objeto Response
            # 5. mandar ese Response al callback self.parse
            #
            # Después, el for puede continuar con la siguiente URL.
            yield request


    # parse() es nuestro callback.
    #
    # Nosotros NO llamamos directamente:
    #
    #     parse(...)
    #
    # Scrapy lo ejecuta automáticamente después
    # de recibir la respuesta de una página.
    #
    #
    # El parámetro response contiene la respuesta HTTP
    # de la página que Scrapy acaba de descargar.
    def parse(self, response):


        # response.url contiene la URL final de la página descargada.
        # Por ejemplo:
        # https://en.wikipedia.org/wiki/Monty_Python
        # Guardamos ese valor en una variable llamada url.
        url = response.url


        # Ahora buscamos el título <h1> dentro del HTML.
        # response.css(...)
        # -----------------
        # permite utilizar selectores CSS sobre el HTML recibido.
        # "h1::text"
        # -----------
        # h1
        #    busca una etiqueta <h1>
        # ::text
        #    extrae solamente el texto que hay dentro de ella
        #
        # Si tenemos:
        # <h1>Monty Python</h1>
        # queremos obtener:

        # "Monty Python"
        #
        #
        # .get()
        # ------
        # devuelve el primer resultado encontrado.
        title = response.css(".mw-page-title-main::text").get()


        # Finalmente imprimimos la URL que estamos procesando.
        print(f"URL is: {url}")


        # E imprimimos el título que acabamos de extraer.
        print(f"Title is: {title}")