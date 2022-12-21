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


def get_upload_url(token, group_id):
    vk_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {'access_token': token, 'v': '5.131', 'group_id': group_id}
    response = requests.get(vk_url, params=params)
    response.raise_for_status()
    decoded_response = response.json()
    if 'error' in decoded_response:
        raise requests.exceptions.HTTPError(decoded_response['error'])
    upload_url = decoded_response['response']['upload_url']
    return upload_url


def upload_image_to_vk_server(upload_url, image):
    with open(image, 'rb') as file:
        response = requests.post(upload_url, files={'photo': file})
    response.raise_for_status()
    response_for_posting = response.json()
    if 'error' in response_for_posting:
        raise requests.exceptions.HTTPError(response_for_posting['error'])

    vk_server = response_for_posting['server'],
    vk_photo = response_for_posting['photo'],
    vk_hash = response_for_posting['hash']

    return vk_server, vk_photo, vk_hash


def save_image(token, group_id, server, photo, hash):
    url_for_saving = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token': token,
        'v': '5.131',
        'group_id': group_id,
        'photo': photo,
        'server': server,
        'hash': hash
    }
    response = requests.post(url_for_saving, params=params)
    response.raise_for_status()
    saved_photo = response.json()
    if 'error' in saved_photo:
        raise requests.exceptions.HTTPError(saved_photo['error'])
    owner_id = saved_photo['response'][0]['owner_id']
    media_id = saved_photo['response'][0]['id']
    attachments = f'photo{owner_id}_{media_id}'
    return attachments


def publish_post_to_vk_wall(token, group_id, attachments, text):
    url_for_posting = 'https://api.vk.com/method/wall.post'
    params = {
        'access_token': token,
        'v': '5.131',
        'owner_id': f'-{group_id}',
        'from_group': '1',
        'attachments': attachments,
        'message': text
    }
    response = requests.post(url_for_posting, params=params)
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
        publication_number = random.randint(1, total_comics)
        url = f'https://xkcd.com/{publication_number}/info.0.json'
        comic_book, message = get_comic_book(url)
        download_image(comic_book['img'], f'{publication_number}.png')
        image_for_posting = os.path.join('images', f'{publication_number}.png')

        upload_url = get_upload_url(token, group_id)

        server, photo, hash = upload_image_to_vk_server(upload_url, image_for_posting)

        attachments = save_image(token, group_id, server, photo, hash)

        publish_post_to_vk_wall(token, group_id, attachments, message)

    except requests.exceptions.HTTPError as error:
        logging.error(f'Ошибка сервера: {error}')
    finally:
        shutil.rmtree('images')


if __name__ == '__main__':
    main()
