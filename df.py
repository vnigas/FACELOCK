from deepface import DeepFace
import cv2
import time
import os
import numpy as np
from scipy.spatial.distance import cosine
from winlocker import winlock


known_face = "data/know_face"
img_from_cam = "my_photo.jpg"
THRESHOLD = 0.3

known_embeddings = []
for file in os.listdir(known_face):
    path = os.path.join(known_face, file)

    try:
        rep = DeepFace.represent(img_path=path, enforce_detection=True)
        known_embeddings.append(rep[0]["embedding"])
        print(f"{file} запущен")
    except Exception as e:
        print(f"{file} пропущен: {e}")

known_embeddings = np.array(known_embeddings)
print(f"загружено {len(known_embeddings)}")

cap = cv2.VideoCapture(0)

while True:
    time.sleep(10)
    ret, frame = cap.read()
    if not ret:
        continue
    cv2.imwrite(img_from_cam, frame)
    # Сравнение лиц
    try:
        rep = DeepFace.represent(img_path=img_from_cam, enforce_detection=True)
        cam_embedding = np.array(rep[0]["embedding"])

        distance = [cosine(cam_embedding, known_emb) for known_emb in known_embeddings]

        min_distance = min(distance)
        if min_distance < THRESHOLD:
            print("Это тот же человек")
        else:
            print("Это другой человек")
            winlock()
    except Exception as e:
        print(f"Ошибка распознавания: {e}")
