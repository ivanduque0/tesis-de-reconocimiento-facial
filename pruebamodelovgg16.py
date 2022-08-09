import tflite_runtime.interpreter as tflite
import time
import urllib.request
import numpy as np
import cv2
import os

tflite_interpreter = tflite.Interpreter("/home/seguricel/Desktop/modelo_antispoofing/modelospoofinglite_vgg16")
tflite_interpreter.allocate_tensors()
# camara = cv2.VideoCapture("http://192.168.20.148:8080/?action=stream")
while True:
    # ret,video = camara.read()
    url = 'http://192.168.21.126:8080/?action=snapshot'
    imagenurl = urllib.request.urlopen (url) #abrimos el URL
    imagenarray = np.array(bytearray(imagenurl.read()),dtype=np.uint8)
    video = cv2.imdecode (imagenarray,-1)
    alto, ancho, _ = video.shape
    #print(alto,ancho)
    K = np.float32([[1,0,100],[0,1,100]])
    video2 = cv2.warpAffine(video, K, (ancho+200,alto+200))
    alto2, ancho2, _ = video2.shape
    K = cv2.getRotationMatrix2D((ancho2 // 2, alto2 // 2), 90, 1)
    video2 = cv2.warpAffine(video2, K, (alto2,ancho2))
    K = np.float32([[1,0,-160],[0,1,-41]])
    video3 = cv2.warpAffine(video2, K, (alto, ancho))
    video3 = cv2.flip(video3, 0)
    #cv2.imshow('imagen3', video3)
    tecla = cv2.waitKey(1)
    if tecla & 0xFF == 27:
        break
    video3 = cv2.resize(video3, (224,224))
    #print(video4.shape)
    video4 = video3.reshape(-1, 224, 224, 3)
    video4 = video4.astype(np.float32)
    #print(video4.shape)
    

    #codigo donde se usa tensorflow lite
    input_details = tflite_interpreter.get_input_details()
    output_details = tflite_interpreter.get_output_details()
    
    #print("== Input details ==")
    #print("shape:", input_details[0]['shape'])
    #print("type:", input_details[0]['dtype'])
    #print("\n== Output details ==")
    #print("shape:", output_details[0]['shape'])
    #print("type:", output_details[0]['dtype'])
    
    tflite_interpreter.resize_tensor_input(input_details[0]['index'], (1, 224, 224, 3))
    # tflite_interpreter.resize_tensor_input(input_details[0]['index'], (1, 224, 224, 3))
    tflite_interpreter.resize_tensor_input(output_details[0]['index'], (1, 2))
    tflite_interpreter.allocate_tensors()
    tflite_interpreter.set_tensor(input_details[0]['index'], video4)
    # Run inference
    tflite_interpreter.invoke()
    # Get prediction results
    tflite_model_predictions = tflite_interpreter.get_tensor(output_details[0]['index'])
    #print("Prediction results shape:", tflite_model_predictions.shape)
    #print(tflite_model_predictions)

    if tflite_model_predictions[0][0] > tflite_model_predictions[0][1]:
        print('falso')
    else:
        print('verdadero')
    #cv2.imshow('imagen', video3)