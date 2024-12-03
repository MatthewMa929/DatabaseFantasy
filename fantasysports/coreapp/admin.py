from django.contrib import admin
from .models import UserData, League, Team, Player, MatchData, MatchEvent, PlayerStats, Trade, Waiver

admin.site.register(UserData)
admin.site.register(League)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(MatchData)
admin.site.register(MatchEvent)
admin.site.register(PlayerStats)
admin.site.register(Trade)
admin.site.register(Waiver)
