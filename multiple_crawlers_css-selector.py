import requests
from bs4 import BeautifulSoup


# =========================================================
# 1. CONTENT
# =========================================================

class Content:
    """
    CONTENT = RESULTADO DEL SCRAPING.

    Guarda los datos REALES encontrados.

    content
    ├── url
    ├── title
    └── body
    """


    def __init__(self, url, title, body):

        self.url = url

        self.title = title

        self.body = body


    def print(self):

        print(f"URL: {self.url}")

        print(f"Título: {self.title}")

        print(f"Cuerpo:\n{self.body}")



# =========================================================
# 2. WEBSITE
# =========================================================

class Website:
    """
    WEBSITE = INSTRUCCIONES.

    Guarda:

    name
    → nombre del sitio

    url
    → URL principal

    title_selector
    → dónde buscar el título

    body_selector
    → dónde buscar el cuerpo
    """


    def __init__(
        self,
        name,
        url,
        title_selector,
        body_selector
    ):

        self.name = name

        self.url = url

        self.title_selector = title_selector

        self.body_selector = body_selector



# =========================================================
# 3. CRAWLER
# =========================================================

class Crawler:


    # =====================================================
    # 3.1 GET PAGE
    # =====================================================

    def getPage(self, url):
        """
        GET PAGE = DESCARGAR.

        url
         ↓
        requests.get()
         ↓
        response
         ↓
        verificar HTTP
         ↓
        BeautifulSoup
         ↓
        page
         ↓
        return page
        """


        print("\nIntentando descargar:")

        print(url)


        # -------------------------------------------------
        # USER AGENT
        # -------------------------------------------------

        # Indicamos un User-Agent típico de navegador.
        #
        # Algunas páginas rechazan solicitudes
        # que no contienen uno.

        headers = {

            "User-Agent":
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/151.0.0.0 "
            "Safari/537.36"

        }


        try:

            response = requests.get(
                url,
                headers=headers,
                timeout=10
            )


        # -------------------------------------------------
        # TIMEOUT
        # -------------------------------------------------

        except requests.exceptions.Timeout:

            print(
                "\n❌ La página tardó demasiado "
                "en responder."
            )

            return None


        # -------------------------------------------------
        # OTRO ERROR DE REQUESTS
        # -------------------------------------------------

        except requests.exceptions.RequestException as error:

            print(
                "\n❌ Error al descargar la página:"
            )

            print(error)

            return None



        # -------------------------------------------------
        # EL SERVIDOR RESPONDIÓ
        # -------------------------------------------------

        print(
            "\n✅ El servidor respondió."
        )


        print(
            f"Estado HTTP: {response.status_code}"
        )


        print(
            f"URL final: {response.url}"
        )



        # -------------------------------------------------
        # COMPROBAR STATUS CODE
        # -------------------------------------------------

        # Queremos continuar solamente
        # cuando recibimos HTTP 200.
        #
        #
        # Ejemplos:
        #
        # 200 → OK
        #
        # 401 → Unauthorized
        #
        # 403 → Forbidden
        #
        # 404 → Not Found


        if response.status_code != 200:

            print(
                "\n❌ El servidor NO entregó "
                "la página correctamente."
            )


            print(
                "No intentaremos buscar "
                "selectores CSS."
            )


            return None



        # -------------------------------------------------
        # CREAR BEAUTIFULSOUP
        # -------------------------------------------------

        page = BeautifulSoup(
            response.text,
            "html.parser"
        )


        print(
            "\n✅ Página convertida a BeautifulSoup."
        )


        return page



    # =====================================================
    # 3.2 SAFE GET
    # =====================================================

    def safeGet(self, page, selector):
        """
        SAFE GET = EXTRAER.

        page
        =
        dónde buscar


        selector
        =
        qué buscar
        """


        selected_elements = page.select(
            selector
        )


        # -------------------------------------------------
        # SI NO ENCONTRÓ NADA
        # -------------------------------------------------

        if len(selected_elements) == 0:

            return ""



        # -------------------------------------------------
        # EXTRAER LOS TEXTOS
        # -------------------------------------------------

        texts = []


        for element in selected_elements:

            text = element.get_text()

            texts.append(
                text
            )



        # -------------------------------------------------
        # UNIR LOS TEXTOS
        # -------------------------------------------------

        result = "\n".join(
            texts
        )


        return result



    # =====================================================
    # 3.3 PARSE
    # =====================================================

    def parse(self, site, url):
        """
        PARSE = COORDINADOR.

        site
        → instrucciones Website

        url
        → artículo específico
        """


        print("\n")
        print("=" * 60)

        print(
            f"PROCESANDO SITIO: {site.name}"
        )

        print("=" * 60)



        # -------------------------------------------------
        # PASO 1
        # DESCARGAR
        # -------------------------------------------------

        page = self.getPage(
            url
        )



        # -------------------------------------------------
        # PASO 2
        # ¿TENEMOS PÁGINA?
        # -------------------------------------------------

        if page is None:

            print(
                "\n❌ No podemos continuar "
                "con este sitio."
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
        # DIAGNÓSTICO
        # -------------------------------------------------

        print(
            "\nResultado:"
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
        # SI FALTA ALGO
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
            "\n✅ Título y cuerpo encontrados."
        )


        print(
            "Creando Content..."
        )


        content = Content(
            url,
            title,
            body
        )


        return content



# =========================================================
# 4. CREAR CRAWLER
# =========================================================

crawler = Crawler()



# =========================================================
# 5. DATOS DE LOS WEBSITES
# =========================================================

siteData = [

    # -----------------------------------------------------
    # O'REILLY
    # -----------------------------------------------------

    [
        "O'Reilly Media",
        "https://www.oreilly.com",
        "h1",
        "section#product-description"
    ],


    # -----------------------------------------------------
    # REUTERS
    # -----------------------------------------------------

    [
        "Reuters",
        "https://www.reuters.com",
        "h1",
        "div.StandardArticleBody_body_1gnLA"
    ],


    # -----------------------------------------------------
    # BROOKINGS
    # -----------------------------------------------------

    [
        "Brookings",
        "https://www.brookings.edu",
        "h1",
        "div.byo-block.wysiwyg-block.wysiwyg"
    ],


    # -----------------------------------------------------
    # NEW YORK TIMES
    # -----------------------------------------------------

    [
        "New York Times",
        "https://www.nytimes.com",
        "h1",
        "p.story-content"
    ]

]



# =========================================================
# 6. CONVERTIR siteData EN OBJETOS WEBSITE
# =========================================================

websites = []


for row in siteData:

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
# 7. O'REILLY
# =========================================================

content = crawler.parse(

    websites[0],

    "http://shop.oreilly.com/product/"
    "0636920028154.do"

)


if content is not None:

    print("\n")
    print("=" * 60)
    print("CONTENT O'REILLY")
    print("=" * 60)

    content.print()



# =========================================================
# 8. REUTERS
# =========================================================

content = crawler.parse(

    websites[1],

    "http://www.reuters.com/article/"
    "us-usa-epa-pruitt-idUSKBN19W2D0"

)


if content is not None:

    print("\n")
    print("=" * 60)
    print("CONTENT REUTERS")
    print("=" * 60)

    content.print()



# =========================================================
# 9. BROOKINGS
# =========================================================

content = crawler.parse(

    websites[2],

    "https://www.brookings.edu/blog/"
    "techtank/2016/03/01/"
    "idea-to-retire-old-methods-of-policy-education/"

)


if content is not None:

    print("\n")
    print("=" * 60)
    print("CONTENT BROOKINGS")
    print("=" * 60)

    content.print()



# =========================================================
# 10. NEW YORK TIMES
# =========================================================

content = crawler.parse(

    websites[3],

    "https://www.nytimes.com/2018/01/"
    "28/business/energy-environment/"
    "oil-boom.html"

)


if content is not None:

    print("\n")
    print("=" * 60)
    print("CONTENT NEW YORK TIMES")
    print("=" * 60)

    content.print()