from flask import render_template, request, jsonify
from flask_login import UserMixin, login_user, logout_user, login_required, current_user
import psycopg2
import psycopg2.extras
import os
import hashlib
from . import databaseService as db
from . import utilsService as utils

# Classe User pour Flask-Login
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

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

def sign_in():
    if current_user.is_authenticated:
            id = current_user.id
            conn = db.get_db_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute('SELECT firstname, lastname, email FROM utilisateurs WHERE user_id = %s', (id,))
            user = cur.fetchone()
            cur.close()
            conn.close()
            if user:
                return render_template("profil.html", prenom=user["firstname"], nom=user["lastname"], email=user["email"])
    return render_template("sign_in.html")

def register_user():
    data = request.get_json()
    password = data['password']
    salt = os.urandom(16)
    salt_hex = salt.hex()
    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()

    conn = db.get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute(
            'INSERT INTO utilisateurs (firstname, lastname, email, hashed_password, salt, account_key, is_admin) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (data['lastName'], data['firstName'], data['email'], hashed_password, salt_hex, utils.generate_random_string(), False)
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

def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    conn = db.get_db_connection()
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

def check_login():
    if current_user.is_authenticated:
        return jsonify({'is_logged_in': True})
    else:
        return jsonify({'is_logged_in': False}) 

def logout():
    logout_user()
    return jsonify({'success': True, 'message': 'Déconnexion réussie'})

def change_password():
    data = request.get_json()
    current_password = data['currentPassword']
    new_password = data['newPassword']

    conn = db.get_db_connection()
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