# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

#Quiero crear mi propio tipo de Item llamado Article, utilizando el comportamiento que Scrapy ya proporciona en Item.


from dataclasses import dataclass
import scrapy


@dataclass
class ScrapyCrawlersItem:
    # define the fields for your item here like:
    # name: str | None = None
    pass


class Article(scrapy.Item):

    url = scrapy.Field()

    title = scrapy.Field()

    text = scrapy.Field()

    lastUpdated = scrapy.Field()
