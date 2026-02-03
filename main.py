import logging
import requests
import sys


# Получить Token
def get_token():
    with open('TOKEN.txt', 'r') as file:
        token = file.readlines()[0].split(':')[1].strip()
    return token


# Создание папки с названием породы
def create_folder(path):
    params = {'path': path}
    headers = {'Authorization': MY_TOKEN}
    requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                 params=params,
                 headers=headers)


# Загрузить картинки
def upload_img_breed(path, url):
    params = {
        'path': path,
        'url': url
    }
    headers = {'Authorization': MY_TOKEN}
    requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload',
                  params=params,
                  headers=headers)


# Получить ссылки на картинки
def get_img_url():
    img_urls = []
    response1 = requests.get(f'{BASE_URL}/breed/{breed}/images/random')
    url1 = response1.json()['message']
    img_urls.append(url1)
    response2 = requests.get(f'{BASE_URL}/breed/{breed}/list')
    sup_breeds = response2.json()['message']
    for sup_b in sup_breeds:
        response3 = requests.get(f'{BASE_URL}/breed/{breed}/'
                                 f'{sup_b}/images/random')
        urls = response3.json()['message']
        img_urls.append(urls)
    return img_urls


# Проверка наличия породы
def check_breed(dog):
    response = requests.get(f'{BASE_URL}/breed/{dog}/images/random')
    if response.status_code != 200:
        logging.error(response.json()['message'])
        sys.exit(response.json()['message'])


MY_TOKEN = get_token()
BASE_URL = 'https://dog.ceo/api'

logging.basicConfig(level=logging.INFO,
                    filename='py_log.log',
                    filemode='w',
                    encoding='utf-8',
                    format='%(asctime)s %(levelname)s %(message)s')
create_folder(f'Backup')
logging.info('Создана папка Backup')
breed = input('Введите породу собаки на английском языке: ').strip().lower()
logging.info(f'Введена порода {breed}')
check_breed(breed)
create_folder(f'Backup/{breed}')
logging.info(f'Создана папка Backup/{breed}')
img_urls = get_img_url()
logging.info(f'Получены ссылки на картинки {img_urls}')
for img_u in img_urls:
    img_name = f'{img_u.split('/')[-2]}_{img_u.split('/')[-1]}'
    upload_img_breed(f'Backup/{breed}/{img_name}', img_u)
    logging.info(f'Загружена картинка {img_name} по ссылке {img_u}')
print(f'Проверьте Яндекс Диск по пути https://disk.yandex.ru/d/OXF5XyKWSykOKg')
logging.info('Конец программы')
sys.exit(0)