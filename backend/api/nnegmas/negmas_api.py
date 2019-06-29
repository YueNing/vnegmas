from ...src.nnegmas import (
    run_negmas as _run_negmas
)
from ..configs import (
    get_world_config,
    get_web_config
)
def run_negmas(config:dict=None) -> None:
    """
        >>> run_negmas()
        'config'
    """
    try:
        config = get_world_config()
        _run_negmas() 
        return config
    except Exception as e:
        print("run the negmas system failure. please confirm the config of simulator are right!", e)