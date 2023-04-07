'''
This module is used to access the database through ReadySet caching layer
'''

import logging
import time
import psycopg2
from argparse import ArgumentParser, RawTextHelpFormatter

class ReadySetQuery:
    def __init__(self):
        self.query_str = '''SELECT * FROM title_basics;'''
    
    # query and dump the results to a file
    def file_query(self, conn):
        with conn.cursor() as cur:
            year = 1980
            cur.execute(
                self.query_str
            )

            with open('data1.txt', 'w') as f:
                f.write(str(cur.description) + ' \n')
                for row in cur:
                    f.write(str(row) + ' \n')
        conn.commit()

    # query and print the results to the console
    def query(self, conn):
        with conn.cursor() as cur:
            year = 1980
            cur.execute(
                self.query_str
            )

            if cur.description is not None:
                print("")
                print("Year:", year)
                rows = cur.fetchall()
                for row in rows:
                    print([str(cell) for cell in row])

        conn.commit()

    def main(self, query, log_data=False):
        start = time.time()
        self.query_str = query
        opt = self.parse_cmdline()
        logging.basicConfig(level=logging.DEBUG if opt.verbose else logging.INFO)
        try:
            db_url = opt.dsn
            conn = psycopg2.connect(db_url)
        except Exception as e:
            logging.fatal("database connection failed")
            logging.fatal(e)
            return

        if log_data:
            self.query(conn)
        else:
            self.file_query(conn)

        conn.close()
        end = time.time()
        compute_time = end - start
        print(f'ReadySet took {compute_time} seconds')
        return compute_time

    def parse_cmdline(self):
        parser = ArgumentParser(description=__doc__,
                                formatter_class=RawTextHelpFormatter)

        parser.add_argument("-v", "--verbose",
                            action="store_true", help="print debug info")

        # parser.add_argument("dsn",
        #                     default=os.environ.get("DATABASE_URL"),
        #                     nargs="?",
        #                     help="""database connection string
        #                     (default: value of the DATABASE_URL env variable)"""
        # )

        parser.add_argument("dsn",
                            default="postgresql://postgres:readyset@127.0.0.1:5433/imdb?sslmode=disable",
                            nargs="?",
                            help="""database connection string
                            (default: value of the DATABASE_URL env variable)"""
        )
        

        opt = parser.parse_args()
        if opt.dsn is None:
            parser.error("database connection string not set")
        return opt

if __name__ == "__main__": 
    readysetquery = ReadySetQuery()
    query = '''
    SELECT title_basics.originaltitle, title_ratings.averagerating
            FROM title_basics
            JOIN title_ratings ON title_basics.tconst = title_ratings.tconst
            WHERE title_basics.startyear = 1960
            AND title_basics.titletype = 'movie'
            AND title_ratings.numvotes > 50000
            ORDER BY title_ratings.averagerating DESC LIMIT 10;
    
    '''
    readysetquery.main(query, log_data=False)

