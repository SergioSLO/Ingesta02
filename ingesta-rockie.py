import boto3
import mysql.connector
import csv

db_host = "3.230.28.178"  
db_user = "root"   
db_password = "utec" 
db_name = "mysql" 
table_name1 = "Rockie" 
table_name2 = "Accesorio"
db_port = 8002 

ficheroUpload1 = "rockie.csv"
ficheroUpload2 = "accesorio.csv"
nombreBucket = "bucket-ingesta-parcial"

# Conexión a la base de datos
conn = mysql.connector.connect(
    host=db_host,
    port=db_port, 
    user=db_user,
    password=db_password,
    database=db_name
)
cursor = conn.cursor()

# Consulta para la tabla Rockie
query1 = f"SELECT * FROM {table_name1}"
cursor.execute(query1)
rows1 = cursor.fetchall()
column_names1 = [i[0] for i in cursor.description]

# Escribir los resultados de la tabla Rockie en un archivo CSV
with open(ficheroUpload1, mode='w', newline='') as file1:
    writer1 = csv.writer(file1)
    writer1.writerow(column_names1)  
    writer1.writerows(rows1) 

# Consulta para la tabla Accesorio
query2 = f"SELECT * FROM {table_name2}"
cursor.execute(query2)
rows2 = cursor.fetchall()
column_names2 = [i[0] for i in cursor.description]

# Escribir los resultados de la tabla Accesorio en un archivo CSV
with open(ficheroUpload2, mode='w', newline='') as file2:
    writer2 = csv.writer(file2)
    writer2.writerow(column_names2)  
    writer2.writerows(rows2) 

# Cerrar cursor y conexión
cursor.close()
conn.close()

# Subir archivos a S3
s3 = boto3.client('s3')
s3.upload_file(ficheroUpload1, nombreBucket, ficheroUpload1)
s3.upload_file(ficheroUpload2, nombreBucket, ficheroUpload2)

print("Ingesta completada y archivos subidos a S3")
