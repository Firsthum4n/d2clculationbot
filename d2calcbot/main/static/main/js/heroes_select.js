//функция показа выпадающего меню
function showMenu(heroButton, menu) {
    heroButton.addEventListener('click', () => {
    menu.classList.toggle('active');
});
}

//функция Закрытие меню при клике вне него
function closeMenu(menu, heroButton, heroSearch) {
    document.addEventListener('click', (event) => {
    if (!event.target.closest(heroButton) && !event.target.closest(heroSearch)) {
      menu.classList.remove('active');
    }
  });
}

//функция замены иконки героя
function changeIcon(menuItems, heroButton, menu, heroIcon) {
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
        const newHeroImage = item.querySelector('img');
        heroIcon.src = newHeroImage.src;
        menu.classList.remove('active');
        heroButton.classList.add('active_pick');
        heroButton.classList.remove('active');
    });
});
}



for (let i = 1; i <= 10; i++) {
    const heroPickSelector = `#hero-pick-${i}`;
    const menuSelector = `.menu-${i}`;
    const menuItemsSelector = `.menu__item-${i}`;
    const heroIconSelector = `#hero-icon-${i}`;
    const heroSearchSelector = `#hero-search-${i}`;

    const heroPick = document.querySelector(heroPickSelector);
    const menu = document.querySelector(menuSelector);
    const menuItems = document.querySelectorAll(menuItemsSelector);
    const heroIcon = document.querySelector(heroIconSelector);

    showMenu(heroPick, menu)
    changeIcon(menuItems, heroPick, menu, heroIcon)
    closeMenu(menu, heroPickSelector, heroSearchSelector)

}
