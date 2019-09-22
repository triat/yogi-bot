from django.contrib import admin

from .models import Match, Server, Team


class MatchAdmin(admin.ModelAdmin):
    model = Match
    list_display = ["team_1", "team_2", "status"]


admin.site.register(Match, MatchAdmin)


class ServerAdmin(admin.ModelAdmin):
    model = Server
    list_display = ["name", "ip", "port"]


admin.site.register(Server, ServerAdmin)


class TeamAdmin(admin.ModelAdmin):
    model = Team
    list_display = ["name", "tag"]


admin.site.register(Team, TeamAdmin)
