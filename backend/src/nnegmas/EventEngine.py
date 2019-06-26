"""
    description: multiprocessing event engine
"""
__author__ = 'naodongbanana'

from multiprocessing import Process, Queue
from negmas.apps.scml import SCMLWorld
import time
from . import glovar
# import glovar
import itertools
# import sys 
# sys.path.append('../')
from .. import configs
class EventEngine(object):
    """
        Base class used to manager a public class
    """
    def __init__(self, *args, **kwargs):
        self._eventQueue = Queue()
        self._active = False
        # {'scmlworld':[handler1, handler2]}
        self._handlers = {}
        self._processPool = []
        self._mainProcess=Process(target=self._run)

    def _run(self):
        while self._active:
            if not self._eventQueue.empty():
                event = self._eventQueue.get(block=True, timeout=1)
                self._process(event)
            else:
                pass

    def _process(self, event):
        if event.type in self._handlers:
            for handler in self._handlers[event.type]:
                p = Process(target=handler, args=(event, ))
                self._processPool.append(p)
                p.start()

    def start(self):
        self._active = True
        self._mainProcess.start()

    def stop(self):
        self._active = False
        for p in self._processPool:
            p.join()
        # self._mainProcess.join()

    def terminate(self):
        self._active = False
        for p in self._processPool:
            p.terminate()
        self._mainProcess.join()

    def register(self, type, handler):
        try:
            handlerList = self._handlers[type]
        except KeyError:
            handlerList = []
            self._handlers[type] = handlerList
        
        if handler not in handlerList:
            self._handlers[type].append(handler)

    def unregister(self, type, handler):
        try:
            handlerList = self._handlers[type]

            if handler in handlerList:
                handlerList.remove(handler)
                self._handlers[type].remove(handler)

            if not handlerList:
                del self._handlers[type]
        
        except KeyError:
            pass

    def sendEvent(self, event):
        self._eventQueue.put(event)

class Event(object):
    """
        Event Class
    """
    def __init__(self, type=None, *args, **kwargs):
        self.type = type
        self.dict = {}

class Public_NegmasAccount:
    """"
        Public class analyse world information and decide which information needed to send to listener ,
        need to use a eventengine to manager the event
        example:
        >>> Event_Porcess_New_Step = "Porcess_New_Step"
        >>> listener1 = ListenerTypeOne('naodongbanana', world_recall_reuslt_dict=glovar.world_recall_reuslt_naodongbanana_manager_dict)
        >>> ee = EventEngine()
        >>> ee.register(Event_Porcess_New_Step, listener1.showNewStep)
        >>> ee.start()
        >>> publicAcc = Public_NegmasAccount(ee)
        >>> from negmas.apps.scml import SCMLWorld
        >>> world = 
        >>> publicAcc.processNewStep(Event_Porcess_New_Step, world)
    """
    def __init__(self, eventManager):
        self._eventManager = eventManager
        self.scmlWorld = None

    def _process_world(self, world):
        miners = [miner.name for miner in world.miners]
        factories_managers = [manager.name for manager in world.factory_managers]
        consumers = [consumer.name for consumer in world.consumers]

        def _contracts():
            return [(_contract['seller_name'], _contract['buyer_name']) for _contract in world.signed_contracts]
        
        contracts = _contracts()
        _stats = world._stats
        public_dic =  {'current_step':world.current_step if world.current_step is not None else 0, 
                                            'scmlworld':world.name if world.name else None,
                                            'factories_managers': factories_managers, 
                                            'consumers':consumers,
                                            'miners': miners,
                                            'contracts':contracts,
                                            'market_size_total':world._stats['_market_size_total']
                                        }
        return public_dic

    def processNewStep(self, eventType, world:SCMLWorld=None):
        event = Event(eventType)
        if world is not None:
            event.dict = self._process_world(world)
        else:
            event.dict['current_step'] = -1
            event.dict['scmlworld'] = None
        self._eventManager.sendEvent(event)
        print('send inforamtion about new step')

class ListenerTypeOne:
    def __init__(self, username, world_recall_reuslt_dict=None):
        self._username = username
        self._world_recall_reuslt_dict = world_recall_reuslt_dict

    def showNewStep(self, event):
        glovar.step = event.dict['current_step']
        glovar.scmlworld = event.dict['scmlworld']
        if self._world_recall_reuslt_dict is not None:
            for k, value in event.dict.items():
                self._world_recall_reuslt_dict[k] = value 
        # print('{} get the result of new step and manager {}'.format(self._username, self._world_recall_reuslt_dict))        
        # print('plot the result of new step {}'.format(self._world_recall_reuslt_dict['current_step']))

if __name__ == "__main__":
    import doctest
    doctest.testmod()