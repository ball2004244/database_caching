from caching import redis_client

# add user to database
key = f'user:{20}'
# redis_client.add_user_to_redis(key, 'Jack', 'Jakarta', '08123456789')
redis_client.add_user_to_redis(key, 'New_USER', 'Vietnam', '1234')

# get user from database
# user = redis_client.get_all_users_from_redis()
# print(user)