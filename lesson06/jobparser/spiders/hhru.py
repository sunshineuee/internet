import scrapy
from scrapy.http import HtmlResponse
from lesson06.jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']

    def __init__(self, vacansy):
        self.start_urls = [f'https://hh.ru/search/vacancy?area=1&st=searchVacancy&text={vacansy}']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        job_links = response.xpath('//a[@data-qa="vacancy-serp__vacancy-title"]/@href').extract()
        for link in job_links:
            yield response.follow(link, callback=self.vacansy_parce)




    def vacansy_parce(self, response:HtmlResponse):
        link = response.url
        name = response.xpath("//h1/text()").extract_first()
        salary = response.xpath('//p[contains(@class,"vacancy-salary")]/span/text()').getall()
        company_name = response.xpath('//a[@data-qa="vacancy-company-name"]/span/text()').getall()
        company_address = response.xpath('//p[@data-qa="vacancy-view-location"]/text()').get()
        yield JobparserItem(name=name, salary=salary, company_name=company_name, company_address=company_address, link=link)