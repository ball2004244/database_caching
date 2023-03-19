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
        
    def get_all_user(self):
        try:
            cursor = self.connection.cursor() 

            query = f'SELECT * FROM {self.user_table}'
            cursor.execute(query)

            result = cursor.fetchall()
            cursor.close()
            result = {id: 
                      {'name': name, 
                       'address': address, 
                       'phonenum': phonenum
                       } 
                       for id, name, address, phonenum in result}
            return result

        except: 
            print('Cannot query data')


    def create_user(self, id, name, address, phonenum):
        try:
            # create cursor
            cursor = self.connection.cursor()

            # excecute query
            query = f'INSERT INTO {self.user_table} (id, name, address, phone_number) VALUES (%s, %s, %s, %s)'
            cursor.execute(query, (int(id), name, address, phonenum))

            # commit to database
            self.connection.commit()
            cursor.close()
            
        except Exception as e:
            print('Cannot insert data')
            print(e)

    def update_user(self, data):
        try:
            # data manipulation
            id = data['id']
            name = data['name']
            address = data['address']
            phonenum = data['phonenum']

            # create cursor
            cursor = self.connection.cursor()

            # check if id exist, if not, navigate to create_user
            query = f'SELECT * FROM {self.user_table} WHERE id=%s'
            cursor.execute(query, (int(id),))
            result = cursor.fetchone()

            if result == None:
                self.create_user(id, name, address, phonenum)
                return
            

            # excecute query
            query = f'UPDATE {self.user_table} SET name=%s, address=%s, phone_number=%s WHERE id=%s'
            cursor.execute(query, (name, address, phonenum, int(id)))

            # commit to database
            self.connection.commit()
            cursor.close()

        except Exception as e:
            print('Cannot update data')
            print(e)
    
    def delete_user(self, id):
        try:
            # create cursor
            cursor = self.connection.cursor()

            # excecute query
            query = f'DELETE FROM {self.user_table} WHERE id=%s'
            cursor.execute(query, (int(id),))

            # commit to database
            self.connection.commit()
            cursor.close()
        except:
            print('Cannot delete data')

    def close_connection(self):
        self.connection.close()

database = ConnectToPostgres()

if __name__ == '__main__':
    # users = database.get_all_user()
    # database.create_user(9, 'test', 'test', 'test')
    database.update_user({'id': 14, 'name': 'test', 'address': 'test', 'phonenum': 'n0_test'})

    # database.close_connection()
