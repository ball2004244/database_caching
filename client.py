from caching import redis_client


users = redis_client.get_all_users()
print(users)