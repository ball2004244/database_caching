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

    def get_user(self, id):
        try:
            # create cursor
            cursor = self.connection.cursor() 

            # excecute query
            query = f'SELECT * FROM {self.user_table} WHERE id=%s'
            cursor.execute(query, (int(id),))

            # fetch result
            result = cursor.fetchone()

            return result

        except: 
            print('Cannot query data')

        finally:
            cursor.close()
            self.connection.close()
            
    def get_all_user(self):
        try:
            cursor = self.connection.cursor() 

            query = f'SELECT * FROM {self.user_table}'
            cursor.execute(query)

            result = cursor.fetchall()

            result = {id: 
                      {'name': name, 
                       'address': address, 
                       'phonenum': phonenum
                       } 
                       for id, name, address, phonenum in result}
            return result

        except: 
            print('Cannot query data')

        finally:
            cursor.close()
            self.connection.close()

    def create_user(self, id, name, address, phonenum):
        try:
            # create cursor
            cursor = self.connection.cursor()

            # excecute query
            query = f'INSERT INTO {self.user_table} (id, name, address, phonenum) VALUES (%s, %s, %s, %s)'
            cursor.execute(query, (int(id), name, address, phonenum))

            # commit to database
            self.connection.commit()

        except:
            print('Cannot insert data')

        finally:
            cursor.close()
            self.connection.close()

    def update_user(self, id, name, address, phonenum):
        try:
            # create cursor
            cursor = self.connection.cursor()

            # excecute query
            query = f'UPDATE {self.user_table} SET name=%s, address=%s, phonenum=%s WHERE id=%s'
            cursor.execute(query, (name, address, phonenum, int(id)))

            # commit to database
            self.connection.commit()

        except:
            print('Cannot update data')

        finally:
            cursor.close()
            self.connection.close()
    
    def delete_user(self, id):
        try:
            # create cursor
            cursor = self.connection.cursor()

            # excecute query
            query = f'DELETE FROM {self.user_table} WHERE id=%s'
            cursor.execute(query, (int(id),))

            # commit to database
            self.connection.commit()

        except:
            print('Cannot delete data')

        finally:
            cursor.close()
            self.connection.close()

database = ConnectToPostgres()

if __name__ == '__main__':
    database.get_all_user()
