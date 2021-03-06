import requests
import time
import json


def get_data(url_):
    while True:
        time.sleep(1)
        response = requests.get(url_)
        if response.status_code == 200:
            break
    return response.json()


username = 'sunshineuee'
url = 'https://api.github.com/users/' + username + '/repos'

response = get_data(url)
print('Получен результат')
# print(response)

repo = []
for itm in response:
    repo.append(itm['name'])
print(f'Список репозиториев пользователя {username}')
print(repo)

with open('json.json', 'w') as f:
    json.dump(repo, f)
