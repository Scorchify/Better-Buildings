/*JavaScript for aesthetic scripts*/
  document.addEventListener('DOMContentLoaded', function () {
    var textareas = document.querySelectorAll('.input-box');

    textareas.forEach(function (textarea) {
      textarea.style.overflow = 'hidden';
      textarea.style.height = 'auto'; // Reset the height
      textarea.style.height = textarea.scrollHeight + 'px';

      textarea.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
      });
    });
  });

  document.addEventListener('DOMContentLoaded', function () {
    if (!sessionStorage.getItem('navbarAnimated')) {
      document.querySelector('.navbar').classList.add('animate');
      sessionStorage.setItem('navbarAnimated', 'true');
    }
  });

  document.addEventListener('DOMContentLoaded', function () {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
  
    function toggleThumbsUp(reportId) {
      const thumbsUpIcon = document.getElementById(`thumbs-up-${reportId}`);
      const upvotesCount = document.getElementById(`upvotes-${reportId}`);
      
      // Toggle icon state
      if (thumbsUpIcon.classList.contains('bi-hand-thumbs-up')) {
        thumbsUpIcon.classList.remove('bi-hand-thumbs-up');
        thumbsUpIcon.classList.add('bi-hand-thumbs-up-fill');
        thumbsUpIcon.classList.add('filled');
        thumbsUpIcon.style.animation = 'thumbs-up-animation 0.6s ease';
  
        // Send upvote request to server
        fetch(`/upvote/${reportId}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          }
        })
        .then(response => response.json())
        .then(data => {
          if (data.upvotes !== undefined) {
            upvotesCount.value = data.upvotes; // Update the textbox value
          } else {
            console.error('Failed to upvote:', data.error);
          }
        })
        .catch(error => console.error('Error:', error));
      } else {
        thumbsUpIcon.classList.remove('bi-hand-thumbs-up-fill');
        thumbsUpIcon.classList.add('bi-hand-thumbs-up');
        thumbsUpIcon.classList.remove('filled');
        thumbsUpIcon.style.animation = 'thumbs-up-animation 0.6s ease';
      }
  
      setTimeout(() => {
        thumbsUpIcon.style.animation = '';
      }, 600);
    }
  
    // Add click event listeners to thumbs-up icons
    document.querySelectorAll('.thumbs-up-icon').forEach(icon => {
      icon.addEventListener('click', function () {
        const reportId = this.id.split('-')[2];
        toggleThumbsUp(reportId);
      });
    });
  });