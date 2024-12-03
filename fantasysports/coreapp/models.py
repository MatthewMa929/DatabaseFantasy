from django.db import models


class UserData(models.Model):
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    profile_settings = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username


class League(models.Model):
    league_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    league_name = models.CharField(max_length=100)
    league_type = models.CharField(max_length=50)
    draft_date = models.DateField()
    max_teams = models.IntegerField()

    def __str__(self):
        return self.league_name


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100)
    total_points_scored = models.IntegerField()
    ranking = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.team_name


class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    sport = models.CharField(max_length=50)
    real_team = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    fantasy_points = models.IntegerField()
    availability_status = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name


class MatchData(models.Model):
    match_id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    match_date = models.DateField()
    final_score = models.IntegerField()
    winner = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Match {self.match_id}"


class MatchEvent(models.Model):
    match_event_id = models.AutoField(primary_key=True)
    match = models.ForeignKey(MatchData, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50)
    event_time = models.TimeField()
    fantasy_points = models.IntegerField()

    def __str__(self):
        return f"Event {self.match_event_id}"


class PlayerStats(models.Model):
    player_stats_id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game_date = models.DateField()
    performance_stats = models.TextField()
    injury_status = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Stats {self.player_stats_id}"


class Trade(models.Model):
    trade_id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    trade_date = models.DateField()
    teams_involved = models.CharField(max_length=255)

    def __str__(self):
        return f"Trade {self.trade_id}"


class Waiver(models.Model):
    waiver_id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    waiver_status = models.CharField(max_length=50)
    waiver_pickup_date = models.DateField()

    def __str__(self):
        return f"Waiver {self.waiver_id}"
