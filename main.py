import requests
import sys
import logging

print('ВНИМАНИЕ! ВЕДЕТСЯ ЛОГИРОВАНИЕ')
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="a", encoding="utf-8", format="%(asctime)s %(levelname)s %(message)s")

def get_Token():
    with open("TOKEN.txt", "r") as file:
        lines = file.readlines()[0]
        token = lines.split(':')[1].strip()
    return token

TOKEN = get_Token()
base_url = 'https://dog.ceo/api/breed'

breed = input('Введите породу собаки на английском языке: ').strip().lower()
logging.info(f"Введена информация о породе {breed}")

url = f'{base_url}/{breed}/images/random'
response = requests.get(url)

if response.status_code != 200:
    logging.error(response.json()["message"])
    sys.exit(response.json()["message"])

# Создание папки с названием породы
def create_folder(path):
    params = {'path': path}
    headers = {'Authorization': TOKEN}
    response = requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                            params=params,
                            headers=headers)

create_folder(f'Backup')
create_folder(f'Backup/{breed}')
logging.info(f"Создана папка {breed} по пути Backup/")

image_url = response.json()["message"]
logging.info(f"Ссылка на картинку {image_url} породы {breed}")

image_name = image_url.split('/')[-1]
logging.info(f"Название картинки = {image_name}")

def upload_img_breed(path,url):
    params = {
        'path': path,
        'url': url
        }
    headers = {'Authorization': TOKEN}
    response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload',
                            params=params,
                            headers=headers)

upload_img_breed(f'Backup/{breed}/{breed}_{image_name}',image_url)
logging.info(f"Загружена картинка {breed}_{image_name} на Яндекс Диск")

#под порода
url_sub = f'{base_url}/{breed}/list'
response = requests.get(url_sub)
sup_breed = response.json()["message"]
logging.info(f"Информация о под-породе(-ах) {sup_breed}")

for sup_b in sup_breed:
    url = f'{base_url}/{breed}/{sup_b}/images/random'
    response = requests.get(url)
    image_breed_url = response.json()["message"]
    logging.info(f"Ссылка на картинку {image_breed_url} под-породы {sup_b}")

    img_sub_name = image_breed_url.split('/')[-1]

    upload_img_breed(f'Backup/{breed}/{sup_b}_{img_sub_name}',{image_breed_url})
    logging.info(f"Загружена картинка {img_sub_name} на Яндекс Диск под наименованием {sup_b}_{img_sub_name}")

print(f'Проверьте Яндекс Диск по пути Backup/{breed}')
logging.info("Конец программы")
sys.exit(0)





