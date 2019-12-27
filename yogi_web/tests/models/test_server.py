from mock import patch, PropertyMock

from yogi_web.helpers import CustomTestCase
from yogi_web.models.server import ServerConfigurationUploadError
from yogi_web.tests.models.factories import MatchFactory, ServerFactory


@patch("yogi_web.models.server.execute_rcon_cmd")
class LoadMatchConfigTest(CustomTestCase):
    def setUp(self):
        self.server = ServerFactory()

    def test_vanilla(self, mock_exec_rcon):
        mock_exec_rcon.return_value = "ok"
        response = self.server.load_match_config()

        self.assertEqual(response, "ok")
        mock_exec_rcon.assert_called_once_with(
            "get5_loadmatch",
            (self.server.ip, self.server.port),
            self.server.rcon_password,
        )


class UploadMatchConfigTest(CustomTestCase):
    def setUp(self):
        self.server = ServerFactory()

    def test_vanilla(self):
        match = MatchFactory()
        self.server.running_match = match
        self.server.save()

        with patch(
            "yogi_web.models.match.Match.match_config", new_callable=PropertyMock
        ) as mock_config:
            expected_response = {"foo": "bar"}
            mock_config.return_value = expected_response

            self.assertEqual(self.server.upload_match_config(), expected_response)

    def test_raises_when_no_match(self):
        with self.assertRaises(ServerConfigurationUploadError):
            self.server.upload_match_config()
