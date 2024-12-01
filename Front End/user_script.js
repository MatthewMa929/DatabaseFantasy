document.addEventListener('DOMContentLoaded', function () {

    // Smaple Data
    const userData = {
        id: 1,
        username: 'johndoe',
        favoriteTeam: 'Los Angeles Lakers',
        fantasyPoints: 2500,
        stats: [
            { player: 'LeBron James', team: 'Los Angeles Lakers', fantasyPoints: 2500 },
            { player: 'Stephen Curry', team: 'Golden State Warriors', fantasyPoints: 2700 },
            { player: 'Kevin Durant', team: 'Phoenix Suns', fantasyPoints: 2600 }
        ]
    };

    document.getElementById('username-display').textContent = `Username: ${userData.username}`;
    document.getElementById('favorite-team-display').textContent = `Favorite Team: ${userData.favoriteTeam}`;
    document.getElementById('fantasy-points-display').textContent = `Total Fantasy Points: ${userData.fantasyPoints}`;

    const statsList = document.getElementById('user-stats-list');
    userData.stats.forEach(stat => {
        const statRow = document.createElement('tr');
        statRow.innerHTML = `
            <td>${stat.player}</td>
            <td>${stat.team}</td>
            <td>${stat.fantasyPoints}</td>
        `;
        statsList.appendChild(statRow);
    });

    document.getElementById('edit-profile-btn').addEventListener('click', function() {
        const newUsername = prompt('Enter new username:', userData.username);
        const newFavoriteTeam = prompt('Enter new favorite team:', userData.favoriteTeam);

        if (newUsername) userData.username = newUsername;
        if (newFavoriteTeam) userData.favoriteTeam = newFavoriteTeam;

        document.getElementById('username-display').textContent = `Username: ${userData.username}`;
        document.getElementById('favorite-team-display').textContent = `Favorite Team: ${userData.favoriteTeam}`;
    });

    document.getElementById('search-player').addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const filteredStats = userData.stats.filter(stat => {
            return stat.player.toLowerCase().includes(searchTerm);
        });

        statsList.innerHTML = '';
        filteredStats.forEach(stat => {
            const statRow = document.createElement('tr');
            statRow.innerHTML = `
                <td>${stat.player}</td>
                <td>${stat.team}</td>
                <td>${stat.fantasyPoints}</td>
            `;
            statsList.appendChild(statRow);
        });
    });

});
