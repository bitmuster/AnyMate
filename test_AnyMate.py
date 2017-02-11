
# 4 Phase test pattern (from Osherove?)
# Setup-Exercise-Verify-Cleanup

import unittest
from unittest.mock import MagicMock,patch

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

    @patch("os.system")
    def test_execute(self, osmock):
        # Setup
        c=Config("ls -l","name","command","color", None)

        # According to the current setting
        call='xterm -sl 10000 -cr blue -bg lightblue -fg black -e /bin/bash -c \' \nls -l echo "Sleeping 5 seconds"\n sleep 5\' &'

        # Execise
        c.execute()

        # Verify
        osmock.assert_called_once_with(call)

    def test_str(self):
        # Setup
        c=Config("text","name","command","color", None)
        expected="Name: name Command: command Code: text"

        # Exercise
        r=str(c)

        # Verify
        self.assertEqual(r, expected)

    def test_getters(self):
        c=Config("text","name","command","color", "Env")
        cmd = "Whatever"
        env= "Env"
        c.setEnvironment(env)
        c.setCommand(cmd)
        r=c.getCommand()
        self.assertEqual(r, cmd)

class TestClassAnyMate(unittest.TestCase):
    """Here we re-use a real existing file with defined content"""

    def test_init(self):
        a=AnyMate("empty.anymate")
        a.list()
        a.commandList()

    def test_fail(self):
        with self.assertRaises(Exception):
            AnyMate("empty.anymate_nix")

    def test_getcolor(self):
        a=AnyMate("empty.anymate")
        self.assertEqual( a.getcolor("red"), red)
        self.assertEqual( a.getcolor("green"), green)
        self.assertEqual( a.getcolor("blue"), blue)
        self.assertEqual( a.getcolor("gray"), gray)
        self.assertEqual( a.getcolor("cyan"), cyan)

        self.assertEqual( red, '#EFBFBF')

    def test_getcolor_fail(self):
        a=AnyMate("empty.anymate")
        self.assertEqual( a.getcolor("colorofmagic"), None)


if __name__ == '__main__':
    unittest.main()
