let radiantPick = ["", "", "", "", ""];
let direPick = ["", "", "", "", ""];

function hero_pick_f(hero_pick, menu, menuItems, heroIcon) {
    hero_pick.addEventListener('click', () => {
        const allMenus = document.querySelectorAll('.menu-1, .menu-2, .menu-3, .menu-4, .menu-5, .menu-6, .menu-7, .menu-8, .menu-9, .menu-10');
        allMenus.forEach(m => {
            if (m !== menu) {
                m.classList.remove('active');
            }
        });

        hero_pick.classList.toggle('active');
        menu.classList.toggle('active');
        hero_pick.setAttribute('aria-expanded', hero_pick.classList.contains('active') ? 'true' : 'false');
    });

    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            const heroName = item.dataset.heroName;
            const heroType = hero_pick.dataset.heroType
            let index = 0

            if (hero_pick.id.length === 11) {
                const pickNumber = Number(hero_pick.id[10])

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
                    radiantPick[index] = heroName;
                } else if (heroType === 'dire') {
                    direPick[index] = heroName;
                }
            } else if (hero_pick.id.length === 12) {
                index = 4
                direPick[index] = heroName;
            }

            const heroImage = item.querySelector('img');
            heroIcon.src = heroImage.src;
            menu.classList.remove('active');
            hero_pick.classList.add('active_pick');
            hero_pick.classList.remove('active');
            hero_pick.setAttribute('aria-expanded', 'false');

        });
    });
}


const sendHeroesButton = document.getElementById('send-heroes-button');
sendHeroesButton.addEventListener('click', () => {
    const data = {
        radiant_heroes: radiantPick,
        dire_heroes: direPick
    };
    sendSelectedHeroes(data, 'api/heroes/');
});

function sendSelectedHeroes(data, endpoint) {
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


function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}


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

for (let i = 1; i <= 10; i++) {
    const heroPickSelector = `#hero-pick-${i}`;
    const menuSelector = `.menu-${i}`;
    const menuItemsSelector = `.menu__item-${i}`;
    const heroIconSelector = `#hero-icon-${i}`;

    const heroPick = document.querySelector(heroPickSelector);
    const menu = document.querySelector(menuSelector);
    const menuItems = document.querySelectorAll(menuItemsSelector);
    const heroIcon = document.querySelector(heroIconSelector);

    hero_pick_f(heroPick, menu, menuItems, heroIcon);
}
