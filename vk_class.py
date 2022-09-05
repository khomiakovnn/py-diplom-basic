import requests
from datetime import datetime


class VK:
    """Класс работы с API VK"""

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        """Вывод ФИО"""
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params}).json()
        result = f"{response['response'][0]['last_name']} {response['response'][0]['first_name']}"
        return result

    def get_photos(self, max_photo=5):
        """Получение фотографий пользователя"""
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': self.id,
            'album_id': 'profile',
            'extended': '1'
        }
        response = requests.get(url, params={**self.params, **params})
        result = self._make_json(response.json(), max_photo)
        return result

    def _make_json(self, response, max_photo):
        """Формирование словаря json (фильтр данных)"""
        file_names = []
        result = []
        for n, item in enumerate(response['response']['items'], start=1):
            if n > max_photo != 0:
                break
            file_name = f"{str(item['likes']['count'])}.jpg"
            if file_name in file_names:
                file_name = (
                    f"{str(item['likes']['count'])} "
                    f"{str(datetime.utcfromtimestamp(item['date']).strftime('(%H-%M %d-%m-%Y)'))}.jpg"
                )
            file_names.append(file_name)
            item_data = {
                "file_name": file_name,
                "size": item['sizes'][-1]['type'],
                "url": item['sizes'][-1]['url']
            }
            result.append(item_data)
        return result
