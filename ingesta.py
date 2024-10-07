import boto3
import mysql.connector
import csv

db_host = "3.230.28.178"  
db_user = "postgres"   
db_password = "utec" 
db_name = "rockie" 
table_name1 = "activities" 
table_name2 = "student" 
db_port = 8002 

ficheroUpload1 = "activities.csv"
ficheroUpload2 = "student.csv"
nombreBucket = "bucket-ingesta-parcial"

conn = mysql.connector.connect(
    host=db_host,
    port=db_port, 
    user=db_user,
    password=db_password,
    database=db_name
)
cursor = conn.cursor()

query1 = f"SELECT * FROM {table_name1}"
cursor.execute(query1)
rows1 = cursor.fetchall()
column_names1 = [i[0] for i in cursor.description]

with open(ficheroUpload1, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(column_names1)  
    writer.writerows(rows1) 

query2 = f"SELECT * FROM {table_name2}"
cursor.execute(query2)
rows2 = cursor.fetchall()
column_names2 = [i[0] for i in cursor.description]

with open(ficheroUpload2, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(column_names2)  
    writer.writerows(rows2) 

cursor.close()
conn.close()

s3 = boto3.client('s3')
s3.upload_file(ficheroUpload1, nombreBucket, ficheroUpload1)
s3.upload_file(ficheroUpload2, nombreBucket, ficheroUpload2)

print("Ingesta completada y archivos subidos a S3")
