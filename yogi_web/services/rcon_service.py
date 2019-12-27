import logging
from typing import Tuple

from valve import rcon

logger = logging.getLogger(__name__)


def execute_rcon_cmd(
    cmd: str, server_address: Tuple[str, int], rcon_password: str, retry: bool = True
) -> str:
    """
    connect to the the server rcon and execute the given command

    Parameters
    ----------
    cmd : str
        the command to execute in the console
    server_address : Tuple[str, int]
        the ip of the server and the port
    rcon_password : str
        the password of the rcon

    Returns
    -------
    str
        the output of the console
    """
    logger.debug(
        "Running command %s on server %s:%s", cmd, server_address[0], server_address[1]
    )
    try:
        with rcon.RCON(server_address, rcon_password) as server_rcon:
            return server_rcon(cmd)
    except TimeoutError:
        if retry:
            logger.debug("Command timedout, retrying")
            return execute_rcon_cmd(cmd, server_address, rcon_password, retry=False)
        return "Command timedout"
    except Exception as e:
        logger.exception("Unknown error during execution of rcon cmd")
        return str(e)
