from flask import Flask, render_template
from flask_session import Session
from flask_login import LoginManager, UserMixin, login_required
import psycopg2
import psycopg2.extras
import logging
import os
import sys
# Ajouter le répertoire 'services' au chemin de recherche des modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'services')))
import services.databaseService as db
import services.offersService as offers
import services.ordersService as orders
import services.ticketService as tickets
import services.authenticationService as authent
import services.cartService as cart

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
    conn = db.get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT user_id, email, is_admin FROM utilisateurs WHERE user_id = %s', (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user:
        return User(user['user_id'], user['email'], 'admin' if user['is_admin'] else 'user')
    return None

# Routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/billets")
def billet():
    return tickets.get_tickets()

@app.route("/sign_in")
def sign_in():
    return authent.sign_in()

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")

@app.route('/register', methods=['POST'])
def register_user():
    return authent.register_user()

@app.route('/login', methods=['POST'])
def login():
    return authent.login()

@app.route('/check_login', methods=['GET'])
def check_login():
    return authent.check_login()

@app.route('/logout', methods=['GET'])
def logout():
    return authent.logout()

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    return authent.change_password()

@app.route('/cart', methods=['GET', 'POST'])
def panier():
    return cart.panier()

# Pour les fonctionnalités administrateur
@app.route('/offers')
@login_required
@authent.admin_required
def getOffers():
    return offers.getOffers()

@app.route('/add_offer', methods=['POST'])
@login_required
@authent.admin_required
def add_offer():
    return offers.add_offer()

@app.route('/get_offer/<int:id>', methods=['GET'])
@login_required
@authent.admin_required
def get_offer_by_id(id):
    return offers.get_offer_by_id(id)

@app.route('/update_offer/<int:id>', methods=['POST'])
@login_required
@authent.admin_required
def update_offer(id):
    return offers.update_offer(id)

@app.route('/delete_offer/<int:id>', methods=['DELETE'])
@login_required
@authent.admin_required
def delete_offer(id):
    return offers.delete_offer(id)

@app.route('/payment')
@login_required
def payment():
    return render_template('payment.html')

@app.route('/process_payment', methods=['POST'])
@login_required
def process_payment():
    return orders.process_payment()

@app.route('/order_summary')
@login_required
def order_summary():
    return orders.order_summary()

@app.route('/orders')
def getOrdersbyClientId() :
    return 0


if __name__ == '__main__':
    app.run(debug=True)
