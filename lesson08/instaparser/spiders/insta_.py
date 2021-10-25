import scrapy
import re
from scrapy.http import HtmlResponse
import json
import os

from copy import deepcopy
from lesson08.instaparser.items import InstaparserItem

class InstaSpider(scrapy.Spider):
    name = ''
    allowed_domains = ['instagram.com']
    start_urls = ['http://www.instagram.com/']
    inst_login_url = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = ''
    inst_pswd = ''
    parse_users = ['']
    api_url = 'https://i.instagram.com/api/v1/friendships/'

    def parse(self, response):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_url,
            method='POST',
            callback=self.login,
            formdata={'username': self.inst_login,
                      'enc_password': self.inst_pswd},
            headers={'X-CSRFToken': csrf}
        )

    def login(self, response: HtmlResponse):
        for parse_user in self.parse_users:

            j_data = response.json()
            if j_data['authenticated']:
                yield response.follow(
                    f'/{parse_user}',
                    callback=self.parse_followers_data,
                    cb_kwargs={'username': parse_user}
                )

    def parse_followers_data(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        max_id = None
        url_posts = f'{self.api_url}{user_id}/followers/?count=12&search_surface=follow_list_page'

        yield response.follow(url_posts,
                              callback=self.followers_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'max_id': max_id
                                         },
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'}
                              )

    def followers_parse(self, response: HtmlResponse, username, user_id, max_id):
        j_data = response.json()

        page_max_id = j_data.get("next_max_id")
        if j_data.get("next_max_id"):
            max_id = page_max_id

        url_posts = f'{self.api_url}{user_id}/following/?count=12&max_id={max_id}&search_surface=follow_list_page'
        yield response.follow(url_posts,
                              callback=self.followers_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'max_id': deepcopy(max_id)
                                         },
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'}
                              )

        followers = j_data.get('users')
        for i in followers:
            if i['pk'] and i['username']:
                followers_id = i.get('pk')
                followers_username = i.get('username')
                followers_photo = i.get('profile_pic_url')
                item = InstaparserItem(
                    username=username,
                    user_id=user_id,
                    friendships_id=followers_id,
                    friendships_username=followers_username,
                    friendships_photo=followers_photo
                )
                yield item

        # Получаем токен для авторизации

    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

        # Получаем id желаемого пользователя

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')