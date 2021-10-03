import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re
url = 'https://hh.ru/search/vacancy'
headers = {'Accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}
params = {'area': 1, 'fromSearchLine': True, 'st': 'searchVacancy', 'text': 'программист python', 'items_on_page': 100,
          'page': -1}
result = []

def requestsget(url, params, headers):
    global response
    params['page'] += 1
    response = requests.get(url, params=params, headers=headers)
    return response

def salary(dict_, sal):
    if sal != None:
        if sal.text.find('–') != -1:
            dict_['sal_from'], dict_['sal_to'] = re.findall(r'\d+', sal.text.replace('\u202f', ''))
        elif sal.text.find('от') != -1:
            dict_['sal_from'] = re.findall(r'\d+', sal.text.replace('\u202f', ''))[0]
        elif sal.text.find('до') != -1:
            dict_['sal_to'] = re.findall(r'\d+', sal.text.replace('\u202f', ''))[0]
        dict_['cur'] = re.findall(r'\w+', sal.text)[-1]

def parse():
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []
    for vac in soup.findAll('div', attrs={'class': "vacancy-serp-item"}):
        dict_ = {}
        dict_['name'] = vac.find('a', attrs={'data-qa': "vacancy-serp__vacancy-title"}).text
        dict_['href'] = vac.find('a', attrs={'data-qa': "vacancy-serp__vacancy-title"}).get('href')
        salary(dict_,vac.find('span', attrs={'data-qa': "vacancy-serp__vacancy-compensation"}))
        data.append(dict_)
    return data

while requestsget(url, params, headers).status_code == 200:
    result = result + parse()

with open("data.json", "w", encoding="utf-8") as file:
    json.dump(result, file)
data = pd.DataFrame(result)
print(data)
