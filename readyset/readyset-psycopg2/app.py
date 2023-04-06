'''
CASE 1: Querying the database and dumping the results to a file
'''

import logging
import time
import psycopg2
from argparse import ArgumentParser, RawTextHelpFormatter

def query(conn):
    with conn.cursor() as cur:
        year = 1980
        cur.execute(
            '''SELECT * FROM title_basics;'''
        )

        # if cur.description is not None:
        #     print("")
        #     print("Year:", year)
        #     rows = cur.fetchall()
        #     for row in rows:
        #         print([str(cell) for cell in row])

        with open('data.txt', 'w') as f:
            f.write(str(cur.description) + ' \n')
            for row in cur:
                f.write(str(row) + ' \n')
    conn.commit()

def main():
    opt = parse_cmdline()
    logging.basicConfig(level=logging.DEBUG if opt.verbose else logging.INFO)
    try:
        db_url = opt.dsn
        conn = psycopg2.connect(db_url)
    except Exception as e:
        logging.fatal("database connection failed")
        logging.fatal(e)
        return

    query(conn)

    conn.close()

def parse_cmdline():
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
    start = time.time()
    main()
    end = time.time()
    print(f'Query took {end - start} seconds')

'''
CASE 2: Querying the database and printing the results to the console
'''

# import logging
# import time
# import psycopg2
# from argparse import ArgumentParser, RawTextHelpFormatter

# def query(conn):
#     with conn.cursor() as cur:
#         year = 1980
#         cur.execute(
#             '''SELECT * FROM title_basics;'''
#         )

#         if cur.description is not None:
#             print("")
#             print("Year:", year)
#             rows = cur.fetchall()
#             for row in rows:
#                 print([str(cell) for cell in row])

#     conn.commit()

# def main():
#     opt = parse_cmdline()
#     logging.basicConfig(level=logging.DEBUG if opt.verbose else logging.INFO)
#     try:
#         db_url = opt.dsn
#         conn = psycopg2.connect(db_url)
#     except Exception as e:
#         logging.fatal("database connection failed")
#         logging.fatal(e)
#         return

#     query(conn)

#     conn.close()

# def parse_cmdline():
#     parser = ArgumentParser(description=__doc__,
#                             formatter_class=RawTextHelpFormatter)

#     parser.add_argument("-v", "--verbose",
#                         action="store_true", help="print debug info")

#     parser.add_argument("dsn",
#                         default="postgresql://postgres:readyset@127.0.0.1:5433/imdb?sslmode=disable",
#                         nargs="?",
#                         help="""database connection string
#                         (default: value of the DATABASE_URL env variable)"""
#     )
    

#     opt = parser.parse_args()
#     if opt.dsn is None:
#         parser.error("database connection string not set")
#     return opt
    
# if __name__ == "__main__":
#     start = time.time()
#     main()
#     end = time.time()
#     print(f'Query took {end - start} seconds')