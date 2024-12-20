/*function for aviablerooms*/ 
function toggleInfo(roomElement) {
    const info = roomElement.querySelector('.room-info');
    
    // Toggle the display of the room info
    if (info.style.display === 'none' || info.style.display === '') {
        info.style.display = 'block';  // Show the information
    } else {
        info.style.display = 'none';    // Hide the information
    }
}





 
