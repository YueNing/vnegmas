import sys
from os.path import dirname, join
source_code_path = join(dirname(__file__), '../')
sys.path.append(source_code_path)

import vnegmas
from vnegmas import vnegmas
from vnegmas import nnegmas, watch_fs
import asyncio
import time

if __name__ == "__main__":
    start = time.time()
    tasks = [vnegmas(), watch_fs('./logs/tournaments')]
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.wait(tasks))
    finally:
        loop.close()
    # table_base().render()
    print("finished all tasks! time %.5f" % float(time.time()-start))
