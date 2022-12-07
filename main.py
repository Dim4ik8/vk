import requests
from pathlib import Path
import os
from dotenv import load_dotenv

def download_image(url, filename, folder='images'):
    response = requests.get(url)
    response.raise_for_status()
    Path(folder).mkdir(exist_ok=True)
    with open(f'{os.path.join(folder, filename)}', 'wb') as file:
        file.write(response.content)

def main():
    load_dotenv()
    token = os.getenv('VK_TOKEN')
    # обращаемся к комиксу и выводим в консоль его комментарий
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic_book = response.json()
    print(comic_book['alt'])
    download_image(comic_book['img'], 'image.png')

    # обращаемся к API VK, выводим информацию о группах
    # url_vk = 'https://api.vk.com/method/groups.get'
    # params = {'access_token': token, 'v': '5.131'}
    # response_vk = requests.get(url_vk, params=params)
    # print(response_vk.json())

    # обращаемся для получения адреса для загрузки картинки
    url_vk = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {'access_token': token, 'v': '5.131', 'group_id': '217553308'}
    response = requests.get(url_vk, params=params)
    print(response.json())
    upload_url = response.json()['response']['upload_url']
    print(upload_url)

    with open('images/image.png', 'rb') as file:
        url = upload_url
        photo = {
            'media': file,
            }
        response = requests.post(url, data=photo)
        response.raise_for_status()
        print(response.json())



if __name__ == '__main__':
    main()