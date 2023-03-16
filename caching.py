import redis
import json 
from database import database

class ConnectToRedis():
    def __init__(self, host="localhost", port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.connection = self.connect_to_redis()

    def connect_to_redis(self):
        return redis.Redis(host=self.host, port=self.port, db=self.db)

    '''
        CRUD between Postgres and Redis
    '''
    def get_user_from_database(self):
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
    
    def add_user_to_database(self, new_data):
        # compare data between Redis and Postgres
        # then update data in Postgres if there is any change
        data = self.get_user_from_database()
        if data != new_data:
            name = new_data['name']
            address = new_data['address']
            phonenum = new_data['phonenum']
            database.update_user(id, name, address, phonenum)
        pass
    
    def delete_user_from_database(self, id):
        # delete data from Postgres
        database.delete_user(id)
        pass 

    def update_user_to_database(self, id, name, address, phonenum):
        # bring change from Redis to Postgres
        database.update_user(id, name, address, phonenum)
        pass
    
    '''
        CRUD between client and Redis
    '''

    def get_user_from_redis(self, id):
        try:
            key = f'user:{id}'
            data = self.connection.get(key)
            if not data:
                data = self.get_user_from_database()
                return data
            else:
                data = json.loads(data)
                return data
            
        except Exception as e:
            print(e)
            return None
    
    def get_all_users(self):
        # check if any user in Redis
        # if not, get all data from Postgres and store it in Redis
        # then return all data
        # the user key is saved as f'user:id'
        try:
            users = self.connection.keys('user:*')
            if not users:
                users = self.get_user_from_database()
                return users
            else:
                output = {}
                for user in users:
                    data = self.connection.get(user)
                    data = json.loads(data)
                    output[user] = data
                return output
            
        except Exception as e:
            print(e)
            return None
    
    def add_user_to_redis(self, id, name, address, phonenum):
        # compare date between client and Redis
        # if the exact data exists in Redis, return None
        # else, add data to Redis
        self.connection.set(id, (name, address, phonenum))
        pass

    def update_user_in_redis(self, id, name, address, phonenum):
        # update data in Redis
        self.connection.set(id, (name, address, phonenum))
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
        # update data in Postgres after 60s
        # create a timer in Redis and set to 60s
        # check if timer is expired
        # if it is, then loop through all data in Redis
        # then push all data to Postgres
        while True:
            if self.connection.ttl('timer') == -2:
                data = self.get_all_users()
                for id, user in data.items():
                    name = user['name']
                    address = user['address']
                    phonenum = user['phonenum']
                    self.update_user_to_database(id, name, address, phonenum)
                # reset timer
                self.connection.set('timer', 'update')
                self.connection.expire('timer', 60)
            else:
                break
        pass

redis_client = ConnectToRedis()

if __name__ == "__main__":
    all_data = redis_client.get_all_users()
    print(all_data)
    # redis_client.update_data()

