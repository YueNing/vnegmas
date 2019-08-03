"""
Demo how to register new Charts into the VNEGMAS system
"""

import sys
from os.path import dirname, join
source_code_path = join(dirname(__file__), '../')
sys.path.append(source_code_path)

from vnegmas.backend.api.configs import ManagerChart
from vnegmas.settings import DEFAULT_CHARTS

def register_from_setting():
    """
        register means this charts can be shown in VNEGMAS, but Default set False
    """
    charts = {}
    for chart in DEFAULT_CHARTS:
        charts [chart] = 'False'
    mc = ManagerChart('/home/naodongbanana/Document/vnegmas/vnegmas/backend/src/configs/real_time.ini')
    mc.register(charts)

if __name__ == "__main__":
    register_from_setting()