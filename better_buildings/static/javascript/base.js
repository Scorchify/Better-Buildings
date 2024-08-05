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

  // Add animation to navbar if not already animated
  if (!sessionStorage.getItem('navbarAnimated')) {
    document.querySelector('.navbar').classList.add('animate');
    sessionStorage.setItem('navbarAnimated', 'true');
  }

  // Function to get CSRF token from meta tag
  function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
  }

  // Function to toggle thumbs-up state
  function toggleThumbsUp(reportId) {
    const thumbsUpIcon = document.getElementById(`thumbs-up-${reportId}`);
    const upvotesCount = document.getElementById(`upvotes-${reportId}`);
    const hasUpvoted = thumbsUpIcon.classList.contains('bi-hand-thumbs-up-fill');
    const csrfToken = getCsrfToken();

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
        if (hasUpvoted) {
          thumbsUpIcon.classList.remove('bi-hand-thumbs-up-fill');
          thumbsUpIcon.classList.add('bi-hand-thumbs-up');
        } else {
          thumbsUpIcon.classList.remove('bi-hand-thumbs-up');
          thumbsUpIcon.classList.add('bi-hand-thumbs-up-fill');
        }

        // Trigger animation
        thumbsUpIcon.classList.add('animate-thumb');
        
        thumbsUpIcon.addEventListener('animationend', () => {
          thumbsUpIcon.classList.remove('animate-thumb');
        });
      } else {
        console.error('Failed to upvote:', data.error);
      }
    })
    .catch(error => console.error('Error:', error));
  }

  // Add click event listeners to thumbs-up icons
  document.querySelectorAll('.thumbs-up-icon').forEach(icon => {
    icon.addEventListener('click', function () {
      const reportId = this.id.split('-')[2];
      toggleThumbsUp(reportId);
    });
  });

  // Theme toggle functionality
  const themeToggleButton = document.getElementById('theme-toggle');
  const themeToggleButtonSmall = document.getElementById('theme-toggle-small');
  const themeToggleIcon = document.getElementById('theme-toggle-icon');
  const themeToggleIconSmall = document.getElementById('theme-toggle-icon-small');
  const darkModeClass = 'dark-mode';

  function setTheme(isDarkMode) {
    if (isDarkMode) {
      document.body.classList.add(darkModeClass);
      themeToggleIcon.classList.remove('bi-brightness-high');
      themeToggleIcon.classList.add('bi-moon');
      themeToggleIconSmall.classList.remove('bi-brightness-high');
      themeToggleIconSmall.classList.add('bi-moon');
    } else {
      document.body.classList.remove(darkModeClass);
      themeToggleIcon.classList.remove('bi-moon');
      themeToggleIcon.classList.add('bi-brightness-high');
      themeToggleIconSmall.classList.remove('bi-moon');
      themeToggleIconSmall.classList.add('bi-brightness-high');
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