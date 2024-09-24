import boto3
import mysql.connector
import csv

db_host = "54.163.40.147"  
db_user = "root"   
db_password = "utec" 
db_name = "tienda" 
table_name = "fabricantes" 
db_port = 8005 

ficheroUpload = "data.csv"
nombreBucket = "sslo-output01"

conn = mysql.connector.connect(
    host=db_host,
    port=db_port, 
    user=db_user,
    password=db_password,
    database=db_name
)
cursor = conn.cursor()

query = f"SELECT * FROM {table_name}"
cursor.execute(query)

rows = cursor.fetchall()
column_names = [i[0] for i in cursor.description]

with open(ficheroUpload, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(column_names)  
    writer.writerows(rows) 

cursor.close()
conn.close()

s3 = boto3.client('s3')
s3.upload_file(ficheroUpload, nombreBucket, ficheroUpload)

print("Ingesta completada y archivo subido a S3")
