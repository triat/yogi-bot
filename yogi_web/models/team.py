from django.db import models
from django.utils.translation import ugettext as _


class Team(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    tag = models.CharField(max_length=10, blank=True, null=True)
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def __str__(self):
        return f"[{self.tag}] {self.name}"
