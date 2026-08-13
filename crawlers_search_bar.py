import requests
from bs4 import BeautifulSoup


class Content:
    """Common base class for all articles/pages"""
    def __init__(self, topic, url, title, body):
        self.topic = topic #e.g. cybersecurity, AI, etc.
        self.title = title #Introduction to AI
        self.body = body #AI is a branch of computer science that aims to create intelligent machines...
        self.url = url #https://www.example.com/ai/ai-introduction

    def print(self):
        """
        Flexible printing function controls output
        """
        print("New article found for topic: {}".format(self.topic))
        print("TITLE: {}".format(self.title))
        print("BODY:\n{}".format(self.body))
        print("URL: {}".format(self.url))     


class Website:
    """Contains information about website structure"""
    def __init__(self, name, url, searchUrl, resultListing, resultUrl, absoluteUrl, titleTag, bodyTag):
        self.name = name #Example News
        self.url = url #https://www.example.com
        self.searchUrl = searchUrl #https://www.example.com/search?q=
        self.resultListing = resultListing #Representa el elemento HTML que envuelve la lista de resultados. Ejemplo "div.result"
        self.resultUrl = resultUrl #Indica donde está el enlace a la noticia dentro del resultado de búsqueda. Ejemplo: 'a.result-link".
        self.absoluteUrl=absoluteUrl #Indica si la URL del resultado es absoluta o relativa. False significa que es relativa y se debe concatenar con la URL base del sitio web.
        self.titleTag = titleTag #Indica el tag HTML para el título de la noticia.
        self.bodyTag = bodyTag #Indica el tag HTML para el cuerpo de la noticia.

class Crawler:
    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')

    
    def safeGet(self, page, selector):
        selected_elements = page.select(selector) #por ejemplo: page.select('h1.title')
        if selected_elements is not None and len(selected_elements) > 0:
            return selected_elements[0].get_text()
        return ""

    
    def search(self, topic, site):
        """
        Searches a given website for a given topic and records all pages found
        """
        bs = self.getPage(site.searchUrl + topic)
        searchResults = bs.select(site.resultListing)
        for result in searchResults:
            url = result.select(site.resultUrl)[0].attrs["href"]
            # Check to see whether it's a relative or an absolute URL
            if(site.absoluteUrl):
                bs = self.getPage(url)
            else:
                bs = self.getPage(site.url + url)
            if bs is None:
                print("Something was wrong with that page or URL. Skipping!")
                return
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)
            if title != '' and body != '':
                content = Content(topic, url, title, body)
                content.print()
crawler = Crawler()

siteData = [
    ['O\'Reilly Media', 'http://oreilly.com',
        'https://ssearch.oreilly.com/?q=','article.product-result',
        'p.title a', True, 'h1', 'section#product-description'],
    ['Reuters', 'http://reuters.com',
        'http://www.reuters.com/search/news?blob=',
        'div.search-result-content','h3.search-result-title a',
        False, 'h1', 'div.StandardArticleBody_body_1gnLA'],
    ['Brookings', 'http://www.brookings.edu',
        'https://www.brookings.edu/search/?s=',
        'div.list-content article', 'h4.title a', True, 'h1', 'div.post-body']
]

sites = []
for row in siteData:
    sites.append(Website(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

topics = [
    "python",
    "data science"
]


for topic in topics:

    print(
        "GETTING INFO ABOUT: " + topic
    )


    for targetSite in sites:

        crawler.search(
            topic,
            targetSite
        )