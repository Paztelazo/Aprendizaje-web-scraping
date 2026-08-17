from scrapy_crawlers.items import Article
#Con este codigo ya no damos manualmente las URLs
#Empieza con una pagina de Wikipedia, encuentra enlaces automaticamente, sigue esos enlaces y extrae
#ASI DESCUBRES URLS POR TI MISMO

from scrapy.linkextractors import LinkExtractor #Busca enlaces <a href="..."> dentro de una pagina
from scrapy.spiders import CrawlSpider, Rule #CrawlSpider es un tipo especializado de Spider. Puede descubir enlaces mediantes Rules que definas
class ArticleSpider(CrawlSpider):
    name = 'articles'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']
    rules = [
    Rule(
    LinkExtractor(allow='(/wiki/)((?!:).)*$'),
    callback='parse_items',
    follow=True
    ),
    Rule(
    LinkExtractor(allow='.*'),
    callback='parse_items'
            )
    ]

    def parse_items(self, response):
        article = Article()
        article["url"] = response.url
        article["title"] = response.css("span.mw-page-title-main::text").get()
        article["text"] = response.xpath('//div[@id="mw-content-text"]//text()').extract()
        lastUpdated = response.css('li#footer-info-lastmod::text').get()
        article['lastUpdated'] =lastUpdated.replace('This page was last edited on ', '')
        return article