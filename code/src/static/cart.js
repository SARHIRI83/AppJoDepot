function updateQuantity(element) {
    const ticketType = element.dataset.ticketType;
    const newQuantity = element.value;

    fetch('http://127.0.0.1:5000/update_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ticketType, newQuantity })
    })
    .then(response => response.json())
    .then(data => {
        //alert(data.message);
        if (data.success) {
            window.location.reload();  // Recharger la page pour refléter la nouvelle quantité
        }
    })
    .catch(error => console.error('Error:', error));
}

function processCheckout() {
    // Rediriger vers la page de paiement ou gérer le paiement
    console.log("Processing checkout...");
}