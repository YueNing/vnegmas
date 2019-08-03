"""
    some class that used for monitor the stats information of 
    negmas during the time of simulation

    monitor methode:
        1. detect the information of changing file
        2. detect the information of shared memory
"""

from abc import ABCMeta, abstractmethod
import os, time
from typing import Optional
from watchdog.events import FileSystemEventHandler 
from watchdog.observers import Observer
from hachiko.hachiko import AIOWatchdog, AIOEventHandler
import asyncio
from negmas.situated import StatsMonitor, WorldMonitor

class NegmasMonitorFile(AIOEventHandler):
    """
        Use this class to monitor the stats file
        >>> nm = NegmasMonitorFile()
        please see how to initial NegmasMonitorFile need set log_folder!
        >>> nm2 = NegmasMonitorFile(log_folder='./log_folder')
        {'log': ['log.txt', 'log_test'], 'stats': ['m_product', 'm_balance', 'm_breach', 'm_kkk']}
        >>> nm2.run()
    """
    def __init__(self, log_folder:Optional[str]=None):
        super(NegmasMonitorFile, self).__init__()
        self.mode = "debug"   
        self._watch_path = log_folder
        NegmasMonitorFile._watch_path = log_folder
        if log_folder is not None:
            self._file_detect()
        else:
            print('please see how to initial NegmasMonitorFile need set log_folder!')
    
    # Use this function to detect  log and stats files in a directory, also set up the cursor to zero(after use seek to get the appended content)
    def _file_detect(self) -> dict:
        try:
            self.worlds_stats = {}
            def _detect_files(world):
                stats_files = {}
                logs_files = {}
                all_files = {}
                for f in os.listdir(self._watch_path+'/'+world):
                    if f.startswith("log"):
                        logs_files[f] = 0
                    elif f.startswith('m_'):
                        stats_files[f] = 0
                all_files["log"] = logs_files
                all_files["stats"] = stats_files
                return all_files
            worlds = next(os.walk(self._watch_path))[1]
            for w in worlds:
                self.worlds_stats[w] = _detect_files(w)
            if self.mode == "debug":
                print(self.worlds_stats)
        except Exception as e:
            print(f'can not find {self._watch_path}')
    
    async def on_deleted(self, event):
        print(event)
        if not event.is_directory:
            if self.mode == "debug":
                print(f"delete {event.src_path}")

    async def on_created(self, event):
        print(event)
        world_monitor = []
        if not event.is_directory:
            new_file = event.src_path.split("/")[-1]
            world_name = event.src_path.split("/")[-2]
            if world_name in self.worlds_stats:
                if new_file.startswith("log"):
                    self.worlds_stats[world_name]["log"][new_file] = 0
                elif new_file.startswith("m_"):
                    self.worlds_stats[world_name]["stats"][new_file] = 0
                if self.mode == "debug":
                    print(f"create {event.src_path} files {self.worlds_stats}")
        else:
            self.worlds_stats[event.src_path.split("/")[-1]] = {"log":{}, "stats":{}}
            print(self.worlds_stats)


    async def on_moved(self, event):
        print(event)
        if not event.is_directory:
            if mode == "debug":
                print(f"moved {event.src_path}")

    async def on_modified(self, event):
        print(event)
        if not event.is_directory:
            file_path = event.src_path
            filename = file_path.split('/')[-1]
            world_name = file_path.split('/')[-2]
            new_content = ''
            if world_name in self.worlds_stats:
                if filename.startswith('m_'):
                    last_seek = self.worlds_stats[world_name]['stats'][filename]
                    f = open(file_path)
                    f.seek(last_seek,0)
                    new_content = f.read().strip().replace("\n", "")
                    self.worlds_stats[world_name]['stats'][filename] = f.tell()
                    print(self.worlds_stats[world_name]['stats'][filename])
                    f.close()
                if self.mode == "debug":
                    print(f"changed {file_path} content {new_content}")

async def watch_fs(path):
    watch = AIOWatchdog(path, event_handler=NegmasMonitorFile(log_folder=path))
    watch.start()
    import threading
        
    print('monitor threading is {}'. format(threading.current_thread()))
    import os

    print("monitor process id is {}".format(os.getpid()))
    for _ in range(100):
        await asyncio.sleep(1)
    watch.stop()
    print("Finish monitoring task")
    
class NegmasMonitorMemory(StatsMonitor,):
    
    def init(self, stats, world_name):
        print(f"The World {world_name} is monitor and init stats is {stats}")
    
    def step(self, stats,  world_name):
        print(f"step function is executed in world {world_name}, the stats are {stats}")

if __name__ == "__main__":
    start = time.time()
    paths = ['./log_folder']
    tasks = [watch_fs(path) for path in paths]
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.wait(tasks))
    finally:
        loop.close()
    print("finished all monitoring tasks! time %.5f" % float(time.time()-start))