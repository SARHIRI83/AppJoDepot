document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', function() {
      const ticketItem = this.closest('.ticket-item');
      const quantity = parseInt(ticketItem.querySelector('.ticket-quantity').value);
      const ticketType = ticketItem.querySelector('h2').textContent;  // Exemple: "Billet Solo"
  
      fetch('http://127.0.0.1:5000/add_to_cart', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ ticketType, quantity })
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message);  // Notification de réussite ou d'erreur
      })
      .catch(error => console.error('Error:', error));
    });
  });