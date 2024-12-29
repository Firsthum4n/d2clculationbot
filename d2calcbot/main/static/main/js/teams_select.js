//функция показа выпадающего меню
function showMenu(teamButton, menu) {
    teamButton.addEventListener('click', () => {
    menu.classList.toggle('active');
});
}


// Закрытие меню при клике вне него
function closeMenu(menu) {
    document.addEventListener('click', (event) => {
    if (!event.target.closest('.team-selector')) {
      menu.classList.remove('active');
    }
  });
}


//функция заменяющая текст: "выбери команду" на картинку команды
function changeIcon(teamButton, menu) {
    menu.addEventListener('click', (event) => {

    const teamName = event.target.closest('li').dataset.teamName;
    const teamLogo = event.target.closest('li').dataset.teamLogo;

    teamButton.innerHTML = `<img src="${teamLogo}" alt="${teamName}" width="30" height="30">`;
    menu.classList.remove('active');

  });
}


for (let i = 1; i <=2; i++) {
  const teamSelectButtonSelector = `#team-select-button-${i}`;
  const teamSelectMenuSelector =`#team-select-menu-${i}`;

  const teamSelectButton = document.querySelector(teamSelectButtonSelector)
  const teamSelectMenu = document.querySelector(teamSelectMenuSelector)

  showMenu(teamSelectButton, teamSelectMenu)
  closeMenu(teamSelectMenu)
  changeIcon(teamSelectButton, teamSelectMenu)


}