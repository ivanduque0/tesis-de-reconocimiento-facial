from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
import pickle
import tensorflow as tf

pickle_in = open("x.pickle","rb")
x = pickle.load(pickle_in)

pickle_in = open("y.pickle","rb")
y = pickle.load(pickle_in)

x = x/255.0

print(y)

y2 = tf.keras.utils.to_categorical(y, num_classes=2)

print(y2)

modelo = Sequential()

modelo.add(Conv2D(64, (3, 3), input_shape=x.shape[1:]))
modelo.add(Activation('relu'))
modelo.add(MaxPooling2D(pool_size=(2, 2)))

modelo.add(Conv2D(64, (3, 3), (1, 1)))
modelo.add(Activation('relu'))
modelo.add(MaxPooling2D(pool_size=(2, 2)))

modelo.add(Conv2D(64, (3, 3), (1, 1)))
modelo.add(Activation('relu'))
modelo.add(MaxPooling2D(pool_size=(2, 2)))


modelo.add(Flatten())

modelo.add(Dense(128))
modelo.add(Activation('relu'))

modelo.add(Dense(128))
modelo.add(Activation('relu'))

modelo.add(Dense(2))
modelo.add(Activation('softmax'))

modelo.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

modelo.summary()

modelo.fit(x, y2, batch_size=10, epochs=4, validation_split=0.4)

modelo.save('abrxd')
