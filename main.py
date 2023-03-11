'''
Import PostgreSQL in Python
'''
import psycopg2 as sql

class ConnectToPostgres():
    def __init__(self):
        self.connection = sql.connect(
            database='testdatabase',
            user='postgres',
            password='12345678',
            host='localhost',
            port='5432'
        )

        self.user_table = 'testschema.testtable'

    def get_all_user(self):
        try:
            # create cursor
            cursor = self.connection.cursor() 

            # excecute query
            query = f'SELECT * FROM {self.user_table}'
            cursor.execute(query)

            # fetch result
            result = cursor.fetchall()

            for row in result:
                print(row)

        except: 
            print('Cannot query data')
        finally:
            cursor.close()
    def end_connect(self):
        self.connection.close()

if __name__ == '__main__':
    database = ConnectToPostgres()
    database.get_all_user()
    database.end_connect()
