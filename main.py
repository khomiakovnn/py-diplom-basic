import user_data
import json
from vk_class import VK
from yd_class import YD


def dump_json(result_json):
    """Форматирует словарь и записывает результирующий файл со списком фото"""
    for i in result_json:
        del i['url']
    with open('res.json', 'w', encoding='utf-8') as file:
        json.dump(result_json, file, indent=4, ensure_ascii=False)
    print('Файл res.json создан')


def run():
    vk = VK(user_data.vk_token, user_data.vk_user_id)
    json_data = vk.get_photos()
    path = f'{vk.users_info()} VK фото'
    yd = YD(user_data.yd_token)
    yd.make_directory(path)
    yd.upload(path, json_data)
    dump_json(json_data)


if __name__ == "__main__":
    run()
