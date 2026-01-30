import requests
import sys
import logging

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="a", encoding="utf-8", format="%(asctime)s %(levelname)s %(message)s")

# Получить Token
def get_Token():
    with open("TOKEN.txt", "r") as file:
        lines = file.readlines()[0]
        token = lines.split(':')[1].strip()
    return token

# Создание папки с названием породы
def create_folder(path):
    params = {'path': path}
    headers = {'Authorization': TOKEN}
    requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                            params=params,
                            headers=headers)
# Загрузить картинку
def upload_img_breed(path,url):
    params = {
        'path': path,
        'url': url
        }
    headers = {'Authorization': TOKEN}
    requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload',
                            params=params,
                            headers=headers)

 # Получить ссылку
def get_url(request):
     url = request.json()["message"]
     return url

# Получить название картинки
def get_img_name(request):
    img_name = request.json()["message"].split('/')[-1]
    return img_name

TOKEN = get_Token()
base_url = 'https://dog.ceo/api'

breed = input('Введите породу собаки на английском языке: ').strip().lower()
logging.info(f"Введена информация о породе {breed}")


create_folder(f'Backup')
create_folder(f'Backup/{breed}')
logging.info(f"Создана папка {breed} по пути Backup/")

resp1 = requests.get(f'{base_url}/breed/{breed}/images/random')

if resp1.status_code != 200:
    logging.error(resp1.json()["message"])
    sys.exit(resp1.json()["message"])

image_url = get_url(resp1)
logging.info(f"Ссылка на картинку {image_url} породы {breed}")

image_name = get_img_name(resp1)
logging.info(f"Название картинки = {image_name}")

upload_img_breed(f'Backup/{breed}/{breed}_{image_name}',image_url)
logging.info(f"Загружена картинка {breed}_{image_name} на Яндекс Диск")

#под порода
resp2 = requests.get(f'{base_url}/breed/{breed}/list')
sup_breed = get_url(resp2)
logging.info(f"Информация о под-породе(-ах) {sup_breed}")

for sup_b in sup_breed:
    resp3 = requests.get(f'{base_url}/breed/{breed}/{sup_b}/images/random')
    image_breed_url = get_url(resp3)
    logging.info(f"Ссылка на картинку {image_breed_url} под-породы {sup_b}")

    img_sub_name = get_img_name(resp3)

    upload_img_breed(f'Backup/{breed}/{sup_b}_{img_sub_name}',{image_breed_url})
    logging.info(f"Загружена картинка {img_sub_name} на Яндекс Диск под наименованием {sup_b}_{img_sub_name}")


print(f'Проверьте Яндекс Диск по пути Backup/')
logging.info("Конец программы")
sys.exit(0)





