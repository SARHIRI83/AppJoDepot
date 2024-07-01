import psycopg2
import psycopg2.extras


# Connexion à la base de données
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        dbname='AppJo',
        user='postgres',
        password='sofyane',
    )
    return conn