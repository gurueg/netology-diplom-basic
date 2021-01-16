import requests


class YaDiskUploader:
    url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token: str):
        self.token = token

    def upload_file_from_url(self, url: str, filename: str, foldername: str):
        response = requests.get(
            self.url,
            params={
                'path': f'{foldername}'
            },
            headers={
                'Authorization': f'OAuth {self.token}'
            }
        )

        if response.status_code == 404:
            response = requests.put(
                self.url,
                params={
                    'path': f'{foldername}'
                },
                headers={
                    'Authorization': f'OAuth {self.token}'
                }
            )
            response.raise_for_status()
        else:
            response.raise_for_status()

        upload_response = requests.post(
            self.url + '/upload',
            params={
                'path': f'{foldername}/{filename}',
                'url': url
            },
            headers={
                'Authorization': f'OAuth {self.token}'
            }
        )

        href_operation = upload_response.json()['href']
        return href_operation

    def check_operation_ended(self, operation_href):
        operation_ended = False
        operation_result = requests.get(
            operation_href,
            headers={
                'Authorization': f'OAuth {self.token}'
            }
        )
        operation_result.raise_for_status()
        if operation_result.json()['status'] == 'success':
            operation_ended = True

        return operation_ended

    def is_token_exists(self):
        response = requests.get(
            'https://cloud-api.yandex.net/v1/disk',
            headers={
                'Authorization': f'OAuth {self.token}'
            }
        )
        if response.status_code == 401:
            return False
        return True


if __name__ == '__main__':
    uploader = YaDiskUploader('')
    print(uploader.check_token_exists())
    # print('Done')
