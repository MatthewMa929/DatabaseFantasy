import random
from datetime import datetime, timedelta

# Helper functions
def generate_name():
    first_names = ["John", "Emma", "Michael", "Sophia", "William", "Olivia"]
    last_names = ["Smith", "Johnson", "Brown", "Taylor", "Miller", "Davis"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def random_status():
    return random.choice(["Active", "Inactive", "Suspended", "Retired"])

# Generate SQL statements
def generate_draft_data(file, num_records):
    for i in range(num_records):
        draft_id = i + 1
        league_id = random.randint(1, 50)
        player_id = random.randint(1, 200)
        draft_date = generate_date(datetime(2023, 1, 1), datetime(2023, 12, 31))
        draft_order = random.randint(1, 10)
        draft_status = random.choice(["Completed", "Pending", "Canceled"])
        file.write(f"INSERT INTO draft (DraftID, LeagueID, PlayerID, draft_date, draft_order, draft_status) "
                   f"VALUES ({draft_id}, {league_id}, {player_id}, '{draft_date}', {draft_order}, '{draft_status}');\n")

def generate_league_data(file, num_records):
    for i in range(num_records):
        league_id = i + 1
        user_id = random.randint(1, 100)
        league_name = f"League_{league_id}"
        league_type = random.choice(["Public", "Private"])
        draft_date = generate_date(datetime(2023, 1, 1), datetime(2023, 12, 31))
        max_teams = random.randint(8, 20)
        file.write(f"INSERT INTO league (LeagueID, UserID, league_name, league_type, draft_date, max_teams) "
                   f"VALUES ({league_id}, {user_id}, '{league_name}', '{league_type}', '{draft_date}', {max_teams});\n")

def generate_match_data(file, num_records):
    for i in range(num_records):
        match_id = i + 1
        team_id = random.randint(1, 100)
        match_date = generate_date(datetime(2023, 1, 1), datetime(2023, 12, 31))
        final_score = random.randint(50, 150)
        winner = random.choice([team_id, random.randint(1, 100)])
        file.write(f"INSERT INTO match_data (MatchID, TeamID, match_date, final_score, winner) "
                   f"VALUES ({match_id}, {team_id}, '{match_date}', {final_score}, {winner});\n")

def generate_player_data(file, num_records):
    for i in range(num_records):
        player_id = i + 1
        full_name = generate_name()
        sport = random.choice(["Football", "Basketball", "Baseball", "Soccer"])
        real_team = f"Team_{random.randint(1, 30)}"
        position = random.choice(["Forward", "Guard", "Pitcher", "Midfielder"])
        fantasy_points = round(random.uniform(0, 500), 2)
        availability_status = random.choice(["Available", "Injured", "Suspended"])
        file.write(f"INSERT INTO player (PlayerID, full_name, sport, real_team, position, fantasy_points, availability_status) "
                   f"VALUES ({player_id}, '{full_name}', '{sport}', '{real_team}', '{position}', {fantasy_points}, '{availability_status}');\n")

def generate_user_data(file, num_records):
    for i in range(num_records):
        user_id = i + 1
        full_name = generate_name()
        email = f"user{user_id}@example.com"
        username = f"user{user_id}"
        password = f"pass{user_id}"
        profile_settings = random.choice(["Standard", "Premium"])
        file.write(f"INSERT INTO user_data (UserID, full_name, email, username, password, profile_settings) "
                   f"VALUES ({user_id}, '{full_name}', '{email}', '{username}', '{password}', '{profile_settings}');\n")

# Write to file
with open("fantasy_sports_insert.sql", "w") as file:
    num_records = 100
    generate_draft_data(file, num_records)
    generate_league_data(file, 50)
    generate_match_data(file, num_records)
    generate_player_data(file, 200)
    generate_user_data(file, 100)
