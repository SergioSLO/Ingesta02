import boto3
import mysql.connector
import csv

# Parámetros de la base de datos MySQL
db_host = "54.163.40.147"  # Cambia esto a tu host de base de datos
db_user = "root"    # Cambia esto por tu nombre de usuario
db_password = "utec"  # Cambia esto por tu contraseña
db_name = "tienda"  # Cambia esto por el nombre de tu base de datos
table_name = "fabricantes"  # Cambia esto por el nombre de tu tabla

# Parámetros de AWS S3
ficheroUpload = "data.csv"
nombreBucket = "sslo-output01"

# Conexión a la base de datos MySQL
conn = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)
cursor = conn.cursor()

# Consulta para leer todos los registros de la tabla
query = f"SELECT * FROM {table_name}"
cursor.execute(query)

# Obtener los resultados
rows = cursor.fetchall()
column_names = [i[0] for i in cursor.description]

# Escribir los resultados en un archivo CSV
with open(ficheroUpload, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(column_names)  # Escribir el encabezado
    writer.writerows(rows)  # Escribir las filas

# Cerrar la conexión a la base de datos
cursor.close()
conn.close()

# Subir el archivo CSV a un bucket de S3
s3 = boto3.client('s3')
s3.upload_file(ficheroUpload, nombreBucket, ficheroUpload)

print("Ingesta completada y archivo subido a S3")
