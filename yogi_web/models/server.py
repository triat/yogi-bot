import logging
import uuid
from django.db import models
from django.utils.translation import ugettext as _

from .match import Match
from ..services.rcon_service import execute_rcon_cmd

logger = logging.getLogger(__name__)


class ServerConfigurationUploadError(Exception):
    """
    Raised when the upload of the config file couldn't be done correctly
    """


class Server(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    ip = models.CharField(max_length=15, blank=True, null=True)
    port = models.IntegerField(blank=True, null=True)
    rcon_password = models.CharField(default=uuid.uuid4, max_length=36)
    running_match = models.OneToOneField(Match, models.SET_NULL, blank=True, null=True)
    server_password = models.CharField(max_length=24, blank=True, null=True)

    class Meta:
        verbose_name = _("Server")
        verbose_name_plural = _("Servers")

    def __str__(self):
        text = f"[{self.name}] steam://connect/{self.ip}:{self.port}"
        if self.server_password:
            text += f"/{self.server_password}"
        return text

    def load_match_config(self) -> str:
        response = execute_rcon_cmd(
            "get5_loadmatch", (self.ip, self.port), self.rcon_password
        )
        logger.debug(
            "Server %s - response to loading of the config: %s", self.id, response
        )
        return response

    def upload_match_config(self):
        if self.running_match is None:
            raise ServerConfigurationUploadError("No match configured for this server")
        match_config = self.running_match.match_config
        return match_config
        # TODO: upload the file to the server or make the server download it
