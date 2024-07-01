import psycopg2.extras
import random
import string




# Générer une suite de caractères alphanumériques aléatoire
def generate_random_string():
    length = random.randint(50, 100)
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Convertir les résultats de curseur de tuple en dictionnaire
def tuple_to_dict(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]