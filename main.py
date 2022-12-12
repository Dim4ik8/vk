import shutil
import time
import requests
from pathlib import Path
import os
from dotenv import load_dotenv
import random


def download_image(url, filename, folder='images'):
    response = requests.get(url)
    response.raise_for_status()
    Path(folder).mkdir(exist_ok=True)
    with open(f'{os.path.join(folder, filename)}', 'wb') as file:
        file.write(response.content)


def main():
    load_dotenv()
    token = os.getenv('VK_TOKEN')
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic_book = response.json()
    message = comic_book['alt']
    print(f"Комментарий к комиксу: {message}")

    download_image(comic_book['img'], 'image.png')

    total_comics = comic_book['num']
    num_of_public = random.randint(1, total_comics)
    url = f'https://xkcd.com/{num_of_public}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic_book = response.json()
    message = comic_book['alt']
    print(f"Комментарий к комиксу: {message}")
    download_image(comic_book['img'], f'{num_of_public}.png')

    url_vk = 'https://api.vk.com/method/groups.get'
    params = {'access_token': token, 'v': '5.131'}
    response_vk = requests.get(url_vk, params=params)
    print(response_vk.json())

    url_vk = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {'access_token': token, 'v': '5.131', 'group_id': '217553308'}
    response = requests.get(url_vk, params=params)
    upload_url = response.json()['response']['upload_url']
    print(f'Ссылка для загрузки фото: {upload_url}')

    with open(f'images/{num_of_public}.png', 'rb') as file:
        response = requests.post(upload_url, files={'photo': file})
        response.raise_for_status()
        server = response.json()['server']
        photo = response.json()['photo']
        hash = response.json()['hash']

    url_save = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token': token,
        'v': '5.131',
        'group_id': '217553308',
        'photo': photo,
        'server': server,
        'hash': hash
    }
    save_wall_photo = requests.post(url_save, params=params).json()
    print(f'Ответ от saveWallPhoto: {save_wall_photo}')

    owner_id = save_wall_photo['response'][0]['owner_id']
    media_id = save_wall_photo['response'][0]['id']
    attachments = f'photo{owner_id}_{media_id}'
    print(attachments)
    url_post = 'https://api.vk.com/method/wall.post'
    params = {
        'access_token': token,
        'v': '5.131',
        'owner_id': '-217553308',
        'from_group': '1',
        'attachments': attachments,
        'message': message
    }

    requests.post(url_post, params=params)
    time.sleep(5)
    shutil.rmtree('images')


if __name__ == '__main__':
    main()
