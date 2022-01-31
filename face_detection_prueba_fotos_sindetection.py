import face_recognition
import cv2
import tensorflow as tf
import numpy as np
import mediapipe as mp
import os

nombres = ["erika", "ivan", "diego"]
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
caraivan = face_recognition.load_image_file("rostros para face recognition/ivan.jpg")
caraerika = face_recognition.load_image_file("rostros para face recognition/erika.jpg")
caradiego = face_recognition.load_image_file("rostros para face recognition/diego.jpg")
encodingerika = face_recognition.face_encodings(caraerika)[0]
encodingivan = face_recognition.face_encodings(caraivan)[0]
encodingdiego = face_recognition.face_encodings(caradiego)[0]
caras=[encodingerika, encodingivan, encodingdiego]
ruta = "C:/Users/seguricell/Desktop/tensorflow/erikamasfotos"


    
for foto in os.listdir(ruta):

    imagen = cv2.imread(os.path.join(ruta,foto))

    alto, ancho, _ = imagen.shape
    imagenrgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    print(foto)

    face_locations = face_recognition.face_locations(imagen)
    encodingcamara = face_recognition.face_encodings(imagen)
    

    if encodingcamara != []:
        encodingcamaraa = face_recognition.face_encodings(imagenrgb, face_locations)[0]

        resultado = face_recognition.compare_faces(caras, encodingcamaraa, tolerance=0.50)
        # print(f" es ivan = {resultado[1]}")
        # print(f" es erika = {resultado[0]}")
    
        if resultado[0]:
            print(nombres[0])

        if resultado[1]:
            print(nombres[1])

        if resultado[2]:
            print(nombres[2])

