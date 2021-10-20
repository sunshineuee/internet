from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

import settings
from lesson06.jobparser.spiders.hhru import HhruSpider
from lesson06.jobparser.spiders.sjru import SjruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(HhruSpider, vacansy='python')
    process.crawl(SjruSpider, vacansy='python')

    process.start()
