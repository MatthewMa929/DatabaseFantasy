document.addEventListener('DOMContentLoaded', function () {
    // I just added sample data
    let leagues = [
        { id: 1, name: 'NBA', type: 'Basketball', maxTeams: 30 },
        { id: 2, name: 'MLS', type: 'Soccer', maxTeams: 29 },
        { id: 3, name: 'NFL', type: 'Football', maxTeams: 32 }
    ];

    const leagueList = document.getElementById('league-list');
    
    function updateTable() {
        leagueList.innerHTML = '';
        leagues.forEach(league => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${league.name}</td>
                <td>${league.type}</td>
                <td>${league.maxTeams}</td>
                <td>
                    <button onclick="editLeague(${league.id})">Edit</button>
                    <button onclick="deleteLeague(${league.id})">Delete</button>
                </td>
            `;
            leagueList.appendChild(row);
        });
    }

    updateTable();

    document.getElementById('add-league-btn').addEventListener('click', function () {
        const leagueName = prompt('Enter League Name');
        const leagueType = prompt('Enter League Type');
        const maxTeams = prompt('Enter Max Teams');

        if (leagueName && leagueType && maxTeams) {
            const newLeague = {
                id: leagues.length + 1,
                name: leagueName,
                type: leagueType,
                maxTeams: parseInt(maxTeams, 10)
            };

            leagues.push(newLeague);
            alert('League added successfully!');
            updateTable();
        } else {
            alert('Please fill all fields');
        }
    });

    window.editLeague = function (id) {
        const league = leagues.find(l => l.id === id);
        if (league) {
            const newName = prompt('Edit League Name', league.name);
            const newType = prompt('Edit League Type', league.type);
            const newMaxTeams = prompt('Edit Max Teams', league.maxTeams);

            if (newName && newType && newMaxTeams) {
                league.name = newName;
                league.type = newType;
                league.maxTeams = parseInt(newMaxTeams, 10);
                alert('League updated successfully!');
                updateTable(); 
            } else {
                alert('Please fill all fields');
            }
        }
    };

    window.deleteLeague = function (id) {
        const index = leagues.findIndex(l => l.id === id);
        if (index > -1) {
            leagues.splice(index, 1);
            alert('League deleted successfully!');
            updateTable();
        }
    };

    const manageTeamsButton = document.getElementById('manage-teams');
    const managePlayersButton = document.getElementById('manage-players');
    const manageLeaguesButton = document.getElementById('manage-leagues');

    manageTeamsButton.addEventListener('click', function () {
        window.location.href = 'manage_teams.html';
    });

    managePlayersButton.addEventListener('click', function () {
        window.location.href = 'manage_players.html';
    });

    manageLeaguesButton.addEventListener('click', function () {
        window.location.href = 'admin_dashboard.html'; 
    });
});

