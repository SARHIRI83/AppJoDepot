from flask import render_template, request
import json
from . import databaseService as db


def panier():
    if request.is_json:
        data = request.get_json()
    else:
        cart_data = request.form.get('cart_data')
        if not cart_data:
            return "Invalid data", 400
        data = json.loads(cart_data)
    cart_items = data['items']
    print("\ncart_items: ", cart_items)

    conn = db.get_db_connection()
    cursor = conn.cursor()

    detailed_cart_items = []

    for item in cart_items:
        print('\nitem:', item)
        type_item = item['name']
        quantity = item['quantity']
        cursor.execute("SELECT nombre_personne, prix, description, image FROM offre WHERE type = %s", (type_item,))
        offer = cursor.fetchone()

        if offer:
            nombre_personne, prix, description, image = offer
            detailed_cart_items.append({
                'name': type_item,
                'quantity': quantity,
                'price': prix,
                'description': description,
                'image_name': image,
                'number_of_people': nombre_personne
            })
    print("\n détail:",detailed_cart_items)
    cursor.close()
    conn.close()
    return render_template('cart.html', cart_items=detailed_cart_items)