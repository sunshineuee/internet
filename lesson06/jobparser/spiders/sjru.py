import scrapy
from scrapy.http import HtmlResponse
from lesson06.jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']

    def __init__(self, vacansy):
        self.start_urls = [f'https://russia.superjob.ru/vacancy/search/?keywords={vacansy}']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[contains(@class,' f-test-link-Dalshe')]/@href").extract_first()
        job_links = response.xpath("//a[contains(@class, 'icMQ_ _6AfZ9 f-test-link')]/@href").extract()
        for link in job_links:
            link = link.split('?')[0]
            yield response.follow(link, callback=self.vacansy_parce)


        yield response.follow(next_page, callback=self.parse)


    def vacansy_parce(self, response:HtmlResponse):
        link = response.url
        name = response.xpath('//h1/span/text()').get()
        salary = response.xpath('//span[@class="_2Wp8I _2rfUm _2hCDz"]/text()').getall()
        company_name = response.xpath('//h2[@class="_1h3Zg _2rfUm _2hCDz _2ZsgW _21a7u _2SvHc"]/text()').getall()
        company_address = response.xpath('//div[@class="f-test-address _3AQrx"]/span/span/text()').get()
        yield JobparserItem(name=name, salary=salary, company_name=company_name, company_address=company_address, link=link)