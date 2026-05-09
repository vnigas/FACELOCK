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

base = []

for file in os.listdir(IMAGE_DIR):
    path = os.path.join(IMAGE_DIR, file)

    result = DeepFace.represent(img_path=path)

    embedding = np.array(result[0]['embedding']).flatten()

    base.append(embedding)

with open(DB_PATH, 'wb') as f:
    pickle.dump(base, f)

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

        distance = [cosine(cam_embedding, known_emb) for known_emb in base]

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