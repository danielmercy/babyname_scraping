import psycopg2

def config():
    return psycopg2.connect("dbname='test_db' user='daniel' host='localhost' password='admin' port='5433'")
