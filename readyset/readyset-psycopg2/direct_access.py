'''
This module is used to access the database directly using psycopg2
'''

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

import subprocess
import time

class DirectQuery:
    def __init__(self):
        self.username = 'postgres'
        self.password = 'readyset'
        self.host = '127.0.0.1'
        self.port = '5432'
        self.dbname = 'imdb'

        # access postgresql with psql in Window Subsystem for Linux
        self.dbaccess = f'PGPASSWORD={self.password} psql --host={self.host} --port={self.port} --username={self.username} --dbname={self.dbname}'
        self.query_str = '''SELECT * FROM title_basics;'''

    # query and dump the results to a file
    def file_query(self):
        # Run the query using subprocess and dump the results to a file
        subprocess.run(f'{self.dbaccess} -c "{self.query_str}" > data2.txt', shell=True)
    
    # query and print the results to the console
    def query(self):
        # Run the query using subprocess and print the results to the console every iteration using cursor
        cur = subprocess.Popen(f'{self.dbaccess} -c "{self.query_str}"', shell=True, stdout=subprocess.PIPE)
        for line in cur.stdout:
            print(line.decode('utf-8'), end='')
        cur.wait()

    def main(self, query, log_data=False):
        start = time.time()
        self.query_str = query

        if log_data:
            self.query()
        else:
            self.file_query()
            
        end = time.time()
        compute_time = end - start
        print(f'Direct Query took {compute_time} seconds')

        return compute_time

if __name__ == '__main__':
    direct_query = DirectQuery()
    print(direct_query.main(log_data=False))