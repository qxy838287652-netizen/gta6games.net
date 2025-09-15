// 动态加载游戏列表到主页
fetch('./assets/games.json')
  .then(response => response.json())
  .then(games => {
    const gamesContainer = document.getElementById('games-container');
    if (!gamesContainer) return;
    
    games.forEach(game => {
      const gameCard = document.createElement('div');
      gameCard.className = 'game-card rounded-xl overflow-hidden game-card-shadow';
      gameCard.style.backgroundImage = `url('${game.coverImage}')`;
      gameCard.innerHTML = `
        <a href="./games/${game.id}.html" class="block h-full">
          <div class="relative overflow-hidden h-full flex items-center justify-center bg-black bg-opacity-30">
            <div class="text-center text-white p-4">
              <h3 class="text-2xl font-bold mb-2">${game.title}</h3>
              <div class="absolute top-3 right-3 bg-primary text-white text-sm font-medium px-3 py-1 rounded-full">
                Play Now
              </div>
            </div>
          </div>
          <div class="p-5">
            <h3 class="text-xl font-semibold mb-2">${game.title}</h3>
            <p class="text-apple-gray mb-4">${game.description}</p>
            <div class="flex items-center text-sm text-apple-gray">
              <span class="flex items-center mr-4"><i class="fa fa-clock-o mr-1"></i> ${game.year}</span>
              <span class="flex items-center"><i class="fa fa-gamepad mr-1"></i> ${game.engine}</span>
            </div>
          </div>
        </a>
      `;
      gamesContainer.appendChild(gameCard);
    });
  })
  .catch(error => console.error('Error loading games:', error));