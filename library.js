/*function for aviablelibrary */
function toggleInfo(roomElement) {
    const info = roomElement.querySelector('.library-info');
    
    // Toggle the display of the library info
    if (info.style.display === 'none' || info.style.display === '') {
        info.style.display = 'block';  // Show the information
    } else {
        info.style.display = 'none';    // Hide the information
    }
}