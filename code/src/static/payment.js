document.getElementById('payment-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const cardName = document.getElementById('card-name').value;
    const cardNumber = document.getElementById('card-number').value;
    const expiryDate = document.getElementById('expiry-date').value;
    const cvv = document.getElementById('cvv').value;

    const cartItems = JSON.parse(localStorage.getItem('cartItems') || '[]');

    if (cardName && cardNumber && expiryDate && cvv) {
        fetch('/process_payment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                cardName,
                cardNumber,
                expiryDate,
                cvv,
                cartItems
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const orderDetails = encodeURIComponent(JSON.stringify(data.order_details));
                window.location.href = `http://localhost:5000/order_summary?order_details=${orderDetails}`;
            } else {
                alert('Erreur lors du traitement du paiement.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        alert('Veuillez remplir tous les champs.');
    }
});