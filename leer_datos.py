import psycopg2


try:
    #aqui se establece la coenxion con la base de datos
    conn = psycopg2.connect(
        database="tesis", user="tesis", password="tesis", host="localhost", port="5432"
    )

    #aqui se habilita la opcion para hacer los guardados automaticos a la base de datos
    conn.autocommit = False

    #aqui se crea un objeto que va a apuntar hacia la base de datos 
    # para empezar a hacer las consultas 
    cursor = conn.cursor()
    array_tables = cursor.fetchall()

    for t_name_table in array_tables:
        print(t_name_table + "\n")

except (Exception, psycopg2.Error) as error:
    print("fallo en hacer las consultas")

finally:
    if conn:
        cursor.close()
        conn.close()
        print("se ha cerrado la conexion a la base de datos")