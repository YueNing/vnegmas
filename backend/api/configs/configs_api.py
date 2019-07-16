import configparser

from ...src.configs import _get_web_config, _get_world_config, _get_real_time_config


def get_web_config(filename: str = None) -> configparser.ConfigParser:
    if filename is not None:
        c = _get_web_config(filename)
    else:
        c = _get_web_config()
    return c


def get_world_config(filename: str = None) -> configparser.ConfigParser:
    if filename is not None:
        c = _get_world_config(filename)
    else:
        c = _get_world_config()
    return c

def get_real_time_config(filename: str = None) -> configparser.ConfigParser:
    if filename is not None:
        c = _get_real_time_config(filename)
    else:
        c = _get_real_time_config()
    return c

# TODO: update web config
def update_web_config(newdate: dict = None) -> str:
    try:
        _update_web_config(newdate)
        return "successfully saved"
    except Exception as e:
        print("update the web config data failure!", e)

# TODO: update world config
def update_world_config(newdate: dict = None) -> str:
    try:
        _update_world_config(newdate)
        return "successfully saved"
    except Exception as e:
        print("update the world config data failure!", e)

# TODO: delete web config
def delete_web_config() -> str:
    try:
        _delete_web_config()
        return "successfully saved"
    except Exception as e:
        print("delete the web config data failure!", e)

# TODO: delete world config
def delete_world_config() -> str:
    try:
        _update_world_config()
        return "successfully saved"
    except Exception as e:
        print("delete the world config data failure!", e)
