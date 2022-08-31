import requests
import user_data
import json

from pprint import pprint
from datetime import datetime


class VK:
    """Класс работы с API VK"""

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        """Вывод общей информации о пользователе"""
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_photos(self):
        """Получение фотографий пользователя"""
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': self.id,
            'album_id': 'profile',
            'extended': '1'
        }
        response = requests.get(url, params={**self.params, **params}).json()
        result = self._make_json(response)
        return result

    def _make_json(self, response):

        file_names = []
        result = []
        for item in response['response']['items']:
            file_name = f"{str(item['likes']['count'])}.jpg"
            if file_name in file_names:
                file_name = (
                    f"{str(item['likes']['count'])} "
                    f"{str(datetime.utcfromtimestamp(item['date']).strftime('(%H:%M %d-%m-%Y)'))}.jpg"
                    )
            file_names.append(file_name)
            item_data = {
                "file_name": file_name,
                "size": item['sizes'][-1]['type'],
                "url": item['sizes'][-1]['url']
            }
            result.append(item_data)
        return result

def dump_json(result_json):
    """Записывает результирующий файл со списком фото"""
    with open('res.json', 'w', encoding='utf-8') as file:
        json.dump(result_json, file, indent=4, ensure_ascii=False)


def run():
    vk = VK(user_data.vk_token, user_data.vk_user_id)
    pprint(vk.get_photos())
    # read_json()
    # dump_json(vk.get_photos())


if __name__ == "__main__":
    run()
