import os
import psycopg2
import psycopg2.extras
import hashlib
import random
import string

LASTNAME="ADMIN"
FIRSTNAME="admin"
EMAIL="admin@gmail.com"
PASSWORD="Admin1234"

def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        dbname='appjo',
        user='postgres',
        password='sofyane',
    )
    return conn

def register_user():

    salt = os.urandom(16)  # Génère un sel aléatoire de 16 octets
    salt_hex = salt.hex()  # Convertit le sel en hexadécimal pour stockage facile

    # Hash le mot de passe avec le sel
    hashed_password = hashlib.sha256(salt + PASSWORD.encode()).hexdigest()

    # Connexion à la base de données
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    try:
        # Insertion des données de l'utilisateur dans la base de données
        cur.execute(
            'INSERT INTO utilisateurs (firstname, lastname, email, hashed_password, salt, account_key, is_admin) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (LASTNAME, FIRSTNAME, EMAIL, hashed_password, salt_hex, generate_random_string(), True)
        )
        conn.commit()
        message = {'message': 'User registered successfully'}
        status_code = 201
    except psycopg2.IntegrityError as e:
        conn.rollback()
        message = {'error': 'User with this email already exists.'}
        status_code = 400
    except Exception as e:
        conn.rollback()
        message = {'error': str(e)}
        status_code = 500
    finally:
        cur.close()
        conn.close()


def generate_random_string():
    # Déterminer une longueur aléatoire entre 50 et 100
    length = random.randint(50, 100)
    
    # Créer une chaîne de caractères alphanumériques
    characters = string.ascii_letters + string.digits  # Inclut les lettres majuscules, minuscules et les chiffres
    random_string = ''.join(random.choice(characters) for _ in range(length))
    
    return random_string

register_user()