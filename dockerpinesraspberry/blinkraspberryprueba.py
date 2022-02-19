import RPi.GPIO as GPIO
import time
import psycopg2

# Primero se configuran los pines
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setwarnings(False)

# Tiempo de encendido
tiempo = 2 #Time interval in Seconds

conn = None
try:  
    conn = psycopg2.connect(
        database="tesis", user="tesis", password="tesis", host="192.168.21.101", port="4443"
    )
    conn.autocommit = False
    cursor = conn.cursor()

    while True:
        cursor.execute('SELECT * FROM led')
        led_onoff = cursor.fetchall()

        print("aun nada")

        if led_onoff[0][0] == 1:
            GPIO.output(3, True)
            time.sleep(tiempo)
            GPIO.output(3, False)
            time.sleep(tiempo)
            print("si funciono")
except (Exception, psycopg2.Error) as error:
    print("fallo en hacer las consultas")
    GPIO.cleanup()

finally:
    if conn:
        cursor.close()
        conn.close()
        print("se ha cerrado la conexion a la base de datos")
        GPIO.cleanup()
