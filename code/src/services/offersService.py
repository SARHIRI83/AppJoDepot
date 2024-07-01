from flask import render_template, request, jsonify
import psycopg2.extras
from . import databaseService as db
from . import utilsService as utils

def get_offre_by_name(name):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT prix FROM offre WHERE type = %s", (name,))
    offre = cursor.fetchone()
    cursor.close()
    conn.close()
    return offre

def getOffers():
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, type, nombre_personne, prix, description, image FROM offre')
    offers = utils.tuple_to_dict(cursor)
    print('\n', offers)
    cursor.close()
    conn.close()
    return render_template('billet_admin.html', offers=offers)

def get_offer_by_id(id):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, type, nombre_personne, prix, description, image FROM offre WHERE id = %s', (id,))
    offer = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify({'id': offer[0], 'type': offer[1], 'nombre_personne': offer[2], 'prix': offer[3], 'description': offer[4], 'image': offer[5]})

def add_offer():
    data = request.get_json()
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO offre (type, nombre_personne, prix, description, image) VALUES (%s, %s, %s, %s, %s)',
                   (data['type'], data['nombre_personne'], data['prix'], data['description'], data['image']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

def update_offer(id):
    data = request.get_json()
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE offre SET type = %s, nombre_personne = %s, prix = %s, description = %s, image = %s WHERE id = %s',
                   (data['type'], data['nombre_personne'], data['prix'], data['description'], data['image'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

def delete_offer(id):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM offre WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})
