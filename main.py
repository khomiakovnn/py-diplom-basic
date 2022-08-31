import requests
import user_data
from pprint import pprint


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




def run():
    vk = VK(user_data.vk_token, user_data.vk_user_id)
    pprint(vk.users_info())


if __name__ == "__main__":
    run()
