document.addEventListener('DOMContentLoaded', function () {
    const players = [
        { name: 'LeBron James', team: 'Los Angeles Lakers', fantasyPoints: 2500 },
        { name: 'Stephen Curry', team: 'Golden State Warriors', fantasyPoints: 2700 },
        { name: 'Kevin Durant', team: 'Brooklyn Nets', fantasyPoints: 2600 }
    ];

    function displayPlayers() {
        const playersList = document.getElementById('players-list');
        playersList.innerHTML = '';
        players.forEach(player => {
            const listItem = document.createElement('li');
            listItem.textContent = `${player.name} (${player.team}) - Fantasy Points: ${player.fantasyPoints}`;
            playersList.appendChild(listItem);
        });
    }

    const addPlayerForm = document.getElementById('add-player-form');
    addPlayerForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const playerName = document.getElementById('player-name').value;
        const playerTeam = document.getElementById('player-team').value;
        const playerStats = parseInt(document.getElementById('player-stats').value, 10);
        if (playerName && playerTeam && playerStats) {
            players.push({ name: playerName, team: playerTeam, fantasyPoints: playerStats });
            displayPlayers();
            document.getElementById('player-name').value = '';
            document.getElementById('player-team').value = '';
            document.getElementById('player-stats').value = '';
        }
    });

    
    const backToDashboardButton = document.getElementById('back-to-dashboard');
    backToDashboardButton.addEventListener('click', function () {
        window.location.href = 'admin_dashboard.html';
    });
    
    displayPlayers();
});

