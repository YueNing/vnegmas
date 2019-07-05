from multiprocessing import Event, Manager, Queue

world_recall_reuslt_dict = Manager().dict()
publicAcc = Manager().Queue()
event = Event()
