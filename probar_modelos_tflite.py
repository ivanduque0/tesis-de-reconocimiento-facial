import cv2
import tflite_runtime.interpreter as tflite
import numpy as np
import mediapipe as mp
from math import  acos,degrees
import os
import pickle
import matplotlib.pyplot as plt
import urllib.request

nombres = []
mp_face_mesh = mp.solutions.face_mesh
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
url = 'http://192.168.20.136/cam-hi.jpg'
pickle_in = open("/home/seguricel/Downloads/nombres.pickle","rb")
nombres = pickle.load(pickle_in)

tflite_interpreter = tflite.Interpreter("/home/seguricel/Downloads/modelolite er-iv-di conv2d (128,128,256)(64,128,128) colab 300x300")
tflite_interpreter.allocate_tensors()

def preparar(imagen):
    matriz_imagen = cv2.imread(imagen, cv2.IMREAD_GRAYSCALE)  # lee la imagen y la convierte a escala de grises
    #cv2.imread(os.path.join(ruta,foto), cv2.IMREAD_GRAYSCALE)
    nueva_matriz_imagen = cv2.resize(matriz_imagen, (300, 300))  # redimensiona la imagen
    nueva_matriz_imagen = nueva_matriz_imagen.reshape(-1, 300, 300, 1)
    nueva_matriz_imagen = nueva_matriz_imagen.astype(np.float32)
    return nueva_matriz_imagen



with mp_face_detection.FaceDetection(
    min_detection_confidence=0.7) as face_detection:
    
    with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75) as face_mesh:
    
        while True:

            imagenurl = urllib.request.urlopen (url) #abrimos el URL
            imagenarray = np.array(bytearray(imagenurl.read()),dtype=np.uint8)
            video = cv2.imdecode (imagenarray,-1) #decodificamos
            #video = cv2.imread("pruebaaa.jpg")  # para pruebas con una foto
            videorgb = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
            alto, ancho, _ = video.shape
            results = face_detection.process(videorgb)
            
            
            if results.detections is not None:
                for detection in results.detections:
                    #mp_drawing.draw_detection(video, detection, 
                        #mp_drawing.DrawingSpec(color=(0, 255, 255), circle_radius=5), 
                        #mp_drawing.DrawingSpec(color=(255, 0, 255)))
                    
                    
                    #deteccion de coordenadas de ojo 1
                    x1 =int(detection.location_data.relative_keypoints[0].x * ancho)
                    y1 =int(detection.location_data.relative_keypoints[0].y * alto)
                    
                    #deteccion de coordenadas de ojo 2
                    x2 =int(detection.location_data.relative_keypoints[1].x * ancho)
                    y2 =int(detection.location_data.relative_keypoints[1].y * alto)

                    #creando coordenadas de cada punto
                    p1 = np.array([x1, y1])
                    p2 = np.array([x2, y2])
                    p3 = np.array([x2, y1])

                    #obteniendo distancias entre los puntos
                    d1 = np.linalg.norm(p1-p2)
                    d2 = np.linalg.norm(p1-p3)

                    angulo = degrees(acos(d2/d1))
                    
                    #haciendo que el angulo sea negativo cuando se rote la cabeza
                    #a la derecha
                    if y1 < y2:
                        angulo= -angulo

                    #registrando la rotacion
                    m = cv2.getRotationMatrix2D((ancho // 2, alto // 2), -angulo, 1)
                    
                    #crearndo nueva ventana y dandole la rotacion a la imagen
                    alinear = cv2.warpAffine(video, m, (ancho,alto))
                    #cv2.imshow("alinear", alinear)


                    xmin = int(detection.location_data.relative_bounding_box.xmin * ancho)
                    ymin = int(detection.location_data.relative_bounding_box.ymin * alto)
                    w = int(detection.location_data.relative_bounding_box.width * ancho)
                    h = int(detection.location_data.relative_bounding_box.height * alto)

                    punto_izquierda = np.array([xmin, ymin])
                    punto_derecha = np.array([w, ymin])
                    punto_abajo = np.array([xmin, h])

                    altura = h - ymin
                    largo = w - xmin
                    

                    if xmin < 0 or ymin < 0:
                        continue

                    vista_previa = alinear[ymin : ymin + h, xmin: xmin + w]

                    #cv2.imshow("vista previa", vista_previa) 
                    #cv2.imshow("vista previa", alinear)

                    alineargb = cv2.cvtColor(alinear, cv2.COLOR_BGR2RGB)
                    
                    results2 = face_mesh.process(videorgb)   


                                    
                    #if results2.multi_face_landmarks is not None:
                     #   for face_landmarks in results2.multi_face_landmarks:
                      #      mp_drawing.draw_landmarks(video, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS, mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1),mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1))
                                # FACEMESH_TESSELATION CONTOURS


                    cv2.imwrite(f'rostrorver.jpg', vista_previa)
                    cv2.imshow("vista previa", vista_previa) 
                    
                    #codigo donde se usa tensorflow lite
                    input_details = tflite_interpreter.get_input_details()
                    output_details = tflite_interpreter.get_output_details()
                    
                    #print("== Input details ==")
                    #print("shape:", input_details[0]['shape'])
                    #print("type:", input_details[0]['dtype'])
                    #print("\n== Output details ==")
                    #print("shape:", output_details[0]['shape'])
                    #print("type:", output_details[0]['dtype'])
                    
                    tflite_interpreter.resize_tensor_input(input_details[0]['index'], (1, 300, 300, 1))
                    tflite_interpreter.resize_tensor_input(output_details[0]['index'], (1, 3))
                    tflite_interpreter.allocate_tensors()
                    tflite_interpreter.set_tensor(input_details[0]['index'], preparar('rostrorver.jpg'))
                    # Run inference
                    tflite_interpreter.invoke()
                    # Get prediction results
                    tflite_model_predictions = tflite_interpreter.get_tensor(output_details[0]['index'])
                    #print("Prediction results shape:", tflite_model_predictions.shape)
                    print(tflite_model_predictions)
                    print(nombres)
                    
                    #fin del codigo donde se usa tensorflow lite
                    
                 

                        
        
            cv2.imshow('imagenn', video)
            if cv2.waitKey(1) & 0xFF == 27:
                break

         
camara.release()
cv2.destroyAllWindows()


