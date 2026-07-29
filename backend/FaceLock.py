#Готовая версия
from deepface import DeepFace
import cv2
import time
import datetime
import os
import sys
import numpy as np
from scipy.spatial.distance import cosine
import pickle
import Quartz
from funct import lock_screen
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import THRESHOLD, DB_PATH, IMAGE_DIR, MODEL_NAME, NAME_FOLDER_BLOCK_USERS


base_embeddings = []
# Проверка наличи существования базы embeddings
if os.path.exists(DB_PATH) and os.path.getsize(DB_PATH) > 0:
    print('База embeddings найдена')
    try:
        with open(DB_PATH, 'rb') as f:
            base_embeddings = pickle.load(f)
        print(f'Успешно загруженно {len(base_embeddings)} записей')
    except Exception as e:
        print(f'Ошибка чтения базы ({e})')
        base_embeddings = []

# Постройка базы
if not base_embeddings:
    print('Создание базы')
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(IMAGE_DIR, exist_ok=True)

    for file in os.listdir(IMAGE_DIR):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(IMAGE_DIR, file)
            try:
                result = DeepFace.represent(img_path=path, model_name=MODEL_NAME)
                embedding = np.array(result[0]['embedding']).flatten()
                base_embeddings.append(embedding)
                print(f' + Обработано: {file}')
            except Exception as e:
                print(f' - Пропущено {file}: {e}')

    with open(DB_PATH, 'wb') as f:
        pickle.dump(base_embeddings, f)
    print(f'База сохранена, всего лиц {len(base_embeddings)}')

if not base_embeddings:
    print('Загрузите лица в папку')
    exit()


cap = cv2.VideoCapture(0)

while True:
    indicator_lock_screem = Quartz.CGSessionCopyCurrentDictionary()
    if indicator_lock_screem and indicator_lock_screem.get('CGSSessionScreenIsLocked', 0) == 1:
        time.sleep(5)
        continue
    else:
        time.sleep(1)
        ret, frame = cap.read()
        if not ret:
            continue
        # Сравнение лиц
        try:
            rep = DeepFace.represent(img_path=frame, enforce_detection=True, model_name=MODEL_NAME)
            cam_embedding = np.array(rep[0]["embedding"]).flatten()

            distance = [cosine(cam_embedding, known_emb) for known_emb in base_embeddings]
            min_distance = min(distance)
        
            if min_distance < THRESHOLD:
                print("Это тот же человек")
            else:
                print("Это другой человек")
                lock_screen()

                timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                source_file = f'block_user_{timestamp}.jpg'
                destination_folder = NAME_FOLDER_BLOCK_USERS
                os.makedirs(destination_folder, exist_ok=True)
                destination_path = os.path.join(destination_folder, source_file)
                cv2.imwrite(destination_path, frame)
        except Exception as e:
            print(f"Ошибка распознавания: {e}")