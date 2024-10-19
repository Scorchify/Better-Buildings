// Function to get CSRF token from meta tag
function getCsrfToken() {
  return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// Function to toggle thumbs-up state
function toggleThumbsUp(reportId) {
  const thumbsUpIcon = document.getElementById(`thumbs-up-${reportId}`);
  const upvotesCount = document.getElementById(`upvotes-${reportId}`);
  const csrfToken = getCsrfToken();

  fetch(`/upvote/${reportId}/`, { // Correct URL pattern
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.upvotes !== undefined) {
      // Update the upvotes count
      upvotesCount.value = data.upvotes;

      // Toggle the thumbs-up icon between outlined and filled
      if (thumbsUpIcon.classList.contains('bi-hand-thumbs-up')) {
        thumbsUpIcon.classList.remove('bi-hand-thumbs-up');
        thumbsUpIcon.classList.add('bi-hand-thumbs-up-fill');
      } else {
        thumbsUpIcon.classList.remove('bi-hand-thumbs-up-fill');
        thumbsUpIcon.classList.add('bi-hand-thumbs-up');
      }

      // Apply animation
      thumbsUpIcon.classList.add('thumbs-up-animate');
      setTimeout(() => {
        thumbsUpIcon.classList.remove('thumbs-up-animate');
      }, 500); // Duration of the animation
    }
  })
  .catch(error => console.error('Error:', error));
}

// Function to set the initial state of thumbs-up icons
function setInitialThumbsUpState() {
  document.querySelectorAll('.thumbs-up-icon').forEach(icon => {
    const reportId = icon.id.split('-')[2];
    fetch(`/report-state/${reportId}/`)
      .then(response => response.json())
      .then(data => {
        if (data.is_upvoted) {
          icon.classList.add('bi-hand-thumbs-up-fill');
          icon.classList.remove('bi-hand-thumbs-up');
        } else {
          icon.classList.add('bi-hand-thumbs-up');
          icon.classList.remove('bi-hand-thumbs-up-fill');
        }
      })
      .catch(error => console.error('Error:', error));
  });
}

// Add click event listeners to thumbs-up icons
document.querySelectorAll('.thumbs-up-icon').forEach(icon => {
  icon.addEventListener('click', function () {
    const reportId = this.id.split('-')[2];
    toggleThumbsUp(reportId);
  });
});

// Set initial state of thumbs-up icons
setInitialThumbsUpState();