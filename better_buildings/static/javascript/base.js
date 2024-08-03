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