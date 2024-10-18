document.addEventListener('DOMContentLoaded', function () {
  // Adjust textarea height based on content
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

  // Theme toggle functionality
  const themeToggleButton = document.getElementById('theme-toggle');
  const themeToggleButtonSmall = document.getElementById('theme-toggle-small');
  const themeToggleIcon = document.getElementById('theme-toggle-icon');
  const themeToggleIconSmall = document.getElementById('theme-toggle-icon-small');
  const darkModeClass = 'dark-mode';

  function setTheme(isDarkMode) {
    if (isDarkMode) {
      document.body.classList.add(darkModeClass);
      themeToggleIcon.classList.remove('bi-brightness-high-fill');
      themeToggleIcon.classList.add('bi-moon-stars-fill');
      themeToggleIconSmall.classList.remove('bi-brightness-high-fill');
      themeToggleIconSmall.classList.add('bi-moon-stars-fill');
      themeToggleButton.classList.add('btn-dark2');
      themeToggleButtonSmall.classList.add('btn-dark2');
      themeToggleButton.classList.remove('btn-light');
      themeToggleButtonSmall.classList.remove('btn-light');
    } else {
      document.body.classList.remove(darkModeClass);
      themeToggleIcon.classList.remove('bi-moon-stars-fill');
      themeToggleIcon.classList.add('bi-brightness-high-fill');
      themeToggleIconSmall.classList.remove('bi-moon-stars-fill');
      themeToggleIconSmall.classList.add('bi-brightness-high-fill');
      themeToggleButton.classList.remove('btn-dark2');
      themeToggleButtonSmall.classList.remove('btn-dark2');
      themeToggleButton.classList.add('btn-light');
      themeToggleButtonSmall.classList.add('btn-light');
    }
  }

  function toggleTheme() {
    const isDarkMode = document.body.classList.toggle(darkModeClass);
    setTheme(isDarkMode);
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
  }

  themeToggleButton.addEventListener('click', toggleTheme);
  themeToggleButtonSmall.addEventListener('click', toggleTheme);

  // Check local storage for theme preference
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    setTheme(savedTheme === 'dark');
  }
});