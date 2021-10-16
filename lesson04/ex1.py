def save_news(news):
    from pymongo import MongoClient
    client = MongoClient("127.0.0.1", 27017)
    db = client["news_bd"]
    col = db.news
    res = [col.insert_one(el) for el in news if col.count_documents({"href": el["href"]}) == 0]
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
    result = root.xpath('//div[@class="daynews__item"]/a | //li/a | //li/span/a')
    res = [{"site": site,
            "text": el.text_content(),
            "href": el.attrib["href"]
            } for el in result]
    return res


def get_news_yandex():
    import requests
    from lxml import html
    site = "news.yandex.by"
    url = f"https://{site}/"

    header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}
    response = requests.get(url, headers=header)
    root = html.fromstring(response.text)
    result = root.xpath('//h2[@class="mg-card__title"]')
    res = [{"site": site,
            "text": el.text,
            "href": el.getparent().attrib["href"]
            } for el in result]
    return res


#save_news(get_news_mail())
#save_news(get_news_yandex())
