import pytest
import app  

# Création de la classe MockRequest pour simuler le comportement de request.get_json() en renvoyant des données JSON
class MockRequest:
    def get_json(self):
        return {
            'cardName': 'SARHIRI Sofyane',
            'cardNumber': '1234567890123456',
            'expiryDate': '12/28',
            'cvv': '123',
            'cartItems': [
                {'name': 'Billet Solo', 'quantity': 1}
            ]
        }

def test_process_payment_success(monkeypatch):
    # Mocker request.get_json() pour retourner des données JSON
    monkeypatch.setattr('app.request.get_json', MockRequest().get_json)

    # Mocker current_user.id pour avoir un attribut id
    class MockCurrentUser:
        id = 1

    monkeypatch.setattr('app.current_user', MockCurrentUser)

    # Mocker get_db_connection par une fonction factice qui renvoie None afin de ne pas dépendre de la base de données
    def mock_get_db_connection():
        return None

    monkeypatch.setattr('app.get_db_connection', mock_get_db_connection)

    # Test de la fonction
    response = app.process_payment()  # Utilisation de app.process_payment

    assert response.status_code == 200  # Réponse envoyé
    
    assert response.data == b'{"success": true}\n'  # Succès Paiement validé

def test_process_payment_invalid_details(monkeypatch):
    # Mocker request.get_json() pour retourner des données JSON vides
    monkeypatch.setattr('app.request.get_json', lambda: {})

    # Test de la fonction
    response = app.process_payment()  

    assert response.status_code == 400
    
    assert response.data == b'{"success": false, "message": "Invalid payment details"}\n'  # Paiement invalide
