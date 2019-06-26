from multiprocessing import Manager, Event, Queue
world_recall_reuslt_dict = Manager().dict()
publicAcc = Manager().Queue()
event =  Event()