import sys
from os.path import dirname, join
source_code_path = join(dirname(__file__), '../')
sys.path.append(source_code_path)

from vnegmas import VNegmas

if __name__ == "__main__":
    vnegmas = VNegmas(name="VNegmas")
    vnegmas.run()
