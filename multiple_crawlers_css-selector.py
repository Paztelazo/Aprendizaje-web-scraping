import requests
from bs4 import BeautifulSoup


# =========================================================
# 1. CONTENT
# =========================================================

class Content:
    """
    CONTENT = EL RESULTADO DEL SCRAPING.

    Esta clase NO descarga páginas.
    Esta clase NO busca elementos.

    Solo sirve para GUARDAR los datos reales
    que ya encontramos en UNA página.

    Ejemplo mental:

    content
    ├── url
    ├── title
    └── body
    """


    def __init__(self, url, title, body):

        # URL real de la página scrapeada.
        self.url = url

        # Título real encontrado.
        self.title = title

        # Cuerpo real encontrado.
        self.body = body


    def print(self):
        """
        Muestra en pantalla los datos
        guardados dentro del objeto Content.
        """

        print(f"URL: {self.url}")

        print(f"Título: {self.title}")

        print(f"Cuerpo:\n{self.body}")



# =========================================================
# 2. WEBSITE
# =========================================================

class Website:
    """
    WEBSITE = LAS INSTRUCCIONES PARA SCRAPEAR UN SITIO.

    NO guarda el título real.
    NO guarda el cuerpo real.

    Guarda DÓNDE debemos buscar esos datos.

    Ejemplo:

    Website
    ├── name
    │   └── "Brookings"
    │
    ├── url
    │   └── "https://www.brookings.edu"
    │
    ├── title_selector
    │   └── "h1"
    │
    └── body_selector
        └── "div.post-body"


    DIFERENCIA:

    title_selector = "h1"
    → INSTRUCCIÓN de dónde buscar


    title = "Mi artículo"
    → DATO REAL encontrado
    """


    def __init__(
        self,
        name,
        url,
        title_selector,
        body_selector
    ):

        # Nombre del sitio.
        self.name = name

        # URL principal del sitio.
        self.url = url

        # Dónde buscar el título.
        self.title_selector = title_selector

        # Dónde buscar el cuerpo.
        self.body_selector = body_selector



# =========================================================
# 3. CRAWLER
# =========================================================

class Crawler:
    """
    CRAWLER = EL TRABAJADOR.

    Tiene tres tareas:

    getPage()
    → DESCARGAR

    safeGet()
    → EXTRAER

    parse()
    → COORDINAR TODO
    """



    # =====================================================
    # 3.1 GET PAGE
    # =====================================================

    def getPage(self, url):
        """
        GET PAGE = DESCARGAR UNA PÁGINA.

        Flujo:

        url
         ↓
        requests.get()
         ↓
        response
         ↓
        response.text
         ↓
        BeautifulSoup
         ↓
        page
         ↓
        return page
        """


        print("\nIntentando descargar:")

        print(url)


        try:

            # Hace la solicitud HTTP.
            #
            # timeout=10 significa:
            #
            # "No te quedes esperando demasiado
            # si el servidor no responde correctamente."
            response = requests.get(
                url,
                timeout=10
            )


        # -------------------------------------------------
        # CASO: LA PÁGINA TARDA DEMASIADO
        # -------------------------------------------------

        except requests.exceptions.Timeout:

            print(
                "\n❌ La página tardó demasiado en responder."
            )

            return None


        # -------------------------------------------------
        # CASO: OTRO ERROR DE REQUESTS
        # -------------------------------------------------

        except requests.exceptions.RequestException as error:

            print(
                "\n❌ Error al descargar la página:"
            )

            print(error)

            return None


        # -------------------------------------------------
        # SI LLEGAMOS AQUÍ:
        # EL SERVIDOR RESPONDIÓ
        # -------------------------------------------------

        print(
            "\n✅ El servidor respondió."
        )


        # Código HTTP recibido.
        #
        # Ejemplos:
        #
        # 200 → OK
        # 403 → acceso prohibido
        # 404 → no encontrado
        print(
            f"Estado HTTP: {response.status_code}"
        )


        # requests puede seguir redirecciones.
        #
        # Por eso mostramos también
        # dónde terminamos realmente.
        print(
            f"URL final: {response.url}"
        )


        # Convertimos el HTML recibido
        # en un objeto BeautifulSoup.
        page = BeautifulSoup(
            response.text,
            "html.parser"
        )


        # Devolvemos la página preparada.
        return page



    # =====================================================
    # 3.2 SAFE GET
    # =====================================================

    def safeGet(self, page, selector):
        """
        SAFE GET = EXTRAER UN DATO.

        page
        =
        DÓNDE buscar


        selector
        =
        QUÉ buscar


        Ejemplo:

        safeGet(
            page,
            "h1"
        )


        podría devolver:

        "Mi artículo"


        Si no encuentra nada:

        return ""
        """


        # -------------------------------------------------
        # PASO 1
        # BUSCAR
        # -------------------------------------------------

        selected_elements = page.select(
            selector
        )


        # Ejemplo:
        #
        # HTML:
        #
        # <h1>Mi artículo</h1>
        #
        #
        # selector:
        #
        # "h1"
        #
        #
        # page.select("h1")
        #
        # devuelve:
        #
        # [
        #     <h1>Mi artículo</h1>
        # ]
        #
        #
        # Eso se guarda en:
        #
        # selected_elements



        # -------------------------------------------------
        # PASO 2
        # ¿ENCONTRAMOS ALGO?
        # -------------------------------------------------

        if len(selected_elements) == 0:

            # Si no encontró nada:
            #
            # selected_elements = []
            #
            # devolvemos un string vacío.
            return ""



        # -------------------------------------------------
        # PASO 3
        # PREPARAR LISTA DE TEXTOS
        # -------------------------------------------------

        texts = []



        # -------------------------------------------------
        # PASO 4
        # RECORRER LOS ELEMENTOS ENCONTRADOS
        # -------------------------------------------------

        for element in selected_elements:

            # Ejemplo:
            #
            # element =
            #
            # <p>Hola</p>


            # Extraemos solamente el texto.
            #
            # <p>Hola</p>
            #
            #      ↓
            #
            # "Hola"
            text = element.get_text()


            # Guardamos el texto.
            texts.append(text)



        # -------------------------------------------------
        # PASO 5
        # UNIR LOS TEXTOS
        # -------------------------------------------------

        # Ejemplo:
        #
        # texts =
        #
        # [
        #     "Párrafo 1",
        #     "Párrafo 2"
        # ]
        #
        #
        # "\n".join(texts)
        #
        # produce:
        #
        # Párrafo 1
        # Párrafo 2

        result = "\n".join(
            texts
        )



        # -------------------------------------------------
        # PASO 6
        # DEVOLVER RESULTADO
        # -------------------------------------------------

        return result



    # =====================================================
    # 3.3 PARSE
    # =====================================================

    def parse(self, site, url):
        """
        PARSE = COORDINAR TODO EL PROCESO.

        Recibe:

        site
        → objeto Website con instrucciones


        url
        → página concreta que queremos scrapear


        Flujo:

        getPage()
            ↓
        page
            ↓
        safeGet(título)
            ↓
        title
            ↓
        safeGet(cuerpo)
            ↓
        body
            ↓
        Content(...)
            ↓
        return content
        """


        print("\n")
        print("=" * 60)

        print(
            f"PROCESANDO SITIO: {site.name}"
        )

        print("=" * 60)



        # -------------------------------------------------
        # PASO 1
        # DESCARGAR PÁGINA
        # -------------------------------------------------

        page = self.getPage(url)



        # -------------------------------------------------
        # PASO 2
        # ¿PUDIMOS OBTENER LA PÁGINA?
        # -------------------------------------------------

        if page is None:

            print(
                "\n❌ No se pudo obtener la página."
            )

            return None



        # -------------------------------------------------
        # PASO 3
        # BUSCAR TÍTULO
        # -------------------------------------------------

        print(
            "\nBuscando título..."
        )


        print(
            f"Selector utilizado: "
            f"{site.title_selector}"
        )


        # Ejemplo:
        #
        # site.title_selector = "h1"
        #
        #
        # entonces realmente hacemos:
        #
        # safeGet(
        #     page,
        #     "h1"
        # )

        title = self.safeGet(
            page,
            site.title_selector
        )


        if title == "":

            print(
                "❌ No se encontró el título."
            )

        else:

            print(
                "✅ Título encontrado."
            )

            print(
                f"Título: {title}"
            )



        # -------------------------------------------------
        # PASO 4
        # BUSCAR CUERPO
        # -------------------------------------------------

        print(
            "\nBuscando cuerpo..."
        )


        print(
            f"Selector utilizado: "
            f"{site.body_selector}"
        )


        # Ejemplo:
        #
        # site.body_selector =
        # "div.post-body"
        #
        #
        # entonces:
        #
        # safeGet(
        #     page,
        #     "div.post-body"
        # )

        body = self.safeGet(
            page,
            site.body_selector
        )


        if body == "":

            print(
                "❌ No se encontró el cuerpo."
            )

        else:

            print(
                "✅ Cuerpo encontrado."
            )



        # -------------------------------------------------
        # PASO 5
        # MOSTRAR DIAGNÓSTICO
        # -------------------------------------------------

        print(
            "\nResultado de la búsqueda:"
        )


        print(
            f"¿Título encontrado? "
            f"{title != ''}"
        )


        print(
            f"¿Cuerpo encontrado? "
            f"{body != ''}"
        )



        # -------------------------------------------------
        # PASO 6
        # COMPROBAR QUE TENEMOS AMBOS DATOS
        # -------------------------------------------------

        if title == "" or body == "":

            print(
                "\n❌ No se crea Content porque "
                "falta título o cuerpo."
            )

            return None



        # -------------------------------------------------
        # PASO 7
        # CREAR CONTENT
        # -------------------------------------------------

        print(
            "\n✅ Se encontraron ambos datos."
        )


        print(
            "Creando objeto Content..."
        )


        content = Content(
            url,
            title,
            body
        )



        # -------------------------------------------------
        # PASO 8
        # DEVOLVER CONTENT
        # -------------------------------------------------

        return content



# =========================================================
# 4. CREAR EL CRAWLER
# =========================================================

# Aquí recién creamos un objeto Crawler.
#
# Hasta antes solo habíamos DEFINIDO la clase.

crawler = Crawler()



# =========================================================
# 5. DATOS DE LOS SITIOS
# =========================================================

siteData = [

    [
        "O'Reilly Media",
        "http://oreilly.com",
        "h1",
        "section#product-description"
    ],

    [
        "Reuters",
        "http://reuters.com",
        "h1",
        "div.StandardArticleBody_body_1gnLA"
    ],

    [
        "Brookings",
        "http://www.brookings.edu",
        "h1",
        "p"
    ],

    [
        "New York Times",
        "http://nytimes.com",
        "h1",
        "p.story-content"
    ]
]



# =========================================================
# 6. CONVERTIR LAS LISTAS EN OBJETOS WEBSITE
# =========================================================

websites = []


for row in siteData:

    # Cada row tiene:
    #
    # row[0] → nombre
    # row[1] → URL principal
    # row[2] → selector título
    # row[3] → selector cuerpo


    website = Website(
        row[0],
        row[1],
        row[2],
        row[3]
    )


    websites.append(
        website
    )



# =========================================================
# 7. PROBAR SOLO BROOKINGS
# =========================================================

# websites[2]
#
# corresponde al objeto Website de Brookings.
#
#
# Mentalmente:
#
# websites[2]
# ├── name = "Brookings"
# ├── title_selector = "h1"
# └── body_selector = "div.post-body"


content = crawler.parse(
    websites[2],
    "https://www.brookings.edu/blog/"
    "techtank/2016/03/01/"
    "idea-to-retire-old-methods-of-policy-education/"
)



# =========================================================
# 8. MOSTRAR EL RESULTADO
# =========================================================

# parse() puede devolver:
#
# Content
#
# o
#
# None
#
#
# Por eso primero comprobamos
# que realmente haya un Content.

if content is not None:

    print("\n")
    print("=" * 60)
    print("CONTENT FINAL")
    print("=" * 60)

    content.print()