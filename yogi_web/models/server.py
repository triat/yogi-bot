import uuid
from django.db import models
from django.utils.translation import ugettext as _

from .match import Match


class Server(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    ip = models.CharField(max_length=15, blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    rcon_password = models.CharField(default=uuid.uuid4, max_length=36)
    running_match = models.OneToOneField(Match, models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = _("Server")
        verbose_name_plural = _("Servers")

    def __str__(self):
        pass
