/*document.addEventListener('DOMContentLoaded', function() {
  // Fonction pour mettre à jour le contenu du panier
  function updateCartDisplay() {
      const cartList = document.getElementById('cart-items');
      if (cartList) {
          cartList.innerHTML = ''; // Nettoyer le contenu précédent du panier

          const cartItemsJSON = localStorage.getItem('cartItems') || '[]'; // Utilisation de la variable cartItemsJSON

          const cartItems = JSON.parse(cartItemsJSON);

          // Parcourir les articles du panier
          cartItems.forEach(item => {
              // Créer les éléments HTML pour afficher les détails de l'article
              const listItem = document.createElement('li');
              listItem.textContent = `${item.name} - Quantité: ${item.quantity}`;

              // Ajouter l'élément de liste au panier
              cartList.appendChild(listItem);
          });
      }
  }*/

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
      //updateCartDisplay();

      alert('Article ajouté au panier avec succès!');
  }

  document.querySelectorAll('.add-to-cart').forEach(button => {
      button.addEventListener('click', function() {
          const ticketItem = this.closest('.ticket-item');
          const quantity = parseInt(ticketItem.querySelector('.ticket-quantity').value);
          const ticketType = ticketItem.querySelector('h2').textContent;  // Exemple: "Billet Solo"
          
          addToCart(ticketType, quantity);

          
     });

    // Appel initial pour afficher le contenu du panier au chargement de la page
    //updateCartDisplay();
    });
//})

