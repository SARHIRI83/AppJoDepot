from flask import render_template
import psycopg2.extras
from . import databaseService as db
from . import utilsService as utils

def get_tickets():
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, type, nombre_personne, prix, description, image FROM offre')
    offers = utils.tuple_to_dict(cursor)
    print('\n', offers)
    cursor.close()
    conn.close()
    return render_template("billets.html",offers=offers)