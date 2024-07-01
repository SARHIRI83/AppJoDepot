// Afficher le formulaire d'ajout
function showAddOfferForm() {
    document.getElementById('offer-form').style.display = 'block';
}

// Ajouter une nouvelle offre
function addOffer() {
    const type = document.getElementById('offer-type').value;
    const nombre_personne = document.getElementById('offer-nombre_personne').value;
    const prix = document.getElementById('offer-prix').value;
    const description = document.getElementById('offer-description').value;
    const image = document.getElementById('offer-image').value;

    fetch('/add_offer', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({type, nombre_personne, prix, description, image})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('Erreur lors de l\'ajout de l\'offre');
        }
    });
}

// Afficher le formulaire de modification
function showEditOfferForm(id) {
    fetch(`/get_offer/${id}`)
    .then(response => response.json())
    .then(data => {
        document.getElementById('edit-offer-id').value = data.id;
        document.getElementById('edit-offer-type').value = data.type;
        document.getElementById('edit-offer-nombre_personne').value = data.nombre_personne;
        document.getElementById('edit-offer-prix').value = data.prix;
        document.getElementById('edit-offer-description').value = data.description;
        document.getElementById('edit-offer-image').value = data.image;

        document.getElementById('edit-offer-form').style.display = 'block';
    });
}

// Modifier une offre existante
function updateOffer() {
    const id = document.getElementById('edit-offer-id').value;
    const type = document.getElementById('edit-offer-type').value;
    const nombre_personne = document.getElementById('edit-offer-nombre_personne').value;
    const prix = document.getElementById('edit-offer-prix').value;
    const description = document.getElementById('edit-offer-description').value;
    const image = document.getElementById('edit-offer-image').value;

    fetch(`/update_offer/${id}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({type, nombre_personne, prix, description, image})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('Erreur lors de la modification de l\'offre');
        }
    });
}

// Supprimer une offre
function deleteOffer(id) {
    if (confirm('Voulez-vous vraiment supprimer cette offre ?')) {
        fetch(`/delete_offer/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert('Erreur lors de la suppression de l\'offre');
            }
        });
    }
}