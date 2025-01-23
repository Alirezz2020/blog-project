/* static/js/navbar.js */
document.getElementById("navbar-toggle").addEventListener("click", function() {
    document.querySelector(".navbar-links").classList.toggle("active");
});
// static/script.js

document.addEventListener('DOMContentLoaded', function () {
  const likeButtons = document.querySelectorAll('.like-btn, .dislike-btn');

  likeButtons.forEach(button => {
    button.addEventListener('click', function () {
      const postId = this.getAttribute('data-post-id');
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

      fetch(`/comments/like/${postId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
      })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            alert(data.like ? 'Liked!' : 'Disliked!');
          } else {
            alert('Something went wrong.');
          }
        })
        .catch(error => console.error('Error:', error));
    });
  });
});
