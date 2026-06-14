#Готовая версия

from deepface import DeepFace
import cv2
import time
import os
import numpy as np
from scipy.spatial.distance import cosine
import ctypes
import pickle
import shutil


img_from_cam = "my_photo.jpg"
THRESHOLD = 0.3
DB_PATH = "backend/embeddings.pkl"
IMAGE_DIR = "data/know_face"

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
        if file.lower().endswith(('.png', '.jpg', 'jpeg')):
            path = os.path.join(IMAGE_DIR, file)
            try:
                result = DeepFace.represent(img_path=path, model_name='Facenet512')
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



with open(DB_PATH, 'wb') as f:
    pickle.dump(base_embeddings, f)

cap = cv2.VideoCapture(0)

while True:
    time.sleep(1)
    ret, frame = cap.read()
    if not ret:
        continue
    cv2.imwrite(img_from_cam, frame)
    # Сравнение лиц
    try:
        rep = DeepFace.represent(img_path=img_from_cam, enforce_detection=True)
        cam_embedding = np.array(rep[0]["embedding"])

        distance = [cosine(cam_embedding, known_emb) for known_emb in base_embeddings]

        min_distance = min(distance)
        if min_distance < THRESHOLD:
            print("Это тот же человек")
        else:
            print("Это другой человек")
            ctypes.windll.user32.LockWorkStation()
            source_file = 'my_photo.jpg'
            destination_folder = 'block_users'
            os.makedirs(destination_folder, exist_ok=True)
            destination_path = os.path.join(destination_folder, os.path.basename(source_file))
            shutil.move(source_file, destination_path)
    except Exception as e:
        print(f"Ошибка распознавания: {e}")