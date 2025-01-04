# 2 Задание: построить осмысленную колизию: 
# Есть две картинки: Заяц и Волк
# Берём картинку Волка - считаем hash
# Берём картинку зайца и аккрутно меняем пиксили, R компоненту - подбираем, чтобы hash совпал с волком

# pip install pillow

from streebog_hash import Streebog
import json
import random
import os
#os.chdir('./Лаба 1 Стрибог')
from PIL import Image

gost = Streebog()

msb_count = 1



# bytes_array = [x for x in img_volk.tobytes()]
# hash gost.GetHash(bytes_array)
def _compare_images(img1: Image, img2: Image) -> bool:
    """
    Не знаю реализацию сравнения внутри библиотеки, поэтому реализую свою, буду сравнить все пиксели
    если их 2^12, то сравним за сек, а сравнения редкие, поэтому норм
    """
    w, h = img1.size
    for x in range(w):
        for y in range(h):
            if img1.getpixel((x, y)) != img2.getpixel((x, y)):
                return False
    return True


def task_2():
    dir_path = './Task2/РезультатыПодбораКандидатов'
    colision_infos = []
    colision_infos_path = f"{dir_path}/colision_infos_volk.json"
    if os.path.exists(colision_infos_path):
        with open(colision_infos_path) as f:
            text = f.read()
            colision_infos = json.loads(text) if text else []
    
    # Волк
    # О том, как менять попиксельно цвета: https://dzen.ru/a/ZQflhWPa9FulHAYi
    volk_file = "./Task2/Волк_64.jpg"
    img_volk = Image.open(volk_file).convert('RGB')
    bytes_array = [x for x in img_volk.tobytes()]

    # Заяц
    zais_file = "./Task2/Заяц_64.jpg"
    img_zais_base = Image.open(zais_file).convert('RGB')

    img_zais_applicant = img_zais_base.copy()

    # n - число бит
    cur_n = max([x["n"] for x in colision_infos]) if colision_infos else 0
    max_n = 40 #
    gost = Streebog()
    for i in range(cur_n + 1, max_n):
        cur = 0
        # Эталонный хэш
        base_hash = gost.GetHash(bytes_array, i)
        while True:   
            x = random.randint(0,63)
            y = random.randint(0,63)
            # случайно сдвигаем один из пикселей на чуть-чуть по R
            res = [1,-1][random.randint(0,1)]
            
            cur_color = img_zais_applicant.getpixel((x,y))
            # Меняем R компоненту цвета
            cur_color = ((cur_color[0] + res) % 256, cur_color[1], cur_color[2])
            
            img_zais_applicant.putpixel((x,y), cur_color)

            applicant_hash = gost.GetHash([x for x in img_zais_applicant.tobytes()], i)
            
            # хэши совпали(Реализовал своё сравнение, попиксельно, тк нет уверенности во внутренней реализации)
            # if base_hash == applicant_hash and img_zais_applicant != img_zais_base: 
            if base_hash == applicant_hash and not _compare_images(img_zais_applicant, img_zais_base):
                print(f'{i}й найден')
                colision_infos.append({
                    "n": i,
                    "needed_check_count": cur+1,
                    "base_hash": base_hash,
                    "applicant_hash": applicant_hash
                })

                # Обновляем файл с результатами
                with open(colision_infos_path, "w") as f:
                    f.write(json.dumps(colision_infos))

                # Дополнительно сохраним сами изображения
                image_saved_dir_path = f'{dir_path}/{i}'
                os.makedirs(image_saved_dir_path, exist_ok=True)

                img_zais_applicant.save(f'{image_saved_dir_path}/applicant_volk.jpg')
                img_zais_base.save(f'{image_saved_dir_path}/base.jpg')
                img_volk.save(f'{image_saved_dir_path}/volk.jpg')
                break
            cur += 1 # переходим дальше
