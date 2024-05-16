import os

import yadisk
from db_functions import DB_get_user_by_telegram_id, DB_add_image_to_list

YADISK_TOKEN = ""
BIRDS_FOLDER = "/birds/"


def check_if_image_name_non_downloaded(tg_user, image_path):
   # проверка скачивал ли пользователь изображение до
   images = DB_get_user_by_telegram_id(telegram_id=tg_user)[0][1]
   if image_path not in images:
       return True
   return False

        
def get_last_non_downloaded_user_image_url(tg_user):
   # получение последнего нескаченного изображения пользователем с Яндекс Диска. С последующей записью названия изображения в бд
   disk = yadisk.YaDisk(token=YADISK_TOKEN)
   photos = list(disk.listdir(BIRDS_FOLDER))
   photos = sorted(photos, key=lambda file: file["created"], reverse=True)
   for photo in photos:
       if check_if_image_name_non_downloaded(tg_user, photo["name"]) == True:
           DB_add_image_to_list(tg_user, photo["name"])
           return photo
       

def delete_download_image_from_server(path):
   # удаление изображения с сервера
   os.remove(path)

def if_equal_images_in_db_with_yadisk(tg_user):
   # проверка: скачал ли пользователь все изображения с Яндекс Диска
   disk = yadisk.YaDisk(token=YADISK_TOKEN)
   number_of_photos_in_yadisk = len(list(disk.listdir(BIRDS_FOLDER)))
   number_of_user_images_in_db = len(DB_get_user_by_telegram_id(telegram_id=tg_user)[0][1].split(' '))
   if number_of_photos_in_yadisk == number_of_user_images_in_db:
       return True
   return False