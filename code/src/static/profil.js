function changePassword() {
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    // Envoi des données au serveur
    fetch('http://127.0.0.1:5000/change_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ currentPassword, newPassword })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            document.getElementById('passwordForm').style.display = 'none';
        }
    })
    .catch(error => console.error('Error:', error));
}

document.getElementById('changePasswordBtn').addEventListener('click', function() {
    document.getElementById('passwordForm').style.display = 'block';
});

function logout() {
    fetch('http://127.0.0.1:5000/logout')
    .then(() => {
        window.location.href = 'http://127.0.0.1:5000/sign_in';
    });
}


function commandes() {
    window.location.href = 'http://127.0.0.1:5000/orders';
};