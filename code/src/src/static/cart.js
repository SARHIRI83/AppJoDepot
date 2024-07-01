
function processCheckout() {
  // Rediriger vers la page de paiement ou gérer le paiement
  console.log("Processing checkout...");
  window.location.href='http://127.0.0.1:5000/payment'

}

function updateCartDisplay(inputElement) {
  // Récupérer les informations nécessaires
  const ticketType = inputElement.getAttribute('data-ticket-type');
  const newQuantity = parseInt(inputElement.value);
  
  // Vérifier que la quantité est un nombre valide
  if (isNaN(newQuantity) || newQuantity < 0) {
      console.error('Quantité invalide:', newQuantity);
      return;
  }

  // Mettre à jour le localStorage
  let cartItems = JSON.parse(localStorage.getItem('cartItems') || '[]');
    cartItems = cartItems.map(item => {
        if (item.name === ticketType) {
            item.quantity = newQuantity;
        }
        return item;
    }).filter(item => item.quantity > 0); // Supprimer les items dont la quantité est 0

  localStorage.setItem('cartItems', JSON.stringify(cartItems));
  let newCartItems = JSON.parse(localStorage.getItem('cartItems') || '[]');

    fetch('http://127.0.0.1:5000/cart', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({items: newCartItems})
    })
    .then(response => { 
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.text();
    })
    .then(html => {
        document.open();
        document.write(html);
        document.close();
    })
    .catch(error => console.error('Error loading cart items:', error)); 
}

