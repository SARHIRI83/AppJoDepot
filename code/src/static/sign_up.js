document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.registration-form');
    const registerBtn = document.querySelector('.register-btn');

    registerBtn.addEventListener('click', function(event) {
        event.preventDefault(); // Empêcher le formulaire de se soumettre automatiquement

        // Récupération des valeurs du formulaire
        const lastName = document.getElementById('last-name').value.trim();
        const firstName = document.getElementById('first-name').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        // Vérifications
        if (!lastName || !firstName || !email || !password || !confirmPassword) {
            alert('Veuillez remplir tous les champs.');
            return;
        }

        if (password !== confirmPassword) {
            alert('Les mots de passe ne correspondent pas.');
            return;
        }

        if (!validateEmail(email)) {
            alert('Veuillez entrer une adresse email valide.');
            return;
        }

        if (!isSafeInput([lastName, firstName, email, password])) {
            alert('Les entrées contiennent des caractères non valides.');
            return;
        }

        const userData = {
            lastName: lastName,
            firstName: firstName,
            email: email,
            password : password
        };

        // Envoi des données au serveur via une requête POST
        fetch('http://127.0.0.1:5000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            window.location.href = 'http://127.0.0.1:5000/sign_in';
        })
        .catch((error) => {
            console.error('Error:', error);
        });
        // Hashage du mot de passe
        /*const salt = CryptoJS.lib.WordArray.random(128 / 8);
        const hashedPassword = CryptoJS.SHA256(salt + password).toString();

        console.log('Hashed Password:', hashedPassword);
        console.log('Salt:', salt);
        console.log('name:', firstName);
        console.log('lastname:', lastName);
        console.log('mail:', email);
        console.log('passwd:', password);*/
        

        // form.submit(); // Décommentez cette ligne pour soumettre le formulaire après validation
    });

    function validateEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email.toLowerCase());
    }

    function isSafeInput(inputs) {
        const re = /<script|<\/script|<sql|;|--|\*|\//i;
        return !inputs.some(input => re.test(input));
    }
});