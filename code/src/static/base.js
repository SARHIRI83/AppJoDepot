/*function loadCart() {
    console.log("toto");
    let cartItems = JSON.parse(localStorage.getItem('cartItems') || '[]');
    console.log('cartItems :', cartItems);

    fetch('http://127.0.0.1:5000/cart', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({items: cartItems})
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
}*/

document.getElementById('cart-button').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the default link behavior

    // Get the cart items from localStorage
    let cartItems = JSON.parse(localStorage.getItem('cartItems') || '[]');

    // Fill the hidden form input with the JSON string
    document.getElementById('cart-data').value = JSON.stringify({items: cartItems});

    // Submit the form
    document.getElementById('cart-form').submit();
});
  

 // Fonction pour ajouter un article au panier
 function addToCart(ticketType, quantity) {
    const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];

    // Vérifier si l'article existe déjà dans le panier
    const existingItem = cartItems.find(item => item.name === ticketType);

    if (existingItem) {
        // Mettre à jour la quantité de l'article existant
        existingItem.quantity += quantity;
    } else {
        // Ajouter un nouvel article au panier
        cartItems.push({ name: ticketType, quantity: quantity });
    }

    // Enregistrer les articles mis à jour dans le localStorage
    localStorage.setItem('cartItems', JSON.stringify(cartItems));
    //localStorage.setItem('cartItemsJSON', JSON.stringify(cartItems)); // Ajout de cette ligne

    // Mettre à jour l'affichage du panier
    updateCartDisplay();

    alert('Article ajouté au panier avec succès!');
}

