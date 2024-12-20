function updateHours(event) {
    event.preventDefault(); // Prevent form submission

    const date = document.getElementById('date').value;
    const openingHours = document.getElementById('opening-hours').value;
    const closingHours = document.getElementById('closing-hours').value;
    
    // Perform update logic here (e.g., send to server via AJAX)
    // For this example, we will just display a confirmation message

    const confirmationMessage = document.getElementById('confirmation-message');
    confirmationMessage.textContent = `Library hours updated for ${date}:\nOpening Hours: ${openingHours}\nClosing Hours: ${closingHours}`;
    confirmationMessage.classList.remove('hidden');
    
    // Clear the form fields
    document.getElementById('update-hours-form').reset();
}
