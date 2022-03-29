import psycopg2
from datetime import datetime
import os
import subprocess
import time
import cloudinary

CONTRATO='oficina'
conn = None
usuarios_faltantes_foto=[]
total=0
usuarioslocal=[]
usuariosheroku=[]

while True:

    connlocal = None
    connheroku = None
    # Se configuran los pines
    t1=time.perf_counter()
    while total<=5:
        t2=time.perf_counter()
        total=t2-t1

    #DATABASE_URL = config('DATABASE_URL', default='')
    try:

        #con esto se apunta a la base de datos local
        connlocal = psycopg2.connect(
            database="tesis", user="tesis", password="tesis", host="0.0.0.0", port="44"
        )
        cursorlocal = connlocal.cursor()
        
        #con esto se apunta a la base de datos en heroku
        conn_info = subprocess.run(["heroku", "config:get", "DATABASE_URL", "-a", 'tesis-reconocimiento-facial'], stdout = subprocess.PIPE)
        connuri = conn_info.stdout.decode('utf-8').strip()
        connheroku = psycopg2.connect(connuri)
        cursorheroku = connheroku.cursor()
        t1=time.perf_counter()
        while True:
            
            nombre=None
            fecha=None
            hora=None
            razon=None
            contrato=None
            cedula=None
            foto=None
            
            cursorlocal.execute('SELECT * FROM web_interacciones where contrato=%s', (CONTRATO,))
            interacciones_local= cursorlocal.fetchall()

            cursorheroku.execute('SELECT * FROM web_interacciones  where contrato=%s', (CONTRATO,))
            interacciones_heroku= cursorheroku.fetchall()

            nro_int_local = len(interacciones_local)
            nro_int_heroku = len(interacciones_heroku)
            
            
            if nro_int_local > nro_int_heroku:
                diferencia = nro_int_local - nro_int_heroku
                diferencia_rango = list(range(diferencia))

                interacciones_local = interacciones_local[::-1]

                for posicion in diferencia_rango:

                    interaccion = interacciones_local[posicion]

                    nombre=interaccion[1]
                    fecha=interaccion[2]
                    hora=interaccion[3]
                    razon=interaccion[4]
                    cedula=interaccion[6]

                    cursorheroku.execute('''INSERT INTO web_interacciones (nombre, fecha, hora, razon, contrato, cedula_id)
                    VALUES (%s, %s, %s, %s, %s, %s);''', (nombre, fecha, hora, razon, CONTRATO, cedula))
                    connheroku.commit()

            diferencia=0
            diferencia_rango=0
            nombre=None
            fecha=None
            hora=None
            razon=None
            cedula=None
            foto=None

            cursorlocal.execute('SELECT * FROM web_usuarios where contrato_id=%s', (CONTRATO,))
            usuarios_local= cursorlocal.fetchall()

            cursorheroku.execute('SELECT * FROM web_usuarios where contrato_id=%s', (CONTRATO,))
            usuarios_heroku= cursorheroku.fetchall()

            nro_usu_local = len(usuarios_local)
            nro_usu_heroku = len(usuarios_heroku)

            # cuando se elimina 
            print(nro_usu_local)
            print(nro_usu_heroku)
            cursorlocal.execute('SELECT * FROM web_fotos')
            fo= cursorlocal.fetchall()
            print(fo)

            if nro_usu_local > nro_usu_heroku:
                
                
                for usuariolocal in usuarios_local:
                    cedula=usuariolocal[0]
                    try:
                        usuarioslocal.index(cedula)
                    except ValueError:
                        usuarioslocal.append(cedula)

                for usuarioheroku in usuarios_heroku:
                    cedula=usuarioheroku[0]
                    try:
                        usuariosheroku.index(cedula)
                    except ValueError:
                        usuariosheroku.append(cedula)

                for usuario in usuarioslocal:
                    try:
                        usuariosheroku.index(usuario)
                    except ValueError:
                        cursorlocal.execute('DELETE FROM web_usuarios WHERE cedula=%s', (usuario,))
                        cursorlocal.execute('DELETE FROM web_fotos WHERE cedula_id=%s', (usuario,))
                        connlocal.commit()
                usuarioslocal=[]
                usuariosheroku=[]


            #cuando se agrega un usuario
            if nro_usu_heroku > nro_usu_local:
                diferencia = nro_usu_heroku - nro_usu_local
                diferencia_rango = list(range(diferencia))
                usuarios_heroku = usuarios_heroku[::-1]
                
                for posicion in diferencia_rango:
                    usuario = usuarios_heroku[posicion]

                    cedula=usuario[0]
                    nombre=usuario[1]
                    # print(usuario)

                    cursorlocal.execute('''INSERT INTO web_usuarios (cedula, nombre, contrato_id)
                    VALUES (%s, %s, %s);''', (cedula, nombre, CONTRATO))
                    connlocal.commit()
            
        
            
            diferencia=0
            diferencia_rango=0
            nombre=None
            fecha=None
            hora=None
            razon=None
            contrato=None
            cedula=None
            foto=None

            if total >10:
                
                for usuariolocal in usuarios_local:
                    cedula=usuariolocal[0]
                    try:
                        usuarioslocal.index(cedula)
                    except ValueError:
                        usuarioslocal.append(cedula)

                for usuarioheroku in usuarios_heroku:
                    cedula=usuarioheroku[0]
                    try:
                        usuariosheroku.index(cedula)
                    except ValueError:
                        usuariosheroku.append(cedula)


                for usuariolocal in usuarios_local:
                    
                    cedula=usuariolocal[0]

                    cursorlocal.execute('SELECT*FROM web_fotos WHERE cedula_id=%s', (cedula,))
                    foto_usuario = cursorlocal.fetchall()

                    if len(foto_usuario) == 0:
                    
                        usuarios_faltantes_foto.append(cedula)
                    if len(foto_usuario) ==1:
                        cursorheroku.execute('SELECT*FROM web_fotos WHERE cedula_id=%s', (cedula,))
                        foto_usuario = cursorlocal.fetchall()
                        if len(foto_usuario) ==0:
                            cursorlocal.execute('DELETE FROM web_fotos WHERE cedula_id=%s', (cedula,))
                            connlocal.commit()


                t1=time.perf_counter()


            if len(usuarios_faltantes_foto) > 0:
                
                for usuario_foto in usuarios_faltantes_foto:

                    cursorheroku.execute('SELECT * FROM web_fotos WHERE cedula_id=%s',(usuario_foto,))
                    foto_usuario= cursorheroku.fetchall()
                    print(foto_usuario)
                    if len(foto_usuario) > 0:

                        foto=foto_usuario[0][1]
                        cedula=foto_usuario[0][2]
                        #SE PUEDE AGREGAR UNA COLUMNA CON EL CONTRATO PARA MANIPULAR MAS FACIL ESTA TABLA
                        cursorlocal.execute('''INSERT INTO web_fotos (foto, cedula_id)
                        VALUES (%s, %s);''', (foto, cedula))
                        connlocal.commit()
                        usuarios_faltantes_foto.remove(usuario_foto)
                usuarios_faltantes_foto = []
            t2=time.perf_counter()
            total=t2-t1

    except (Exception, psycopg2.Error) as error:
        print("fallo en hacer las consultas")
        if connlocal or connheroku:    
            cursorlocal.close()
            connlocal.close()
            cursorheroku.close()
            connheroku.close()


    finally:
        if connlocal or connheroku:
            cursorlocal.close()
            connlocal.close()
            cursorheroku.close()
            connheroku.close()
            print("se ha cerrado la conexion a la base de datos")
