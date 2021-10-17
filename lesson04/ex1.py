def save_news(news, name_source):
    from pymongo import MongoClient
    client = MongoClient("127.0.0.1", 27017)
    db = client[name_source]
    col = db.news
    res = [col.insert_one(el) for el in news if col.count_documents({"link": el["link"]}) == 0]
    print(col.count_documents({}))
    return res


def get_news_mail():
    import requests
    from lxml import html
    site = "news.mail.ru"
    url = f"https://{site}/"

    header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}
    response = requests.get(url, headers=header)
    root = html.fromstring(response.text)
    result = root.xpath('//td[@class="daynews__main"]/div | //div[@class="daynews__item"] | //ul[@data-module]/li')
    res = []
    for el in result:
        link = el.xpath('.//a/@href')[0]
        response_link = requests.get(link, headers=header)
        dom_news = html.fromstring(response_link.text)
        res.append({"site": site,
                    "source": dom_news.xpath('//span[@class="note"]//span[@class="link__text"]/text()')[0],
                    "name": el.xpath('.//span[@class="photo__captions"]//span[1]/text() | .//a/text()')[0].replace(
                        '\xa0', ' '),
                    "link": el.xpath('.//a/@href')[0],
                    "text": el.text_content(),
                    "time": dom_news.xpath('//span[@class="note"]/span[@datetime]/@datetime')[0]
                    })
    return res


def get_news_yandex():
    import requests
    from lxml import html
    site = "news.yandex.by"
    url = f"https://{site}/"

    header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}
    response = requests.get(url, headers=header)
    root = html.fromstring(response.text)
    result = root.xpath("//article[contains(@class, 'mg-card')]")
    res = [{"site": site,
            "source": el.xpath(".//a[@class = 'mg-card__source-link']/text()"),
            "name": str(el.xpath(".//h2[@class = 'mg-card__title']/text()")).replace("\\xa0", " "),
            "link": el.xpath(".//a[@class = 'mg-card__link']/@href"),
            "text": el.text,
            "time": el.xpath(".//span[@class = 'mg-card-source__time']/text()")
            } for el in result]
    return res


save_news(get_news_mail(), 'mail')
save_news(get_news_yandex(), 'yaru')
