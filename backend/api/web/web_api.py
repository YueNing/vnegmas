from typing import Optional

from ..configs import get_web_config as _get_web_config
from ..nnegmas import run_negmas as _run_negmas
from ...src.web import _monitor_every_info

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

# TODO return information of world from backend to frontend
def monitor_every_info(data: Optional[dict]) -> dict:
    try:
        if data is not None:
            show = _monitor_every_info(data)
            return show
        else:
            return {"message":"nothing has been changed!"}
    except Exception as e:
        print("some problem when process the monitor every info!", e)