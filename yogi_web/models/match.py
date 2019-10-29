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
        return f"[{self.status}] {self.team_1} vs {self.team_2}"
