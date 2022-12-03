import requests
from pathlib import Path
import os

url = 'https://xkcd.com/info.0.json'

def download_image(url, filename, folder='images'):
    response = requests.get(url)
    response.raise_for_status()
    Path(folder).mkdir(exist_ok=True)
    with open(f'{os.path.join(folder, filename)}', 'wb') as file:
        file.write(response.content)

def main():
    response = requests.get(url)
    response.raise_for_status()

    comic_book = response.json()
    print(comic_book['alt'])


if __name__ == '__main__':
    main()