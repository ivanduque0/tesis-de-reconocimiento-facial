import cv2
import tflite_runtime.interpreter as tflite
import numpy as np
import mediapipe as mp
from math import  acos,degrees
import os
import pickle

nombres = []
mp_face_mesh = mp.solutions.face_mesh
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
camara = cv2.VideoCapture("http://192.168.21.102:81/stream")
pickle_in = open("/home/ivan/Downloads/nombres.pickle","rb")
nombres = pickle.load(pickle_in)
parpado=0
tflite_interpreter = tflite.Interpreter("/home/ivan/Downloads/modelolite er-iv-di conv2d (128,128,256)(64,128,128) colab 300x300")
tflite_interpreter.allocate_tensors()

def preparar(imagen):
    matriz_imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)  # lee la imagen y la convierte a escala de grises
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

            ret,video = camara.read()
            #video = cv2.flip(video, 0)
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
                    cv2.imshow("vista previa", vista_previa)   


                                    
                    if results2.multi_face_landmarks is not None:
                    	for face_landmarks in results2.multi_face_landmarks:
                            y_386 = int(face_landmarks.landmark[386].y * alto) 
                            y_374 = int(face_landmarks.landmark[374].y * alto) 
                            y_159 = int(face_landmarks.landmark[159].y * alto)
                            y_145 = int(face_landmarks.landmark[145].y * alto)
                            
                            p1 = np.array([0, y_386])
                            p2 = np.array([0, y_374])
                            p3 = np.array([0, y_159])
                            p4 = np.array([0, y_145])

                            d1 = np.linalg.norm(p2-p1)
                            d2 = np.linalg.norm(p4-p3)

                            print(d1)
                            print(d2)
                            
                            dif1 = (d1old*29)/100
                            dif2 = (d2old*29)/100

                            if d1==d1old and d2==d2old:
                                parpado=1
                        
                            if d1<=d1old-dif1 and d2<=d2old-dif2 and parpado==1:	

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
                                tflite_interpreter.set_tensor(input_details[0]['index'], preparar(vista_previa))
                                # Run inference
                                tflite_interpreter.invoke()
                                # Get prediction results
                                tflite_model_predictions = tflite_interpreter.get_tensor(output_details[0]['index'])
                                #print("Prediction results shape:", tflite_model_predictions.shape)
                                print(tflite_model_predictions)
                                print(nombres)
                                
                                #fin del codigo donde se usa tensorflow lite            
                                parpado=0
                                d1old=0
                                d2old=0

                            if d1 >= d1old:
                                d1old=d1
                            if d1 >= d1old:
                                d2old=d1

            cv2.imshow('imagenn', video)

            if cv2.waitKey(1) & 0xFF == 27:
                break

         
camara.release()
cv2.destroyAllWindows()


