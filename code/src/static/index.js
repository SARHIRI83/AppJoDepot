document.addEventListener('DOMContentLoaded', function () {
    const prevButton = document.querySelector('.carousel-control.prev');
    const nextButton = document.querySelector('.carousel-control.next');
    const items = document.querySelectorAll('.carousel-item');
  
    let currentIndex = 0;
  
    function showCurrentItem() {
      // Retire la classe 'active' de tous les éléments
      items.forEach(item => item.classList.remove('active'));
      
      // Ajoute la classe 'active' à l'élément courant
      items[currentIndex].classList.add('active');
    }
  
    prevButton.addEventListener('click', function (event) {
      event.preventDefault();
      currentIndex = (currentIndex + items.length - 1) % items.length;
      showCurrentItem();
    });
  
    nextButton.addEventListener('click', function (event) {
      event.preventDefault();
      currentIndex = (currentIndex + 1) % items.length;
      showCurrentItem();
    });
  
    showCurrentItem(); // Affiche l'élément initial
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
    //updateCartDisplay();

    alert('Article ajouté au panier avec succès!');
}

  document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', function() {
        const ticketItem = this.closest('.card');
        const quantity = 1;
        const ticketType = ticketItem.querySelector('h2').textContent;  // Exemple: "Billet Solo"
        
        addToCart(ticketType, quantity);
   });
});