// Fonction pour mettre à jour le contenu du panier
function updateCartDisplay() {
  const cartContainer = document.getElementById('cart-items');
  cartContainer.innerHTML = ''; // Nettoyer le contenu précédent du panier

  const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];

  // Parcourir les articles du panier
  cartItems.forEach(item => {
      // Créer les éléments HTML pour afficher les détails de l'article
      const cartItem = document.createElement('div');
      cartItem.classList.add('cart-item');

      const itemImage = document.createElement('div');
      itemImage.classList.add('item-image');
      const img = document.createElement('img');
      // Remplacer par une image par défaut si nécessaire, car 'image_name' n'est pas disponible
      img.src = item.image_name || 'default-image.jpg';
      img.alt = item.name;
      itemImage.appendChild(img);

      const itemDetails = document.createElement('div');
      itemDetails.classList.add('item-details');
      const itemName = document.createElement('h2');
      itemName.textContent = item.name;
      const itemDescription = document.createElement('p');
      itemDescription.textContent = item.description || 'Description non disponible'; // Remplacer par une description par défaut si nécessaire
      const itemPrice = document.createElement('p');
      itemPrice.textContent = `Prix unitaire: €${item.price}`;

      itemDetails.appendChild(itemName);
      itemDetails.appendChild(itemDescription);
      itemDetails.appendChild(itemPrice);

      const quantityInput = document.createElement('input');
      quantityInput.type = 'number';
      quantityInput.value = item.quantity;
      quantityInput.min = '0';
      quantityInput.dataset.ticketType = item.name;
      quantityInput.classList.add('quantity-input');
      quantityInput.addEventListener('change', function() {
          updateQuantity(this);
      });

      const subtotal = document.createElement('p');
      subtotal.textContent = `Sous-total: €${item.price * item.quantity}`;

      cartItem.appendChild(itemImage);
      cartItem.appendChild(itemDetails);
      cartItem.appendChild(quantityInput);
      cartItem.appendChild(subtotal);

      cartContainer.appendChild(cartItem);
  });
}

// Fonction pour mettre à jour la quantité d'un article
function updateQuantity(inputElement) {
  const ticketType = inputElement.dataset.ticketType;
  const newQuantity = parseInt(inputElement.value);

  let cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
  const item = cartItems.find(item => item.name === ticketType);

  if (item) {
      item.quantity = newQuantity;

      if (item.quantity <= 0) {
          cartItems = cartItems.filter(item => item.name !== ticketType);
      }

      localStorage.setItem('cartItems', JSON.stringify(cartItems));
      updateCartDisplay();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const cartItems = JSON.parse(localStorage.getItem('cartItems') || '[]');
  fetch('http://127.0.0.1:5000/cart', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},     
      body: JSON.stringify({ items: cartItems })
  })
  .then(response => response.json())
  .then(cartItems => {
      updateCartDisplay(cartItems);
  })
  .catch(error => console.error('Error loading cart items:', error));
});

function processCheckout() {
  // Rediriger vers la page de paiement ou gérer le paiement
  console.log("Processing checkout...");
}