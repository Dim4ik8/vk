import shutil
import requests
from pathlib import Path
import os
from dotenv import load_dotenv
import random


def download_image(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(f"{os.path.join('images', filename)}", 'wb') as file:
        file.write(response.content)


def main():
    load_dotenv()
    token = os.getenv('VK_TOKEN')
    group_id = os.getenv('GROUP_ID_VK')
    Path('images').mkdir(exist_ok=True)
    try:
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

        vk_url = 'https://api.vk.com/method/groups.get'
        params = {'access_token': token, 'v': '5.131'}
        response_vk = requests.get(vk_url, params=params)
        print(response_vk.json())

        vk_url = 'https://api.vk.com/method/photos.getWallUploadServer'
        params = {'access_token': token, 'v': '5.131', 'group_id': group_id}
        response = requests.get(vk_url, params=params)
        upload_url = response.json()['response']['upload_url']
        print(f'Ссылка для загрузки фото: {upload_url}')

        with open(f'images/{num_of_public}.png', 'rb') as file:
            response = requests.post(upload_url, files={'photo': file})
        response.raise_for_status()
        response_for_public = response.json()
        vk_server = response_for_public['server']
        vk_photo = response_for_public['photo']
        vk_hash = response_for_public['hash']

        save_url = 'https://api.vk.com/method/photos.saveWallPhoto'
        params = {
            'access_token': token,
            'v': '5.131',
            'group_id': group_id,
            'photo': vk_photo,
            'server': vk_server,
            'hash': vk_hash
        }
        save_wall_photo = requests.post(save_url, params=params).json()
        print(f'Ответ от saveWallPhoto: {save_wall_photo}')

        owner_id = save_wall_photo['response'][0]['owner_id']
        media_id = save_wall_photo['response'][0]['id']
        attachments = f'photo{owner_id}_{media_id}'
        print(attachments)
        post_url = 'https://api.vk.com/method/wall.post'
        params = {
            'access_token': token,
            'v': '5.131',
            'owner_id': f'-{group_id}',
            'from_group': '1',
            'attachments': attachments,
            'message': message
        }
        print(params)
        requests.post(post_url, params=params)
    finally:
        shutil.rmtree('images')


if __name__ == '__main__':
    main()
