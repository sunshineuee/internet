import scrapy
from scrapy.http import HtmlResponse
from lesson07.leroy.items import LeroyItem
from scrapy.loader import ItemLoader

class leroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}&suggest=true']

    def parse(self, response:HtmlResponse):
        products = response.xpath("//div[@data-qa-product]/a")
        next_page = response.xpath("//a[contains(@aria-label, 'Следующая страница')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for product in products:
            yield response.follow(product, callback=self.ads_parse)

    def ads_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//uc-pdp-price-view[@slot='primary-price']/span[@slot='price']/text()")
        loader.add_xpath('photos', "//picture[@slot='pictures']/img[@itemprop='image']/@src")

        yield loader.load_item()