var sidenav=document.querySelector(".side-navbar")

function shownav()
{
    sidenav.style.left="0"
}
function closenav()
{
    sidenav.style.left="-60%"
}
 // Function to toggle dropdown menus
 function toggleDropdown(id) {
    const dropdown = document.getElementById(id);
    dropdown.classList.toggle('show'); // Add or remove the "show" class
}
function shownav() {
    const navbarLinks = document.querySelector('.navbar-links');
    navbarLinks.classList.toggle('active');
}

