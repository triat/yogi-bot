from uuid import uuid4

from django.db import models
from django.utils.translation import ugettext as _

from .team import Team


class Match(models.Model):
    DEFAULT = "WARMUP"
    STATUS = [
        (DEFAULT, _("Warm up")),
        ("KNIFE", _("Knife")),
        ("LIVE", _("Live")),
        ("PAUSED", _("Paused")),
        ("OVERTIME", _("Over time")),
        ("DONE", _("Done")),
        ("CANCELLED", _("Cancelled")),
    ]
    uuid = models.CharField(default=uuid4, max_length=100)
    team_1 = models.ForeignKey(
        Team, on_delete=models.SET_NULL, blank=True, null=True, related_name="team_1"
    )
    team_2 = models.ForeignKey(
        Team, on_delete=models.SET_NULL, blank=True, null=True, related_name="team_2"
    )
    winner = models.ForeignKey(
        Team, on_delete=models.SET_NULL, blank=True, null=True, related_name="winner"
    )
    status = models.CharField(max_length=50, choices=STATUS, default=DEFAULT)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    skip_veto = models.BooleanField(default=True)
    team_1_score = models.IntegerField(default=0)
    team_2_score = models.IntegerField(default=0)
    veto_mappool = models.CharField(max_length=500, blank=True, null=True)
    max_maps = models.IntegerField(default=1)

    class Meta:
        verbose_name = _("Match")
        verbose_name_plural = _("Matches")

    def __str__(self):
        return f"{self.status} - {self.team_1} vs {self.team_2}"

    @property
    def match_config(self) -> dict:
        t1_info = self.team_1.team_information if self.team_1 else {}
        t2_info = self.team_2.team_information if self.team_2 else {}
        return {
            "match_id": self.uuid,
            "num_maps": 1,
            "maplist": [{"de_dust2": ""}],
            "skip_veto": self.skip_veto,
            "veto_first": "team1",
            "side_type": "always_knife",
            "players_per_team": 5,
            "min_players_to_ready": 1,
            "team1": t1_info,
            "team2": t2_info,
            "cvars": {
                "hostname": f"Match - {t1_info.get('name')} vs {t2_info.get('name')}"
            },
        }
