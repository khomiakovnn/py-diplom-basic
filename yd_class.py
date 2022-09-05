import requests


class YD:
    """Класс работы с API ЯндексДиск"""

    def __init__(self, access_token):
        self.token = access_token

    def make_directory(self, path):
        """Создает директорию для загрузки файлов"""
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Authorization': f'OAuth {self.token}'}
        params = {'path': path}
        response = requests.put(url, headers=headers, params=params)
        if response.status_code == 201:
            print(f"Директория '{path}' на Яндекc.Диск создана")
        elif response.status_code == 401:
            print('Ошибка авторизации. Проверьте OAuth токен ЯндекcДиск')
        elif response.status_code == 409:
            print(f"Директория '{path}' на Яндекc.Диск уже существует")
        elif response.status_code == 423:
            print("Технические работы. Сейчас можно только просматривать и скачивать файлы.")
        elif response.status_code == 503:
            print("Сервис временно недоступен.")

    def upload(self, path, files):
        """Upload file from path to Yandex.Disk"""
        for file in files:
            # Receive link for upload
            file_path = f'{path}/{file["file_name"]}'
            url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
            headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}
            params = {"path": file_path, "overwrite": "true"}
            href = requests.get(url, headers=headers, params=params).json()['href']
            # print(file['url'])
            # Upload file from file path
            data = requests.get(file["url"]).content
            response = requests.put(href, data=data)
            if response.status_code == 201:
                print(f"Файл '{file['file_name']}' записан")
        print(f"Записано '{len(files)}' файлов в папку '{path}'")
