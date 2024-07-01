document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('.login-form');
    const loginButton = document.querySelector('.login-btn');

    loginButton.addEventListener('click', function(event) {
        event.preventDefault(); // Empêcher le formulaire de se soumettre automatiquement

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();

        // Envoi des données au serveur via une requête POST
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: email, password: password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = 'http://127.0.0.1:5000/'; // Rediriger l'utilisateur après succès
            } else {
                alert(data.message); // Afficher l'erreur
            }
        })
        .catch(error => console.error('Error:', error));
    });
});