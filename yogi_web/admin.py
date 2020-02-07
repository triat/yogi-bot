from django.contrib import admin

from .models import Match, Server, Team


class MatchAdmin(admin.ModelAdmin):
    model = Match
    list_display = ["id", "team_1", "team_2", "status"]


admin.site.register(Match, MatchAdmin)


class ServerAdmin(admin.ModelAdmin):
    model = Server
    list_display = ["id", "name", "ip", "port"]


admin.site.register(Server, ServerAdmin)


class TeamAdmin(admin.ModelAdmin):
    model = Team
    list_display = ["id", "name", "tag"]


admin.site.register(Team, TeamAdmin)
