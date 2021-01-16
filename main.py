from vkUser import vkUser
from yaDiskUploader import YaDiskUploader
from pprint import pprint
from progress.bar import IncrementalBar
from datetime import date
import json


def get_max_photo_data(sizes_array):
    sizes = {'s': 1, 'm': 2, 'x': 3,
             'o': 4, 'p': 5, 'q': 6,
             'r': 7, 'y': 8, 'z': 9, 'w': 1
             }

    sizes_array.sort(key=lambda item: sizes[item['type']])
    return sizes_array[-1]


def main():

    user_id = input('Введите id пользователя вКонтакте: ')
    new_user = vkUser(user_id)
    if not new_user.is_user_exists():
        print('Пользователя с таким id не существует')
        return

    ya_token = input('Введите токен для yaAPI: ')

    uploader = YaDiskUploader(ya_token)
    if not uploader.is_token_exists():
        print('Несуществующий токен Я.диска')
        return

    is_from_all = input('Сохранять фотографии из всех альбомов?(y/n): ')
    if is_from_all == 'y':
        photos_list = new_user.get_user_all_photos()
    else:
        photos_list = new_user.get_user_profile_photos()

    likes_dict = {}
    for photo in photos_list:
        likes_count = str(photo['likes']['count'])
        if likes_count in likes_dict.keys():
            likes_dict[likes_count] += 1
        else:
            likes_dict[likes_count] = 1

    bar = IncrementalBar(
        max=len(photos_list),
        message='Загрузка'
    )

    json_list = []
    operations_list = []

    for photo in photos_list:
        file_name = str(photo['likes']['count'])
        if likes_dict[file_name] > 1:
            file_name += '_' + str(date.fromtimestamp(photo['date']))

        size_data = get_max_photo_data(photo['sizes'])
        file_url = size_data['url']
        file_format = file_url.split('?')[0].split('.')[-1]

        file_name += file_format
        operation_href = uploader.upload_file_from_url(
            file_url,
            file_name,
            'FromVkUploader'
        )
        operations_list.append(operation_href)
        json_list.append({'file_name': file_name, 'size': size_data['type']})

    operations_done = []
    while(len(operations_done) != len(operations_list)):
        for operation in operations_list:
            if operation not in operations_done:
                if uploader.check_operation_ended(operation):
                    operations_done.append(operation)
                    bar.next()
    bar.finish()

    with open('result.json', 'w', encoding='utf-8') as result_file:
        json.dump(json_list, result_file, ensure_ascii=True, indent=4)

    print('Работа программы завершена')


if __name__ == '__main__':
    main()
