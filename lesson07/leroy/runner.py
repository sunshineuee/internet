from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

import settings
from lesson07.leroy.spiders.leroy_sp import leroySpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(leroySpider, search="линолеум")
    process.start()

    process.start()
