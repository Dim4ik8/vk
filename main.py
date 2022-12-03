import requests

url = 'https://xkcd.com/info.0.json'


def main():
    response = requests.get(url)
    response.raise_for_status()

    comic_book = response.json()
    print(comic_book)

if __name__ == '__main__':
    main()