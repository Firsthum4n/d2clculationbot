       document.addEventListener('DOMContentLoaded', function() {
           const heroPickButtons = document.querySelectorAll('.header-content button');

           heroPickButtons.forEach(button => {

               button.addEventListener('click', () => {

                   const list = document.getElementById(button.getAttribute('aria-controls'));

                   const searchInput = list.querySelector('input#hero-search-' + button.id.split('-')[2]);

                   searchInput.addEventListener('input', () => {

                       const searchTerm = searchInput.value.toLowerCase();

                       const listItems = list.querySelectorAll('li.menu__item-' + button.id.split('-')[2]);

                       listItems.forEach(item => {

                           const heroName = item.getAttribute('data-hero-name').toLowerCase();
                           if (heroName.includes(searchTerm)) {
                               item.style.display = 'block';
                           } else {
                               item.style.display = 'none';
                           }
                       });
                   });
               });
           });
       });