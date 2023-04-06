import psycopg2

class ConnectToPostgres():
    def __init__(self):
        self.connection = psycopg2.connect(
            host='localhost',
            port='5432',
            dbname='imdb',
            user='postgres',
            password='12345678'
        )

    def query(self):
        with self.connection.cursor() as cur:
            year = 1980
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

            if cur.description is not None:
                print("")
                print("Year:", year)
                rows = cur.fetchall()
                for row in rows:
                    print([str(cell) for cell in row])

        self.connection.commit()

if __name__ == "__main__":
    database = ConnectToPostgres()
    print(database)
    # database.query()
