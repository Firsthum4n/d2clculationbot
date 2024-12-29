const radiant = {
  team: "",
  heroes: ["", "", "", "", ""]
};

const dire = {
  team: "",
  heroes: ["", "", "", "", ""]
};

//функция записи в словари команд
function teamsInfo(menu, teamButton) {
    menu.addEventListener('click', (event) => {
        const teamName = event.target.closest('li').dataset.teamName;
        const teamButtonId = Number(teamButton.id[19])
        if (teamButtonId === 1) {
            radiant["team"] = teamName
            console.log(radiant)
            console.log(dire)
        }else if (teamButtonId === 2) {
            dire["team"] = teamName
            console.log(radiant)
            console.log(dire)
        }
    });
}

//функция записи в словари героев
function heroesInfo(heroButton, menu, menuItems) {
        menuItems.forEach(item => {
        item.addEventListener('click', () => {
            const heroName = item.dataset.heroName;
            const heroType = heroButton.dataset.heroType
            let index = 0

            if (heroButton.id.length === 11) {
                const pickNumber = Number(heroButton.id[10])

                if (pickNumber === 1 || pickNumber === 2){
                    index = 0
                }else if (pickNumber === 3 || pickNumber === 4){
                    index = 1
                }else if (pickNumber === 5 || pickNumber === 6) {
                    index = 2
                }else if (pickNumber === 7 || pickNumber === 8) {
                    index = 3
                }else if (pickNumber === 9) {
                    index = 4
                }
                if (heroType === 'radiant' ) {
                    radiant["heroes"][index] = heroName;
                    console.log(radiant)
                    console.log(dire)

                } else if (heroType === 'dire') {
                    dire["heroes"][index] = heroName;
                    console.log(radiant)
                    console.log(dire)

                }
            } else if (heroButton.id.length === 12) {
                index = 4
                dire["heroes"][index] = heroName;
                console.log(radiant)
                console.log(dire)
            }

        });
    });
}


//отправляет оба словаря на сервер
const sendHeroesButton = document.getElementById('send-heroes-button');
sendHeroesButton.addEventListener('click', () => {
    const data = {
        radiant_heroes: radiant,
        dire_heroes: dire
    };
    sendSelectedTeamsAndHeroes(data, 'pick/heroes/');
});

//функция отправки словарей
function sendSelectedTeamsAndHeroes(data, endpoint) {
    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify(data),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const calculationResult = document.getElementById("calculation-result");
            calculationResult.textContent = data.result;
            modal.style.display = "block";
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

//Получает значение CSRF-токена из скрытого поля формы
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

//модальное окно
const modal = document.getElementById("calculation-popup");
const btn = document.getElementById("send-heroes-button");
const span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
    modal.style.display = "block";
}

span.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
}













for (let i = 1; i <=2; i++) {
    const teamSelectButtonSelector = `#team-select-button-${i}`;
    const teamSelectMenuSelector =`#team-select-menu-${i}`;

    const teamSelectButton = document.querySelector(teamSelectButtonSelector)
    const teamSelectMenu = document.querySelector(teamSelectMenuSelector)

    teamsInfo(teamSelectMenu, teamSelectButton)
}

for (let i = 1; i <= 10; i++) {
    const heroPickSelector = `#hero-pick-${i}`;
    const menuSelector = `.menu-${i}`;
    const menuItemsSelector = `.menu__item-${i}`;

    const heroPick = document.querySelector(heroPickSelector);
    const menu = document.querySelector(menuSelector);
    const menuItems = document.querySelectorAll(menuItemsSelector);

    heroesInfo(heroPick, menu, menuItems)
}