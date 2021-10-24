from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from lesson08.instaparser.spiders.insta import InstaSpider as IS1
from lesson08.instaparser.spiders.insta_ import InstaSpider as IS2
from lesson08.instaparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(IS1)
    process.crawl(IS2)

    process.start()