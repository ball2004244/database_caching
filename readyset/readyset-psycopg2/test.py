'''
Query:
cur.execute(
            """SELECT title_basics.originaltitle, title_ratings.averagerating
            FROM title_basics
            JOIN title_ratings ON title_basics.tconst = title_ratings.tconst
            WHERE title_basics.startyear = %s
            AND title_basics.titletype = %s
            AND title_ratings.numvotes > %s
            ORDER BY title_ratings.averagerating DESC LIMIT 10""",
            (year, 'movie', 50000)
        )

Access DB with psql in WSL: PGPASSWORD=readyset psql --host=127.0.0.1 --port=5432 --username=postgres --dbname=imdb
'''
'''
CASE 1: Querying the database and dumping the results to a file
'''

import time
import subprocess

password = 'readyset'
host = '127.0.0.1'
port = '5432'
username = 'postgres'   
dbname = 'imdb'

# access postgresql with psql in Window Subsystem for Linux
command = f'PGPASSWORD={password} psql --host={host} --port={port} --username={username} --dbname={dbname}'
query = '''SELECT * FROM title_basics;'''

# Run the query using subprocess and dump the results to a file
start = time.time()
subprocess.run(f'{command} -c "{query}" > data.txt', shell=True)
end = time.time()
print(f'Query took {end - start} seconds')

'''
CASE 2: Querying the database and printing the results to the console
'''

# import time
# import subprocess

# password = 'readyset'
# host = '127.0.0.1'
# port = '5432'
# username = 'postgres'   
# dbname = 'imdb'

# # access postgresql with psql in Window Subsystem for Linux
# command = f'PGPASSWORD={password} psql --host={host} --port={port} --username={username} --dbname={dbname}'
# query = '''SELECT * FROM title_basics;'''

# # Run the query using subprocess and print the results to the console every iteration using cursor
# start = time.time()
# cur = subprocess.Popen(f'{command} -c "{query}"', shell=True, stdout=subprocess.PIPE)
# for line in cur.stdout:
#     print(line.decode('utf-8'), end='')
# end = time.time()
# print(f'Query took {end - start} seconds')
