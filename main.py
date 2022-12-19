import logging
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


def get_comic_book(url):
    response = requests.get(url)
    response.raise_for_status()
    comic_book = response.json()
    if 'error' in comic_book:
        raise requests.exceptions.HTTPError(comic_book['error'])
    message = comic_book['alt']
    return comic_book, message


def publish_post_to_vk_wall(token, group_id, image, text):
    vk_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {'access_token': token, 'v': '5.131', 'group_id': group_id}
    response = requests.get(vk_url, params=params)
    response.raise_for_status()
    decoded_response = response.json()
    if 'error' in decoded_response:
        raise requests.exceptions.HTTPError(decoded_response['error'])
    upload_url = decoded_response['response']['upload_url']

    with open(image, 'rb') as file:
        response = requests.post(upload_url, files={'photo': file})
    response.raise_for_status()
    response_for_public = response.json()
    if 'error' in response_for_public:
        raise requests.exceptions.HTTPError(response_for_public['error'])
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
    response = requests.post(save_url, params=params)
    response.raise_for_status()
    save_wall_photo = response.json()
    if 'error' in save_wall_photo:
        raise requests.exceptions.HTTPError(save_wall_photo['error'])
    owner_id = save_wall_photo['response'][0]['owner_id']
    media_id = save_wall_photo['response'][0]['id']
    attachments = f'photo{owner_id}_{media_id}'
    post_url = 'https://api.vk.com/method/wall.post'
    params = {
        'access_token': token,
        'v': '5.131',
        'owner_id': f'-{group_id}',
        'from_group': '1',
        'attachments': attachments,
        'message': text
    }
    response = requests.post(post_url, params=params)
    response.raise_for_status()


def main():
    load_dotenv()
    token = os.getenv('VK_TOKEN')
    group_id = os.getenv('GROUP_ID_VK')
    Path('images').mkdir(exist_ok=True)
    try:
        url = 'https://xkcd.com/info.0.json'
        comic_book, message = get_comic_book(url)

        total_comics = comic_book['num']
        num_of_public = random.randint(1, total_comics)
        url = f'https://xkcd.com/{num_of_public}/info.0.json'
        comic_book, message = get_comic_book(url)
        download_image(comic_book['img'], f'{num_of_public}.png')
        image_for_public = os.path.join('images', f'{num_of_public}.png')

        publish_post_to_vk_wall(token, group_id, image_for_public, message)
    except requests.exceptions.HTTPError as error:
        logging.error(f'Ошибка сервера: {error}')
    finally:
        shutil.rmtree('images')


if __name__ == '__main__':
    main()
