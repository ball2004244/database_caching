from caching import redis_client

# add user to database
key = f'user:{11}'
redis_client.add_user_to_redis(key, 'Jack', 'Jakarta', '08123456789')

# get user from database
# user = redis_client.get_all_users_from_redis()
# print(user)