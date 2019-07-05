from ..configs import get_web_config as _get_web_config
from ..nnegmas import run_negmas as _run_negmas


def run_negmas():
    try:
        _run_negmas()
        negmas_status = "Running"
    except Exception as e:
        print("some problem when run the negmas click from interface!", e)


def get_web_config():
    try:
        c = _get_web_config()
        get_web_config_status = "Get"
        return c
    except Exception as e:
        print("some problem when get the web config click from interface!", e)
