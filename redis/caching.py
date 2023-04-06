import redis
import json 
from database import database
import threading

class ConnectToRedis():
    def __init__(self, host="localhost", port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.connection = self.connect_to_redis()
        self.close_server = False

    def connect_to_redis(self):
        return redis.Redis(host=self.host, port=self.port, db=self.db)

    '''
        CRUD between Postgres and Redis
    '''
    def get_all_users_from_database(self):
        # get data from Postgres and store it in Redis
        try:
            users = database.get_all_user()

            for id, user in users.items():
                # set key using redis convetion
                key = f'user:{id}'
                self.connection.set(key, json.dumps(user))

            return users
        
        except Exception as e:
            print(e)
            return None
    
    def add_user_to_database(self, id, name, address, phonenum):
        # add data to Postgres
        database.create_user(id, name, address, phonenum)
        pass
    
    def delete_user_from_database(self, id):
        # delete data from Postgres
        database.delete_user(id)
        pass 

    def update_user_to_database(self, all_data):
        # bring change from Redis to Postgres
        for id, data in all_data.items():
            sent_data = data 
            sent_data['id'] = id
            print(sent_data)
            database.update_user(sent_data)
        pass
    
    '''
        CRUD between client and Redis
    '''

    def get_user_from_redis(self, id):
        try:
            key = f'user:{id}'
            data = self.connection.get(key)
            data = json.loads(data)
            return data
            
        except Exception as e:
            print(e)
            return None
    
    def get_all_users_from_redis(self):
        # check if any user in Redis
        try:
            all_data = {}
            keys = self.connection.keys(pattern='user:*')
            for key in keys:
                data = self.connection.get(key) 
                data = json.loads(data)

                # decode key from bytes to int
                key = int(key.decode('utf-8').split(':')[1])
                all_data[key] = data
            return all_data
            
        except Exception as e:
            print(e)
            return None
    
    def add_user_to_redis(self, id, name, address, phonenum):
        raw_data = {
            'name': name,
            'address': address,
            'phonenum': phonenum
        }

        # convert data to json
        data = json.dumps(raw_data)
        self.connection.set(id, data)

        pass

    def update_user_in_redis(self, id, name, address, phonenum):
        # update data in Redis
        data = {
            'name': name,
            'address': address,
            'phonenum': phonenum
        }
        self.connection.set(id, data)
        pass

    def delete_user_from_redis(self, id):
        # delete data in Redis
        self.connection.delete(id)
        pass
    
    def delete_cache(self):
        # delete all data in Redis
        self.connection.flushall()
        pass
    
    '''
        Compare data between Postgres and Redis every 60s
        if there is any change, update data in Postgres
        do this using Redis built-in timer
    '''
    def update_data(self):
        print(f'Cache Server is running on port {self.port}')
        print('Listening for changes...')

        # create an infinite loop to check if there is any change in Redis
        # the timer is set to 20s
        def server_loop():
            while True:
                if self.connection.ttl('timer') == -2:
                    data = self.get_all_users_from_redis()
                    self.update_user_to_database(data)
                
                    if self.close_server == True:
                        self.end_connection()
                        break

                    # reset timer
                    self.connection.set('timer', 'update')
                    self.connection.expire('timer', 20)

        def end_server():
            # check for user input to break out the previous loop
            user_input = input('Press any key to stop the server: ')
            if user_input:
                self.close_server = True

        # create a thread to run the server loop
        server_thread = threading.Thread(target=server_loop)
        server_thread.start()

        # create a thread to run get the ending signal
        end_signal = threading.Thread(target=end_server)
        end_signal.start()
        

    def end_connection(self):
        database.close_connection()
        self.delete_cache()
        self.connection.close()
        print('Server stopped')

redis_client = ConnectToRedis()

if __name__ == "__main__":
    redis_client.update_data()

