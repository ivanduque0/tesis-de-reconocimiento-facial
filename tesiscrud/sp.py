import psycopg2
import pytz
from datetime import datetime

conn = None
try:

    conn = psycopg2.connect(
        database="tesis2", user="tesis2", password="tesis2", host="0.0.0.0", port="4443"
    )

    conn.autocommit = False
    cursor = conn.cursor()


    cursor.execute('SELECT * FROM prueba')
    d= cursor.fetchall()
    diass = d[0][0]
    print(diass)
    listadias=[]
    for d in diass:
        listadias.append(d)
    print(listadias)
    #print(diass[0])
    weekDays = ("lunes","martes","miercoles","jueves","viernes","sabado","domingo")
    tz = pytz.timezone('America/Caracas')
    caracas_now = datetime.now(tz)
    dia = caracas_now.weekday()
    diia = weekDays[diass]
    print(diia)
except (Exception, psycopg2.Error) as error:
    print("fallo en hacer las consultas")

finally:
    if conn:
        cursor.close()
        conn.close()
        print("se ha cerrado la conexion a la base de datos")
