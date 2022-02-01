import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import random 
import pickle
import glob

directorio = "C:/Users/Ivonne/Desktop/tensorflow/"
carpetas_personas = os.listdir(directorio)
nombres = []
for imagen in carpetas_personas:
    nombre = os.path.splitext(imagen)[0]
    print(nombre)
    nombres.append(nombre)
    
#for persona in personas:
    #ruta = os.path.join(directorio, personas)
    #print(ruta)

    #for foto in os.listdir(ruta):
        #matriz_foto= cv2.imread(os.path.join(ruta,foto), cv2.IMREAD_GRAYSCALE)

data_entrenamiento = []

def crear_entrenamiento_datos():
        for persona in nombres:
            
            ruta = os.path.join(directorio)
            class_num = nombres.index(persona)
            print(class_num)

            for foto in glob.glob(f'partes del rostro/{persona}/nariz*.*'):
                
                try:
                    
                    matriz_foto = cv2.imread(os.path.join(ruta,foto), cv2.IMREAD_GRAYSCALE)
                    #matriz_foto = cv2.imread(os.path.join(ruta,foto), cv2.IMREAD_GRAYSCALE)
                    #matriz_foto = cv2.imread(os.path.join(ruta,foto), cv2.IMREAD_GRAYSCALE)
                    matriz_redimensionada = cv2.resize(matriz_foto, (105,96))
                    #khe = np.array(matriz_redimensionada)
                    #print(khe.shape)
                    data_entrenamiento.append([matriz_redimensionada, class_num])
                    print(foto)
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

x = np.array(x).reshape(-1, 105, 96, 1)
y = np.array(y)

print(x.shape)
pickle_out = open("x2 nariz105x96.pickle","wb")
pickle.dump(x, pickle_out)
pickle_out.close()

pickle_out = open("y2 nariz105x96.pickle","wb")
pickle.dump(y, pickle_out)
pickle_out.close()

pickle_out = open("nombres.pickle","wb")
pickle.dump(nombres, pickle_out)
pickle_out.close()
