(function () {
  var root = document.documentElement;
  var THEME_KEY = 'theme';
  var LANG_KEY = 'lang';

  document.addEventListener('DOMContentLoaded', function () {
    var themeToggle = document.getElementById('theme-toggle');
    var langToggle = document.getElementById('lang-toggle');

    themeToggle.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem(THEME_KEY, next);
    });

    langToggle.addEventListener('click', function () {
      var next = root.getAttribute('data-lang') === 'ru' ? 'en' : 'ru';
      root.setAttribute('data-lang', next);
      root.setAttribute('lang', next);
      localStorage.setItem(LANG_KEY, next);
    });
  });
})();
