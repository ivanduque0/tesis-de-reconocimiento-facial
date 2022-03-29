import psycopg2
from datetime import datetime
import os
import subprocess

#DATABASE_URL = config('DATABASE_URL', default='')
CONTRATO='casa'
conn = None
try:

    connlocal = psycopg2.connect(
        database="tesis", user="tesis", password="tesis", host="0.0.0.0", port="44"
    )
    cursorlocal = connlocal.cursor()
    
    conn_info = subprocess.run(["heroku", "config:get", "DATABASE_URL", "-a", 'tesis-reconocimiento-facial'], stdout = subprocess.PIPE)
    connuri = conn_info.stdout.decode('utf-8').strip()
    connheroku = psycopg2.connect(connuri)
    cursorheroku = connheroku.cursor()

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
                contrato=interaccion[5]
                cedula=interaccion[6]

                cursorheroku.execute('''INSERT INTO web_interacciones (nombre, fecha, hora, razon, contrato, cedula_id)
                VALUES (%s, %s, %s, %s, %s, %s);''', (nombre, fecha, hora, razon, contrato, cedula))
                connheroku.commit()

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

        if nro_usu_heroku > nro_usu_local:
            diferencia = nro_usu_heroku - nro_usu_local
            diferencia_rango = list(range(diferencia))

            usuarios_heroku = usuarios_heroku[::-1]

            for posicion in diferencia_rango:

                usuario = usuarios_heroku[posicion]

                cedula=usuario[0]
                nombre=usuario[1]
                contrato=interaccion[2]

                cursorlocal.execute('''INSERT INTO web_usuarios (cedula, nombre, contrato_id)
                VALUES (%s, %s, %s);''', (cedula, nombre, contrato))
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

        cursorlocal.execute('SELECT * FROM web_fotos')
        fotos_local= cursorlocal.fetchall()

        cursorheroku.execute('SELECT * FROM web_fotos')
        fotos_heroku= cursorheroku.fetchall()

        nro_fotos_local = len(fotos_local)
        nro_fotos_heroku = len(fotos_heroku)

        if nro_fotos_heroku > nro_fotos_local:
            diferencia = nro_fotos_heroku - nro_fotos_local
            diferencia_rango = list(range(diferencia))

            fotos_heroku = fotos_heroku[::-1]

            for posicion in diferencia_rango:

                usuario = fotos_heroku[posicion]

                foto=usuario[1]
                cedula=usuario[2]
                #NECESITO AGREGAR UNA COLUMNA CON EL CONTRATO PARA MANIPULAR MAS FACIL ESTA TABLA
                cursorlocal.execute('''INSERT INTO web_usuarios (foto, cedula_id)
                VALUES (%s, %s, %s);''', (foto, cedula))
                connlocal.commit()
        diferencia=0
        diferencia_rango=0

except (Exception, psycopg2.Error) as error:
    print("fallo en hacer las consultas")

finally:
    if conn:
        cursorlocal.close()
        connlocal.close()
        cursorheroku.close()
        connheroku.close()
        print("se ha cerrado la conexion a la base de datos")
