import psycopg2
from datetime import datetime
import os
import subprocess
import time

#DATABASE_URL = config('DATABASE_URL', default='')
CONTRATO='casa'
conn = None
usuarios_faltantes_foto=[]
listausuariosheroku=[]
listausuarioslocal=[]
total=0
nro_int_local_old=0

while True:
    
    t1=time.perf_counter()
    while total<=5:
        t2=time.perf_counter()
        total=t2-t1
    total=0
    try:
        
        #con esto se apunta a la base de datos local
        connlocal = psycopg2.connect(
            database="tesis", user="tesis", password="tesis", host="0.0.0.0", port="44"
        )
        cursorlocal = connlocal.cursor()
        print('abr')
        #con esto se apunta a la base de datos en heroku
        conn_info = subprocess.run(["heroku", "config:get", "DATABASE_URL", "-a", 'tesis-reconocimiento-facial'], stdout = subprocess.PIPE)
        connuri = conn_info.stdout.decode('utf-8').strip()
        connheroku = psycopg2.connect(connuri)
        cursorheroku = connheroku.cursor()

        cursorlocal.execute('SELECT * FROM web_interacciones where contrato=%s', (CONTRATO,))
        interacciones_local= cursorlocal.fetchall()
        nro_int_local_old=len(interacciones_local)
        
        cursorlocal.execute('CREATE TABLE IF NOT EXISTS web_usuarios (cedula integer, nombre varchar(150), contrato_id varchar(150))')
        cursorlocal.execute('CREATE TABLE IF NOT EXISTS web_interacciones (nombre varchar(150), fecha date, hora time without time zone, razon varchar(150), contrato varchar(150), cedula_id integer)')
        cursorlocal.execute('CREATE TABLE IF NOT EXISTS web_fotos (foto varchar(150), cedula_id integer)')
        connlocal.commit()
        print('abr')

        t1=time.perf_counter()
        while True:
            t2=time.perf_counter()
            nombre=None
            fecha=None
            hora=None
            razon=None
            contrato=None
            cedula=None
            foto=None

            cursorlocal.execute('SELECT * FROM web_interacciones where contrato=%s', (CONTRATO,))
            interacciones_local= cursorlocal.fetchall()

            nro_int_local = len(interacciones_local)

            if nro_int_local > nro_int_local_old:

                diferencia_rango=nro_int_local-nro_int_local_old
                diferencia= list(range(diferencia_rango))
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
                
                cursorlocal.execute('SELECT * FROM web_interacciones where contrato=%s', (CONTRATO,))
                interacciones_local= cursorlocal.fetchall()
                nro_int_local_old = len(interacciones_local)
                diferencia=0
                diferencia_rango=0
                nombre=None
                fecha=None
                hora=None
                razon=None
                contrato=None
                cedula=None
                foto=None

            cursorlocal.execute('SELECT * FROM web_usuarios where contrato_id=%s', (CONTRATO,))
            usuarios_local= cursorlocal.fetchall()

            cursorheroku.execute('SELECT * FROM web_usuarios where contrato_id=%s', (CONTRATO,))
            usuarios_heroku= cursorheroku.fetchall()

            nro_usu_local = len(usuarios_local)
            nro_usu_heroku = len(usuarios_heroku)


            #cuando se va a eliminar un usuario
            if nro_usu_local > nro_usu_heroku:

                for usuario in usuarios_heroku:
                    cedula=usuario[0]
                    listausuariosheroku.append(cedula)
                
                for usuario in usuarios_local:
                    cedula=usuario[0]
                    listausuarioslocal.append(cedula)
                

                    for usuario in listausuarioslocal:
                        try:
                            listausuariosheroku.index(usuario)
                        except ValueError:
                            cursorlocal.execute('DELETE FROM web_usuarios WHERE cedula=%s)', (usuario,))
                            connlocal.commit()
                listausuariosheroku=[]
                listausuarioslocal=[]



            # cuando se va a agregar usuarios
            if nro_usu_heroku > nro_usu_local:

                for usuario in usuarios_heroku:
                    cedula=usuario[0]
                    listausuariosheroku.append(cedula)
                
                for usuario in usuarios_local:
                    cedula=usuario[0]
                    listausuarioslocal.append(cedula)

                for usuario in listausuariosheroku:
                    try:
                        listausuarioslocal.index(usuario)
                    except ValueError:
                        cursorheroku.execute('SELECT * FROM web_usuarios where cedula=%s', (usuario,))
                        usuario_local= cursorlocal.fetchall()

                        cedula=usuario_local[0]
                        nombre=usuario_local[1]
                        cursorlocal.execute('''INSERT INTO web_usuarios (cedula, nombre, contrato_id)
                        VALUES (%s, %s, %s);''', (cedula, nombre, CONTRATO))
                        connlocal.commit()
                cedula=None
                nombre=None


            if total>10:
                
                for usuario in usuarios_heroku:
                    cedula=usuario[0]
                    listausuariosheroku.append(cedula)

                
                for usuario in usuarios_local:
                    cedula=usuario[0]
                    listausuarioslocal.append(cedula)
                

                for usuario in listausuarioslocal:
                    cursorlocal.execute('SELECT * FROM web_fotos where cedula_id=%s', (usuario,))
                    foto_local= cursorlocal.fetchall()

                    if len(foto_local) == 1:
                        cursorheroku.execute('SELECT * FROM web_fotos where cedula_id=%s', (usuario,))
                        foto_heroku= cursorheroku.fetchall()
                        if len(foto_heroku) == 0:
                            cursorlocal.execute('DELETE FROM web_fotos where cedula_id=%s', (CONTRATO,))
                            connlocal.commit()

                    if len(foto_local) == 0:
                        cursorheroku.execute('SELECT * FROM web_fotos where cedula_id=%s', (usuario,))
                        foto_heroku= cursorheroku.fetchall()
                        if len(foto_heroku) == 1:
                            foto=foto_heroku[1]
                            cedula=foto_heroku[2]
                            cursorlocal.execute('''INSERT INTO web_usuarios (foto, cedula_id)
                            VALUES (%s, %s, %s);''', (foto, cedula))
                            connlocal.commit()
                    
                t1=time.perf_counter()
                total=0

    except (Exception, psycopg2.Error) as error:
        print("fallo en hacer las consultas")

    finally:
        if conn:
            cursorlocal.close()
            connlocal.close()
            cursorheroku.close()
            connheroku.close()
            print("se ha cerrado la conexion a la base de datos")
