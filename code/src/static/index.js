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