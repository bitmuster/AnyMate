
import unittest
from AnyMate import *

class TestAnyMateConfig(unittest.TestCase):

    def test_pass(self):
        self.assertEqual( 1, 1)

    def test_init(self):
        c=Config("text","name","command","color","envobj")
        self.assertEqual(c.text,"text")
        self.assertEqual(c.name,"name")
        self.assertEqual(c.command,"command")
        self.assertEqual(c.color,"color")
        self.assertEqual(c.envobj,"envobj")



if __name__ == '__main__':
    unittest.main()
