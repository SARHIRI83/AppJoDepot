from flask import Flask, current_app, render_template, request, jsonify, make_response
from flask_session import Session
import psycopg2
import psycopg2.extras
import os
import hashlib
import random
import string
import json
import logging

# Système de Journalisation pour le suivi du comportement de l'application, la détection et la résolution des erreurs
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


app=Flask(__name__)


# Configuration des sessions
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Positionner à False si vous n'utilisez pas HTTPS
app.config['SESSION_USE_SIGNER'] = True
Session(app)  # Initialiser l'extension Session

#----------------------------------Fonctions-------------------------------------------

# Connexion à la base de données
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        dbname='AppJo',
        user='postgres',
        password='sofyane',
        port=5432 #modifiez le port pour qu'il soit le même que le port d'écoute de votre serveur postgre sql local
    )
    return conn

# Génerer une suite de caractère alphanumériques aléatoire pour la clé de compte et la clé de transaction
def generate_random_string():
    # Déterminer une longueur aléatoire entre 50 et 100
    length = random.randint(50, 100)
    
    # Créer une chaîne de caractères alphanumériques
    characters = string.ascii_letters + string.digits  # Inclut les lettres majuscules, minuscules et les chiffres
    random_string = ''.join(random.choice(characters) for _ in range(length))
    
    return random_string

# Cette fonction enregistre des informations sur les articles ajoutés au panier d'un utilisateur dans un fichier JSON
def save_to_cart(user_id, ticket_type, quantity, image_name, description, price, name):
    file_path = 'cart.json'
    if not os.path.exists(file_path):
        data = {}
    else:
        with open(file_path, 'r') as file:
            data = json.load(file)

    if user_id not in data:
        data[user_id] = {}

    if ticket_type not in data[user_id]:
        # Si le type de billet n'existe pas encore, initialisez-le avec les nouvelles informations
        data[user_id][ticket_type] = {
            'quantity': 0,
            'image_name': image_name,
            'description': description,
            'price': price,  # Ajout du prix ici
            'name': name
        }

    # Mettre à jour la quantité pour ce type de billet
    data[user_id][ticket_type]['quantity'] += quantity
    # On suppose que l'image, la description et le prix ne changent pas. 
    # Si ce n'est pas le cas, il faudrait les mettre à jour ici également.

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Cette fonction charge les articles du panier d'un utilisateur à partir d'un fichier JSON
def load_cart_items(user_id):
    try:
        with open('cart.json', 'r') as file:
            data = json.load(file)
        return data.get(user_id, [])  # Retourne le panier de l'utilisateur ou un panier vide
    except FileNotFoundError:
        return []  # Retourne un panier vide si le fichier n'existe pas
    

# Cette fonction met à jour les informations du panier d'un utilisateur dans un fichier JSON
def update_cart_file(user_id, ticket_type, new_quantity, image_name=None, description=None, price=None):
    file_path = 'cart.json'
    # Chargement des données existantes ou initialisation d'un nouveau dictionnaire
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = {}

    # Accéder au panier de l'utilisateur ou initialiser un nouveau dictionnaire pour cet utilisateur
    user_cart = data.get(user_id, {})

    # Mise à jour ou suppression de l'entrée
    if new_quantity > 0:
        # Mettre à jour ou créer une nouvelle entrée
        user_cart[ticket_type]['quantity'] = new_quantity
    else:
        # Supprimer l'entrée existante si la quantité est zéro ou moins
        del user_cart[ticket_type]

    # Mettre à jour le panier de l'utilisateur dans le dictionnaire principal
    if user_cart:
        data[user_id] = user_cart
    else:
        # Supprimer complètement l'entrée de l'utilisateur si son panier est vide
        data.pop(user_id, None)

    # Sauvegarder les modifications dans le fichier JSON
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


#----------------------------------Routes-------------------------------------------


# page d'acceuil
@app.route("/")
def home():
    return render_template("home.html")

# page avec les billets
@app.route("/billets")
def billets():
    return render_template("billets.html")


# page de connexion
@app.route("/sign_in")
def sign_in():
    if request.cookies.get('is_logged_in') == 'true':
        id=request.cookies.get('user_id')
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT firstname, lastname, email FROM utilisateurs WHERE user_id = %s', (id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            return render_template("profil.html", prenom=user["firstname"], nom=user["lastname"], email=user["email"])
        else:
            return render_template("sign_in.html")
    else:
        return render_template("sign_in.html")
    

# page d'inscription
@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")


# pour enregistrer un nouvel utilisateur depuis la page d'inscription
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    password = data['password']
    salt = os.urandom(16)  # Génère un sel aléatoire de 16 octets
    salt_hex = salt.hex()  # Convertit le sel en hexadécimal pour stockage facile

    # Hash le mot de passe avec le sel
    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()

    # Connexion à la base de données
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    try:
        # Insertion des données de l'utilisateur dans la base de données
        cur.execute(
            'INSERT INTO utilisateurs (firstname, lastname, email, hashed_password, salt, account_key, is_admin) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (data['lastName'], data['firstName'], data['email'], hashed_password, salt_hex, generate_random_string(), False)
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

    return jsonify(message), status_code


#Fonction pour gérer une demande de connexion à un compte utilisateur
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('SELECT user_id, hashed_password, salt FROM utilisateurs WHERE email = %s', (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        hashed_password = hashlib.sha256(bytes.fromhex(user['salt']) + password.encode()).hexdigest()
        if hashed_password == user['hashed_password']:
            resp = make_response(jsonify({'success': True, 'message': 'Connexion réussie'}))
            resp.set_cookie('is_logged_in', 'true', httponly=True, secure=False)  # Set secure=True in production
            resp.set_cookie('user_id', str(user["user_id"]), httponly=True, secure=False)
            return resp
        else:
            return jsonify({'success': False, 'message': 'Mot de passe incorrect'}), 401
    else:
        return jsonify({'success': False, 'message': 'Aucun utilisateur trouvé avec cet email'}), 404


@app.route('/check_login', methods=['GET'])
def check_login():
    if request.cookies.get('is_logged_in') == 'true':
        return jsonify({'is_logged_in': True})
    else:
        return jsonify({'is_logged_in': False})


@app.route('/logout', methods=['GET'])
def logout():
    resp = make_response(jsonify({'success': True, 'message': 'Déconnexion réussie'}))
    resp.set_cookie('is_logged_in', '', expires=0)  # Supprime le cookie
    resp.set_cookie('user_id', '', expires=0)  # Supprime le cookie
    return resp

  
@app.route('/change_password', methods=['POST'])
def change_password():
    data = request.get_json()
    user_id = request.cookies.get('user_id')  # Supposons que nous avons un user_id dans le cookie
    current_password = data['currentPassword']
    new_password = data['newPassword']

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT hashed_password, salt FROM utilisateurs WHERE user_id = %s', (user_id,))
    user = cur.fetchone()

    if user:
        current_hashed = hashlib.sha256(bytes.fromhex(user['salt']) + current_password.encode()).hexdigest()
        if current_hashed == user['hashed_password']:
            new_salt = os.urandom(16).hex()
            new_hashed_password = hashlib.sha256(bytes.fromhex(new_salt) + new_password.encode()).hexdigest()
            cur.execute('UPDATE utilisateurs SET hashed_password = %s, salt = %s WHERE user_id = %s',
                        (new_hashed_password, new_salt, user_id))
            conn.commit()
            message = {'success': True, 'message': 'Mot de passe changé avec succès'}
        else:
            message = {'success': False, 'message': 'Mot de passe actuel incorrect'}
    else:
        message = {'success': False, 'message': 'Utilisateur non trouvé'}

    cur.close()
    conn.close()
    return jsonify(message)


#Ajoute de nouvelles offres au panier
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    ticket_type = data['ticketType']
    quantity = data['quantity']
    #image_name = data['imageName']
    #description = data['description']
    #price = data['price']
    #name = data['name']

    # Récupérer les articles actuellement dans le panier depuis le cookie ou initialiser un nouveau dictionnaire
    cart_items_str = request.cookies.get('cart_items') or '{}'
    cart_items = json.loads(cart_items_str)

    # Ajouter la nouvelle offre au panier
    if ticket_type in cart_items:
        cart_items[ticket_type]['quantity'] += quantity
    else:
        cart_items[ticket_type] = {
            'quantity': quantity
            #'image_name': image_name,
            #'description': description,
            #'price': price,
            #'name': name
        }

    # Création de la réponse HTTP avec un cookie mis à jour
    resp = make_response(jsonify({'message': 'Ajouté avec succès au panier'}))
    resp.set_cookie('cart_items', json.dumps(cart_items))

    return resp, 200

#Mettre à jour l'offre dans le panier sans être connecté
@app.route('/update_cart', methods=['POST'])
def update_cart():
    cartItems = request.get_json().get('cartItems')
    if cartItems is None:
        cartItems = []  # Initialise cartItems si absent
    ticket_type = cartItems['ticketType']
    new_quantity = int(cartItems['newQuantity'])

    # Récupérer les articles actuellement dans le panier depuis le cookie ou initialiser un nouveau dictionnaire
    cart_items = request.cookies.get('cart_items')
    if cart_items:
        cart_items = json.loads(cart_items)
    else:
        cart_items = {}

    # Mettre à jour la quantité de l'article dans le panier
    cart_items[ticket_type] = new_quantity

    # Mettre à jour le cookie avec les nouvelles données du panier
    resp = make_response(jsonify({'success': True, 'message': 'Quantité mise à jour'}))
    resp.set_cookie('cart_items', json.dumps(cart_items))

    return resp

 # Point d'arrivée pour recevoir les articles du panier du client et répondre avec les mêmes articles
#@app.route('/load_cart', methods=['POST'])
# def load_cart():
#     cart_items = request.json.get('cartItems', [])
#     return jsonify(cart_items)
  

#@app.route('/cart')
#def panier():
    user_id = request.cookies.get('user_id')  # Obtenir l'ID de l'utilisateur
    cart_items = load_cart_items(user_id)  # Charger les éléments du panier depuis le fichier JSON
    print("cart_items: ", cart_items)
    return render_template('cart.html', cart_items=cart_items)

@app.route('/cart', methods=['GET', 'POST'])
def panier():
    cart_items = request.get_json().get('cartItems', [])
    print("cart_items: ", cart_items)
    return render_template('cart.html', cart_items=cart_items)


if __name__ == '__main__':
    app.run(debug=True)