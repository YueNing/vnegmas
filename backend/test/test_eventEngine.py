from ..src.nnegmas import EventEngine
import unittest

class TestPublicNegmasAccount(unittest.TestCase):
    def setUp(self):
        print("Test EventEngine start")
    
    def test_processNewStep(self):
        ee = EventEngine.EventEngine()
        self.PublicNegmasAccount = EventEngine.Public_NegmasAccount(ee)
        self.assertEqual(self.PublicNegmasAccount.processNewStep(), 
                            'send inforamtion about new step')
    def test__process_world(self):
        self.PublicNegmasAccount = EventEngine.Public_NegmasAccount()
