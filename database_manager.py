import psycopg2
import psycopg2.extras


CONNECTION_STR = "dbname = 'bans' user = 'bans' host = 'localhost' password = 'pass'"


def query_select(sql_str, variables=None, connection_str=CONNECTION_STR):
    try:
        with psycopg2.connect(connection_str) as connection:
            with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(sql_str, variables)
                return cursor.fetchall()
    except psycopg2.DatabaseError as exception:
        print(exception)


def query_modify(sql_str, variables=None, connection_str=CONNECTION_STR):
    print("sql_str in query: ", sql_str)
    try:
        with psycopg2.connect(connection_str) as connection:
            with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(sql_str, variables)
                print(sql_str.split()[0] + " done.")
    except psycopg2.DatabaseError as exception:
        print(exception)


def query_modify_returning(sql_str, variables=None, connection_str=CONNECTION_STR):
    try:
        with psycopg2.connect(connection_str) as connection:
            with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(sql_str, variables)
                return cursor.fetchall()
    except psycopg2.DatabaseError as exception:
        print(exception)
    