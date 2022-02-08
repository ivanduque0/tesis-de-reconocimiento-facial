import psycopg2


try:
    #aqui se establece la coenxion con la base de datos
    conn = psycopg2.connect(
        database="tesis", user="tesis", password="", host="", port=""
    )

    #aqui se habilita la opcion para hacer los guardados automaticos a la base de datos
    conn.autocommit = False

    #aqui se crea un objeto que va a apuntar hacia la base de datos 
    # para empezar a hacer las consultas 
    cursor = conn.cursor()

    #aqui se muestra como se hacen las consultas

    cursor.execute('''INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX,
    INCOME) VALUES ('Ramya', 'Rama priya', 27, 'F', 9000)''')
    cursor.execute('''INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX,
    INCOME) VALUES ('Vinay', 'Battacharya', 20, 'M', 6000)''')
    cursor.execute('''INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX,
    INCOME) VALUES ('Sharukh', 'Sheik', 25, 'M', 8300)''')
    cursor.execute('''INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX,
    INCOME) VALUES ('Sarmista', 'Sharma', 26, 'F', 10000)''')
    cursor.execute('''INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX,
    INCOME) VALUES ('Tripthi', 'Mishra', 24, 'F', 6000)''')

    #con esto se suben las consultas a la base de datos
    conn.commit()

    # este es un contador que se usa para saber
    #cuantas filas se cambiaron
    count = cursor.rowcount

    print(count)

except (Exception, psycopg2.Error) as error:
    print("fallo en hacer las consultas")

finally:
    if conn:
        cursor.close()
        conn.close()
        print("se ha cerrado la conexion a la base de datos")