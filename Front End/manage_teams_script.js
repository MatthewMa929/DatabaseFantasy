document.addEventListener('DOMContentLoaded', function () {
    const teams = [
        { name: 'Los Angeles Lakers', league: 'NBA', players: 15 },
        { name: 'Golden State Warriors', league: 'NBA', players: 15 },
        { name: 'Brooklyn Nets', league: 'NBA', players: 15 }
    ];

    function displayTeams() {
        const teamsList = document.getElementById('teams-list');
        teamsList.innerHTML = '';
        teams.forEach(team => {
            const listItem = document.createElement('li');
            listItem.textContent = `${team.name} (League: ${team.league}) - Players: ${team.players}`;
            teamsList.appendChild(listItem);
        });
    }

    
    const addTeamForm = document.getElementById('add-team-form');
    addTeamForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const teamName = document.getElementById('team-name').value;
        const teamLeague = document.getElementById('team-league').value;
        const teamPlayers = parseInt(document.getElementById('team-players').value, 10);
        if (teamName && teamLeague && teamPlayers) {
            teams.push({ name: teamName, league: teamLeague, players: teamPlayers });
            displayTeams();
            document.getElementById('team-name').value = '';
            document.getElementById('team-league').value = '';
            document.getElementById('team-players').value = '';
        }
    });

    
    const backToDashboardButton = document.getElementById('back-to-dashboard');
    backToDashboardButton.addEventListener('click', function () {
        window.location.href = 'admin_dashboard.html';
    });

    displayTeams();
});

