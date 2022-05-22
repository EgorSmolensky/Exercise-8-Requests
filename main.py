import requests
import os
from pprint import pprint
from datetime import timedelta, datetime

# Задача 1
print('Задача 1')


def search_id(name):
    search_url = 'https://superheroapi.com/api/2619421814940190/search/' + name
    response = requests.get(search_url)
    info = response.json()
    return info['results'][0]['id']


def get_intelligence(id):
    id_url = 'https://superheroapi.com/api/2619421814940190/' + id + '/powerstats/'
    response = requests.get(id_url)
    stats = response.json()
    return stats['intelligence']


if __name__ == '__main__':
    superheroes = ['Hulk', 'Captain America', 'Thanos']
    hero_intelligence = dict()

    print(f'Incoming list: {", ".join(superheroes)}')
    print('plese, wait...')
    for hero in superheroes:
        intelligence = get_intelligence(search_id(hero))
        hero_intelligence[int(intelligence)] = hero

    intelligenece = max(hero_intelligence)
    heroname = hero_intelligence[intelligenece]

    print(f'{heroname} is the cleverest hero from list. His intelligence is {intelligenece}')

# Задача 2
print('\n' * 2)
print('Задача 2')


class YaUploader:

    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload(self, file_path: str):
        file_name = os.path.basename(file_path)
        url = self._get_upload_link(disk_file_path=file_name).get('href', '')
        response = requests.put(url, data=open(file_path, 'rb'))
        if response.status_code == 201:
            return "Success"
        return 'Печалька'


if __name__ == '__main__':
    path_to_file = input('Введите полный путь до файла: ')
    my_token = 'my_token'
    uploader = YaUploader(my_token)
    result = uploader.upload(path_to_file)
    pprint(result)

# Задача 3
print('\n' * 2)
print('Задача 3')


def search_for_tag(tag):
    finish_date = datetime.now()
    finish_date = datetime(finish_date.year, finish_date.month, finish_date.day, 0, 0, 0)
    finish_date += timedelta(hours=7)       # Поправка на мой текущий часовой пояс
    start_date = finish_date - timedelta(days=1)

    finish_date = str(finish_date.timestamp())[:-2]
    start_date = str(start_date.timestamp())[:-2]
    tag_url = f'https://api.stackexchange.com/2.3/questions?fromdate={start_date}&todate={finish_date}&order=desc&sort=activity&tagged={tag}&site=stackoverflow'
    response = requests.get(tag_url)
    info = response.json()
    return info


if __name__ == '__main__':
    pprint(search_for_tag('Python'))