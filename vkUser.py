import requests
import json
import time
from pprint import pprint

with open('settings.json') as f:
    json_data = json.load(f)

VERSION = json_data['version']
TOKEN = json_data['token']


class vkUser():
    url = 'https://api.vk.com/method/'
    version = VERSION
    token = TOKEN

    def __init__(self, user_id):
        self.user_id = user_id
        self.params = {
            'access_token': self.token,
            'v': self.version
        }

    def __send_request(self, url, params):
        repeat = True
        while repeat:
            response = requests.get(url, params).json()
            if 'error' in response and 'error_code' in response['error'] and \
                    response['error']['error_code'] == 6:
                time.sleep(0.3)
            else:
                repeat = False

        if 'error' in response:
            response['response'] = None

        return response['response']

    def is_user_exists(self):
        url = self.url+'users.get'
        request_params = {
            **self.params,
            'user_ids': self.user_id
        }
        response = self.__send_request(url, request_params)
        return response is not None

    def get_user_data(self):
        request_params = {**self.params, 'user_ids': [self.user_id]}

        return self.__send_request(self.url+'users.get', request_params)[0]

    def get_user_photos_from_album(self, album_id='profile', count=5):
        url = self.url+'photos.get'
        request_params = {
            **self.params,
            'owner_id': self.user_id,
            'album_id': album_id,
            'extended': True,
            'photo_sizes': True,
            'rev': 1,
            'count': count
        }
        return self.__send_request(url, request_params)

    def get_user_profile_photos(self, count=5):
        return self.get_user_photos_from_album()['items']

    def get_user_all_photos(self):
        url = self.url+'photos.getAlbums'
        request_params = {
            **self.params,
            'owner_id': self.user_id,
            'need_system': 1
        }
        albums_data = self.__send_request(url, request_params)['items']
        # pprint(albums_data)

        all_photos = []
        for album in albums_data:
            result = self.get_user_photos_from_album(album_id=album['id'])
            all_photos += result['items']

        return all_photos


def main():
    user1 = vkUser(34604696)

    pprint(user1.get_user_all_photos())

    # pprint(user1.get_user_all_photos())
    # user2 = vkUser(95323557)


if __name__ == '__main__':
    main()
