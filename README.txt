En este repositorio se encuentran los archivos y explicaciones necesarias para hacer correr una aplicacion de reconocimiento facial que interacciona con una base de datos en postgres. La aplicacion y la base de datos corren en contenedores docker independiente el uno del otro.

El archivo Dockerfile es para ser usado en una computadora con una aquitectura amd. El codigo llamado face_detection_prueba_stream_parpadeos_psycopg.py es el que por ahora esta mas actualizado en cuanto a la funcionalidad de captar los parpadeos y a las consultas de la base de datos en postgres usando la libreria face recognition

para poder correr la aplicacion se debe hacer lo siguiente:
1) Crear una imagen docker con el archivo docker Dockerfile

2)Hacer un pull a alguna imagen de postgres en dockerhub (en lo personal utilizo la imagen de postgres de alpine porque es mas liviana)

3) crear una red de docker (la red con la que funcionan los scripts .sh se llama dockernetowrktesis, asi que es conveniente crear la red con ese nombre, sino se tendra que cambiar la linea --network= de los archivos .sh con el nombre de la red creada)

4)en mi caso utilizo una cama esp32cam la cual utiliza una ip enla red wifi local por lo que en el codigo de python en la linea 21 aparece el link del stream de la camara, en caso contrario se debe colocar el recurso que se esta usando para captar imagenes

5) Iniciar el script rundockerv2.sh para inciar a correr los contenedores, es muy probable que no funcione al principio porque primero se debe configurar el usuario, base de datos, contrasena, host y puerto a usar de la base de datos. Llegado a este punto el contenedor del codigo de python no va a correr, pero el contenedor de la base de datos si, por lo que primero debes acceder al contenedor de postgres con una sesion interactiva y crear un role, una base de datos, una tabla con las caracteristicas de la consulta en la linea 208 y colocarle una contrasena a la base de datos (para saber como hacer esto vease el archivo txt dedicado al aprendizaje de postgres en la rama "pythonpostgres"), una vez hecho todo eso, se coloca el nombre del usuario, la base de datos y la contrasena del usuario de postgres que se desea usar, luego se ejecuta esta vez el script rundockerv2_1.sh y si todo se hizo bien, se empezara a visualizar la camara, y si un rostro esta en su campo de vision, otra ventana kas pequena aparecera mostrando solo el rostro.

6) comprobar que la aplicacion corre perfectamente colocando el rostro de frente a la camara y sin hacer ningun movimiento se da un parpadeo profundo, se deberia visualizar en la terminal que se agrego una fila en la lista llamada "interacciones"
