import configparser
import os
from .managerchart import ManagerChart

def _get_config(filename):
    try:
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__) + filename))
        return config
    except Exception as e:
        print("open config file error please confirm the path of ini file is right", e)


def _get_world_config(
    filename: str = "/world_config.ini"
) -> configparser.ConfigParser:
    """
        >>> get_world_config(filename='./world_config_ini') #doctest: +ELLIPSIS
        <configparser.ConfigParser object at 0x...>
    """
    config = _get_config(filename)
    return config


def _get_web_config(
    filename: str = "/web_config.ini"
) -> configparser.ConfigParser:
    """
        >>> get_world_config(filename='./web_config_ini') #doctest: +ELLIPSIS
        <configparser.ConfigParser object at 0x...>
    """
    config = _get_config(filename)

    def remove_character(data):
        if "(" and ")" in data:
            return tuple(
                data.replace(" ", "").replace("(", "").replace(")", "").split(",")
            )
        return data

    for section in config._sections:
        for key in config._sections[section]:
            config._sections[section][key] = remove_character(
                config._sections[section][key]
            )
    return config

def _get_real_time_config(filename: str = "/real_time.ini"):
    mc = ManagerChart(filename)
    return mc



if __name__ == "__main__":
    import doctest

    doctest.testmod()
