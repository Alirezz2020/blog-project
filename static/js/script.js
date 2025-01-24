/* static/js/navbar.js */
document.getElementById("navbar-toggle").addEventListener("click", function() {
    document.querySelector(".navbar-links").classList.toggle("active");
});
document.addEventListener('DOMContentLoaded', () => {
    // Highlight current page (if needed dynamically)
    const currentPage = parseInt(document.querySelector('nav').dataset.currentPage, 10); // Adjust selector as needed
    const pageLinks = document.querySelectorAll('.page-link');

    pageLinks.forEach(link => {
        if (parseInt(link.textContent, 10) === currentPage) {
            link.parentElement.classList.add('active');
        }
    });

    // Smooth scroll to top on pagination click
    const paginationLinks = document.querySelectorAll('.pagination a.page-link');
    paginationLinks.forEach(link => {
        link.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    });
});
