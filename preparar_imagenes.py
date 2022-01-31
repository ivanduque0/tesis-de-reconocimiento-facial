import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import random 
import pickle


directorio = "C:/Users/Ivonne/Desktop/tensorflow/caras"
personas = ["erika","ivan"]

#for persona in personas:
    #ruta = os.path.join(directorio, personas)
    #print(ruta)

    #for foto in os.listdir(ruta):
        #matriz_foto= cv2.imread(os.path.join(ruta,foto), cv2.IMREAD_GRAYSCALE)

data_entrenamiento = []

def crear_entrenamiento_datos():
        for persona in personas:
            ruta = os.path.join(directorio, persona)
            class_num = personas.index(persona)
            print(class_num)

            for foto in os.listdir(ruta):
                
                try:
                    
                    matriz_foto = cv2.imread(os.path.join(ruta,foto), cv2.IMREAD_GRAYSCALE)
                   # khe = np.array(matriz_foto)
                    #print(khe.shape)
                    #matriz_foto = cv2.imread(os.path.join(ruta,foto), cv2.IMREAD_GRAYSCALE)
                    #matriz_foto = cv2.imread(os.path.join(ruta,foto), cv2.IMREAD_GRAYSCALE)
                    matriz_redimensionada = cv2.resize(matriz_foto, (250,250))
                    #khe = np.array(matriz_redimensionada)
                    #print(khe.shape)
                    data_entrenamiento.append([matriz_redimensionada, class_num])
                
                    #plt.imshow(matriz_redimensionada, cmap='gray')
                    #plt.show()
                    #print(matriz_redimensionada.shape)
                    
                
                except Exception as e:
                    pass

crear_entrenamiento_datos()

random.shuffle(data_entrenamiento)

x = []
y = []


for caracteristicas, etiqueta in data_entrenamiento:
    x.append(caracteristicas)
    y.append(etiqueta)

# esto es opcional, solo para ver los arreglos print(x[0].reshape(-1, 70, 70, 1))

x = np.array(x).reshape(-1, 250, 250, 1)
y = np.array(y)

print(x.shape)
pickle_out = open("x.pickle","wb")
pickle.dump(x, pickle_out)
pickle_out.close()

pickle_out = open("y.pickle","wb")
pickle.dump(y, pickle_out)
pickle_out.close()