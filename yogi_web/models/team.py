from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _


class Team(models.Model):
    _name = models.CharField(max_length=50, blank=False, null=False, db_column="name")
    _tag = models.CharField(max_length=10, blank=True, null=True, db_column="tag")
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def __str__(self):
        return f"[{self.tag}] {self.name}"

    def get_absolute_url(self):
        return reverse("yogi_web:team_detail", args=[self.id])

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = value

    @property
    def team_information(self) -> dict:
        return {"name": self.name, "tag": self.tag}
