'''
Import PostgreSQL in Python
'''
import psycopg2 as sql

connection = sql.connect(
    database='testdatabase',
    user='testuser',
    password='12345678',
    host='localhost',
    port='5432'
)

# create cursor
cursor = connection.cursor() 

# excecute query
query = 'SELECT * FROM testtable'
cursor.execute(query)

# fetch result
result = cursor.fetchall()

for row in result:
    print(row)

cursor.close()
connection.close()
