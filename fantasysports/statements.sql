CREATE TABLE user_data (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'read_only'
);

INSERT INTO user_data (full_name, email, username, password, role)
VALUES
('John Doe', 'johndoe@example.com', 'johndoe', 'password123', 'admin'),
('Jane Smith', 'janesmith@example.com', 'janesmith', 'securepass321', 'read_only'),
('Admin User', 'admin@example.com', 'adminuser', 'adminpass456', 'admin');


CREATE TABLE player (
    player_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    sport VARCHAR(50) NOT NULL,
    real_team VARCHAR(100),
    position VARCHAR(50),
    fantasy_points INT DEFAULT 0,
    availability_status VARCHAR(20)
);

INSERT INTO player (full_name, sport, real_team, position, fantasy_points, availability_status)
VALUES
('LeBron James', 'Basketball', 'Los Angeles Lakers', 'Forward', 2500, 'Available'),
('Lionel Messi', 'Soccer', 'Inter Miami', 'Forward', 3200, 'Available'),
('Tom Brady', 'Football', 'Tampa Bay Buccaneers', 'Quarterback', 2900, 'Retired'),
('Serena Williams', 'Tennis', 'N/A', 'Singles', 1500, 'Retired'),
('Sidney Crosby', 'Hockey', 'Pittsburgh Penguins', 'Center', 2100, 'Available'),
('Shohei Ohtani', 'Baseball', 'Los Angeles Angels', 'Pitcher', 3100, 'Available'),
('Kevin Durant', 'Basketball', 'Phoenix Suns', 'Forward', 2600, 'Available'),
('Cristiano Ronaldo', 'Soccer', 'Al Nassr', 'Forward', 3000, 'Available'),
('Roger Federer', 'Tennis', 'N/A', 'Singles', 1700, 'Retired'),
('Stephen Curry', 'Basketball', 'Golden State Warriors', 'Guard', 2700, 'Available');

CREATE TABLE team (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    total_points_scored INT DEFAULT 0,
    ranking INT,
    status VARCHAR(20)
);

INSERT INTO team (team_name, total_points_scored, ranking, status)
VALUES
('Los Angeles Lakers', 10200, 1, 'Active'),
('Inter Miami', 8500, 2, 'Active'),
('Tampa Bay Buccaneers', 7600, 3, 'Active'),
('Phoenix Suns', 9100, 4, 'Active');

CREATE TABLE league (
    league_id SERIAL PRIMARY KEY,
    league_name VARCHAR(100) NOT NULL,
    league_type VARCHAR(50),
    draft_date DATE,
    max_teams INT DEFAULT 10
);

INSERT INTO league (league_name, league_type, draft_date, max_teams)
VALUES
('NBA Fantasy League', 'Basketball', '2024-01-10', 12),
('Soccer Stars League', 'Soccer', '2024-01-15', 8),
('Gridiron Masters', 'Football', '2024-01-20', 10);

CREATE TABLE match_data (
    match_id SERIAL PRIMARY KEY,
    team_id INT REFERENCES team(team_id),
    match_date DATE NOT NULL,
    final_score INT,
    winner VARCHAR(100)
);

INSERT INTO match_data (match_id, team_id, match_date, final_score, winner)
VALUES
(1, 1, '2024-01-15', 100, NULL),
(1, 2, '2024-01-15', 98, 'Los Angeles Lakers'),
(2, 3, '2024-01-20', 30, NULL),
(2, 4, '2024-01-20', 28, 'Inter Miami');

CREATE TABLE match_event (
    match_event_id SERIAL PRIMARY KEY,
    match_id INT REFERENCES match_data(match_id),
    event_type VARCHAR(50),
    event_time TIME,
    fantasy_points INT
);

INSERT INTO match_event (match_id, event_type, event_time, fantasy_points)
VALUES
(1, 'Three Pointer', '00:15:00', 5),
(1, 'Foul', '00:20:00', -2),
(2, 'Touchdown', '00:25:00', 10),
(2, 'Field Goal', '00:30:00', 3);

CREATE TABLE waiver (
    waiver_id SERIAL PRIMARY KEY,
    team_id INT REFERENCES team(team_id),
    waiver_status VARCHAR(20),
    waiver_pickup_date DATE
);

INSERT INTO waiver (waiver_id, team_id, waiver_status, waiver_pickup_date)
VALUES
(1, 1, 'Approved', '2024-01-10'),
(2, 2, 'Pending', '2024-01-12'),
(3, 3, 'Denied', '2024-01-14'),
(4, 4, 'Approved', '2024-01-16');

CREATE TABLE draft (
    draft_id SERIAL PRIMARY KEY,
    league_id INT REFERENCES league(league_id),
    draft_date DATE NOT NULL,
    draft_order JSONB NOT NULL,
    draft_status VARCHAR(20) DEFAULT 'Scheduled'
);

INSERT INTO draft (league_id, draft_date, draft_order, draft_status)
VALUES
(1, '2024-01-10', '{"1": "LeBron James", "2": "Kevin Durant"}', 'Completed'),
(2, '2024-01-15', '{"1": "Lionel Messi", "2": "Cristiano Ronaldo"}', 'Scheduled'),
(3, '2024-01-20', '{"1": "Tom Brady", "2": "Shohei Ohtani"}', 'In Progress');


CREATE TABLE player_stats (
    player_stats_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES player(player_id),
    game_date DATE NOT NULL,
    performance_stats JSONB NOT NULL,
    injury_status VARCHAR(50)
);

INSERT INTO player_stats (player_id, game_date, performance_stats, injury_status)
VALUES
(1, '2024-01-12', '{"points": 30, "rebounds": 10, "assists": 5}', 'Healthy'),
(2, '2024-01-14', '{"goals": 2, "assists": 1}', 'Healthy'),
(3, '2024-01-16', '{"touchdowns": 3, "yards": 250}', 'Injured');


CREATE TABLE match_team (
    match_team_id SERIAL PRIMARY KEY,
    match_id INT REFERENCES match_data(match_id),
    team_id INT REFERENCES team(team_id)
);

INSERT INTO match_team (match_id, team_id)
VALUES
(1, 1),
(1, 2),
(2, 3),
(2, 4);

CREATE TABLE trade (
    trade_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES player(player_id),
    trade_date DATE NOT NULL,
    teams_involved VARCHAR(255)
);

INSERT INTO trade (player_id, trade_date, teams_involved)
VALUES
(1, '2024-01-15', 'Los Angeles Lakers, Phoenix Suns'),
(2, '2024-01-20', 'Inter Miami, Al Nassr'),
(3, '2024-01-25', 'Tampa Bay Buccaneers, Golden State Warriors');


--Function

CREATE OR REPLACE FUNCTION updateRankings()
RETURNS VOID AS $$
BEGIN
    WITH ranked_teams AS (
        SELECT 
            team_id,
            RANK() OVER (ORDER BY total_points_scored DESC) AS new_rank
        FROM team
    )
    UPDATE team
    SET ranking = ranked_teams.new_rank
    FROM ranked_teams
    WHERE team.team_id = ranked_teams.team_id;
END;
$$ LANGUAGE plpgsql;
