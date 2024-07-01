from datetime import datetime
from flask import render_template, request, jsonify
from flask_login import current_user
import psycopg2.extras
import json
import urllib.parse
import databaseService as db
from . import utilsService as utils
from . import offersService as offers

def generate_transaction_key(order_date, offer_id):
    random_string = utils.generate_random_string()
    return f"{order_date.strftime('%Y%m%d%H%M%S')}{offer_id}{random_string}"

def process_payment():
    data = request.get_json()
    card_name = data['cardName']
    card_number = data['cardNumber']
    expiry_date = data['expiryDate']
    cvv = data['cvv']
    cart_items = data['cartItems']

    if card_name and card_number and expiry_date and cvv and cart_items:
        user_id = current_user.id
        
        conn = db.get_db_connection()
        cursor = conn.cursor()
        order_details = []

        for item in cart_items:
            cursor.execute('SELECT id, prix FROM offre WHERE type = %s', (item['name'],))
            result = cursor.fetchone()
            if result:
                offer_id = result[0]
                price = result[1]
                ticket_number = item['quantity']
                order_status = 'paid'
                amount = price * ticket_number
                order_date = datetime.now()
                payment_method = 'Credit Card'
                payment_date = order_date
                transaction_key = generate_transaction_key(order_date, offer_id)

                cursor.execute('INSERT INTO commande (user_id, offer_id, ticket_number, order_status, order_date, amount, payment_method, payment_date, transaction_key) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id',
                               (user_id, offer_id, ticket_number, order_status, order_date, amount, payment_method, payment_date, transaction_key))
                
                
                order_id = cursor.fetchone()[0]
                order_details.append({
                    'id': order_id,
                    'offer_id': offer_id,
                    'ticket_number': ticket_number,
                    'order_date': order_date,
                    'amount': amount,
                    'payment_method': payment_method,
                    'payment_date': payment_date,
                    'transaction_key': transaction_key,
                    'type': item['name'],
                    'price': price
                })
        
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid payment details'}), 400
    

def order_summary():
    order_details = request.args.get('order_details')
    if order_details:
        try:
            # Décoder les caractères spéciaux dans l'URL
            decoded_order_details = urllib.parse.unquote(order_details)
            print("decoded_url : ", decoded_order_details)

            # Convertir la chaîne JSON en objet Python
            orders = json.loads(decoded_order_details)
            print("commande : ", orders)  # Log pour vérifier le contenu après json.loads

            date=datetime.now()
            payment_date = date.strftime("%d/%m/%Y")

            # Enrichir les données avec les prix unitaires et les prix totaux
            for order in orders:
                offre = offers.get_offre_by_name(order['name'])
                if offre:
                    unit_price = offre[0]  # Récupérer le prix unitaire depuis le tuple
                    order['unit_price'] = unit_price
                    order['total_price'] = order['quantity'] * unit_price
                else:
                    order['unit_price'] = 0
                    order['total_price'] = 0

            return render_template('order_summary.html', orders=orders, date=payment_date)
        except json.JSONDecodeError:
            print("erreur pendant le json.load")
            return render_template('order_summary.html', orders=[], error="Erreur de décodage JSON")
    return render_template('order_summary.html', orders=[])