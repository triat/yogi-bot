from valve import rcon

from typing import Tuple


def execute_rcon_cmd(
    cmd: str, server_address: Tuple[str, int], rcon_password: str
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
    with rcon.RCON(server_address, rcon_password) as server_rcon:
        return server_rcon(cmd)
