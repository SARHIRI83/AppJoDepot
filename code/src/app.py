import datetime
from flask import Flask, current_app, render_template, request, jsonify, make_response, redirect, url_for
from flask_session import Session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
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

app = Flask(__name__)

# Configuration des sessions
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Positionner à False si vous n'utilisez pas HTTPS
app.config['SESSION_USE_SIGNER'] = True
app.secret_key = 'your_secret_key'  # Ajoutez une clé secrète pour sécuriser les sessions
Session(app)  # Initialiser l'extension Session

# Configuration Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'sign_in'

# Classe User pour Flask-Login
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

# Chargement de l'utilisateur pour Flask-Login
@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT user_id, email, is_admin FROM utilisateurs WHERE user_id = %s', (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user:
        return User(user['user_id'], user['email'], 'admin' if user['is_admin'] else 'user')
    return None

# Connexion à la base de données
def get_db_connection():
    conn = psycopg2.connect(
        host='localhost',
        dbname='appjo',
        user='postgres',
        password='sofyane',
    )
    return conn

# Générer une suite de caractères alphanumériques aléatoire
def generate_random_string():
    length = random.randint(50, 100)
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Convertir les résultats de curseur de tuple en dictionnaire
def tuple_to_dict(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# Vérification des droits administrateur
def admin_required(f):
    @login_required
    def wrap(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'admin':
            return f(*args, **kwargs)
        else:
            return jsonify({'error': 'Unauthorized access'}), 403
    wrap.__name__ = f.__name__
    return wrap













# Routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/billets")
def billets():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, type, nombre_personne, prix, description, image FROM offre')
    offers = tuple_to_dict(cursor)
    print('\n', offers)
    cursor.close()
    conn.close()
    return render_template("billets.html",offers=offers)

@app.route("/sign_in")
def sign_in():
    if current_user.is_authenticated:
        id = current_user.id
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT firstname, lastname, email FROM utilisateurs WHERE user_id = %s', (id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            return render_template("profil.html", prenom=user["firstname"], nom=user["lastname"], email=user["email"])
    return render_template("sign_in.html")

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    password = data['password']
    salt = os.urandom(16)
    salt_hex = salt.hex()
    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
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

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT user_id, email, hashed_password, salt, is_admin FROM utilisateurs WHERE email = %s', (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        hashed_password = hashlib.sha256(bytes.fromhex(user['salt']) + password.encode()).hexdigest()
        if hashed_password == user['hashed_password']:
            user_obj = User(user['user_id'], user['email'], 'admin' if user['is_admin'] else 'user')
            login_user(user_obj)
            return jsonify({'success': True, 'message': 'Connexion réussie'})
        else:
            return jsonify({'success': False, 'message': 'Mot de passe incorrect'}), 401
    else:
        return jsonify({'success': False, 'message': 'Aucun utilisateur trouvé avec cet email'}), 404

@app.route('/check_login', methods=['GET'])
def check_login():
    if current_user.is_authenticated:
        return jsonify({'is_logged_in': True})
    else:
        return jsonify({'is_logged_in': False})

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify({'success': True, 'message': 'Déconnexion réussie'})

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    data = request.get_json()
    current_password = data['currentPassword']
    new_password = data['newPassword']

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT hashed_password, salt FROM utilisateurs WHERE user_id = %s', (current_user.id,))
    user = cur.fetchone()

    if user:
        current_hashed = hashlib.sha256(bytes.fromhex(user['salt']) + current_password.encode()).hexdigest()
        if current_hashed == user['hashed_password']:
            new_salt = os.urandom(16).hex()
            new_hashed_password = hashlib.sha256(bytes.fromhex(new_salt) + new_password.encode()).hexdigest()
            cur.execute('UPDATE utilisateurs SET hashed_password = %s, salt = %s WHERE user_id = %s',
                        (new_hashed_password, new_salt, current_user.id))
            conn.commit()
            message = {'success': True, 'message': 'Mot de passe changé avec succès'}
        else:
            message = {'success': False, 'message': 'Mot de passe actuel incorrect'}
    else:
        message = {'success': False, 'message': 'Utilisateur non trouvé'}

    cur.close()
    conn.close()
    return jsonify(message)

@app.route('/cart', methods=['GET', 'POST'])
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

    conn = get_db_connection()
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

# Pour les fonctionnalités administrateur
@app.route('/offers')
@login_required
@admin_required
def offers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, type, nombre_personne, prix, description, image FROM offre')
    offers = tuple_to_dict(cursor)
    print('\n', offers)
    cursor.close()
    conn.close()
    return render_template('billet_admin.html', offers=offers)

@app.route('/add_offer', methods=['POST'])
@login_required
@admin_required
def add_offer():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO offre (type, nombre_personne, prix, description, image) VALUES (%s, %s, %s, %s, %s)',
                   (data['type'], data['nombre_personne'], data['prix'], data['description'], data['image']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

@app.route('/get_offer/<int:id>', methods=['GET'])
@login_required
@admin_required
def get_offer(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, type, nombre_personne, prix, description, image FROM offre WHERE id = %s', (id,))
    offer = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify({'id': offer[0], 'type': offer[1], 'nombre_personne': offer[2], 'prix': offer[3], 'description': offer[4], 'image': offer[5]})

@app.route('/update_offer/<int:id>', methods=['POST'])
@login_required
@admin_required
def update_offer(id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE offre SET type = %s, nombre_personne = %s, prix = %s, description = %s, image = %s WHERE id = %s',
                   (data['type'], data['nombre_personne'], data['prix'], data['description'], data['image'], id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

@app.route('/delete_offer/<int:id>', methods=['DELETE'])
@login_required
@admin_required
def delete_offer(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM offre WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})




from datetime import datetime

@app.route('/payment')
@login_required
def payment():
    return render_template('payment.html')

@app.route('/process_payment', methods=['POST'])
@login_required
def process_payment():
    data = request.get_json()
    card_name = data['cardName']
    card_number = data['cardNumber']
    expiry_date = data['expiryDate']
    cvv = data['cvv']
    cart_items = data['cartItems']

    if card_name and card_number and expiry_date and cvv and cart_items:
        user_id = current_user.id
        
        conn = get_db_connection()
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

def generate_transaction_key(order_date, offer_id):
    random_string = generate_random_string()
    return f"{order_date.strftime('%Y%m%d%H%M%S')}{offer_id}{random_string}"

@app.route('/order_summary')
@login_required
def order_summary():
    order_details = request.args.get('order_details')
    if order_details:
        orders = json.loads(order_details)
        return render_template('order_summary.html', orders=orders)
    return render_template('order_summary.html', orders=[])

if __name__ == '__main__':
    app.run(debug=True)
