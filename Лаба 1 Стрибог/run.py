from streebog_hash import *
import json
import random
import os
from run_2 import task_2

# message = [
#     0x32,0x31,0x30,0x39,0x38,0x37,0x36,0x35,0x34,0x33,0x32,0x31,0x30,0x39,0x38,0x37,
#     0x36,0x35,0x34,0x33,0x32,0x31,0x30,0x39,0x38,0x37,0x36,0x35,0x34,0x33,0x32,0x31,
#     0x30,0x39,0x38,0x37,0x36,0x35,0x34,0x33,0x32,0x31,0x30,0x39,0x38,0x37,0x36,0x35,
#     0x34,0x33,0x32,0x31,0x30,0x39,0x38,0x37,0x36,0x35,0x34,0x33,0x32,0x31,0x30]

# gost512 = Streebog(512)
# gost256 = Streebog(256)

# res512 = gost512.GetHash(message)
# res256 = gost256.GetHash(message)

# print(f"ГОСТ 512: {res512}")
# print(f"ГОСТ 256: {res256}")

# Задача 1: Построение коллизий:
# {n:int, needed_check_count: int, final: bit_str, success_applicant: bit_str, hash: str}
def task_1():
    colision_infos = []
    file_path = "colision_infos.json"
    if os.path.exists(file_path):
        with open(file_path) as f:
            text = f.read()
            colision_infos = json.loads(text) if text else []

    def get_random_512():
        """
        Генерирует рандомно 512 бит
        """
        return ''.join([str(random.randint(0,1)) for x in range(512)])
    # эталон
    final = get_random_512() 

    # n - число бит
    cur_n = max([x["n"] for x in colision_infos]) if colision_infos else 0
    max_n = 40 #
    gost = Streebog()
    for i in range(cur_n + 1, max_n):
        cur = 0
        final_hash = gost.GetHashByBits(final, i)
        while True:
            # Этот вариант показал, что достаточно медленный
            #applicant = bin(cur)[2:]
            applicant = get_random_512()
            # Дополнили нулями, чтобы сравнение final != applicant было корректно
            # applicant = '0'*(512-i) + applicant
            applicant_hash = gost.GetHashByBits(applicant, i)
            # хэши совпали
            if final_hash == applicant_hash and final != applicant:
                print(f'{i}й найден')
                colision_infos.append({
                    "n": i,
                    "needed_check_count": cur+1,
                    "final": final,
                    "success_applicant": applicant,
                    "hash": applicant_hash
                })

                # Обновляем файл с результатами
                with open(file_path, "w") as f:
                    f.write(json.dumps(colision_infos))
                break
            cur += 1 # переходим дальше

# task_1()

task_2()