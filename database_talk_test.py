import timeit
import psycopg2
import psycopg2.extras
from config import config

def create_year_table(year):
    """ create tables in the PostgreSQL database"""
    table_name = f'year_{year}'
    command = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            rank int PRIMARY KEY,
            maleName VARCHAR(255) NOT NULL,
            femaleName VARCHAR(255) NOT NULL
        )
        """
    conn = None
    try:
        # reference the current time
        start = timeit.default_timer()
        # set connecion
        conn = config()
        # set cursor
        cur = conn.cursor()
        # create a table
        cur.execute(command)
        # reference the current time
        end = timeit.default_timer()
        # reference the time table creation end
        time = (end - start) * 1000
        cur.close()
        print(f'++++ Created table {table_name} in {time}ms')
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def table_exists(year):
    # command checks if table exists?
    command = f"""         	
                SELECT to_regclass('public.year_{year}')
           """
    # initialize a connenction variable
    conn = None
    try:
        # set connection
        conn = config()
        # set the cursor
        cur = conn.cursor()
        # execute command
        cur.execute(command)
        # returns true if table exist else false if none
        if bool(cur.fetchone()[0]):
            print(f'!!!! Table with name year_{year} exists')
            return True
        else:
            print(f'!!!! Table with name year_{year} does not exists')
            return False
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def data_exists_in_table(year):
    # command checks if table exists?
    command = f"""
                    SELECT 1
                    FROM year_{year}
                    WHERE rank=1
           """
    # initialize a connenction variable
    conn = None
    try:
        # set connection
        conn = config()
        # set the cursor
        cur = conn.cursor()
        # execute command
        cur.execute(command)
        # returns true if table exist else false if none
        print(f'\n Checking if data exists in table year_{year}')
        if bool(cur.fetchone()[0]):
            print(f'!!!! Sorry data already exists in table year_{year}\n')
            return True
        else:
            print(f'!!!! Data does not exist in table year_{year}')
            return False
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def write_to_table(raw_data):
    connection = config()
    start = timeit.default_timer()
    with connection as conn:
        with conn.cursor() as cursor:
            # create a year table to store the data
            year = raw_data[0]
            create_year_table(year)
            # check if the table exists and then persist raw data
            if table_exists(year) and (data_exists_in_table(year) is not True):
                print('\n Writing data to table')
                # loop through the raw_data and insert each data into the year table
                for i in range(1,len(raw_data)):
                    command = f"""
                        INSERT INTO year_{year} 
                        (rank, maleName, femaleName)
                        VALUES ('{raw_data[i]["rank"]}', '{raw_data[i]["maleName"]}', '{raw_data[i]["femaleName"]}')
                    """

                    cursor.execute(command)
                end = timeit.default_timer()
                time = (end - start) * 1000
                print(f'++++ finished inserting data into table year_{year} in {time}ms\n')
                conn.commit()
                return True
            else:
                return False

