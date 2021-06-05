import unittest
from unittest.mock import MagicMock, patch

from interpreter import Interpreter


class TestInterpreter(unittest.TestCase):
    """The test class for the Interpreter"""

    def test_interpreter_init(self):
        Interpreter("urxvt")

    def test_interpreter_fail(self):
        with self.assertRaises(Exception):
            Interpreter("fail")

    def test_interpreter_suffix(self):
        interp = Interpreter("urxvt")
        suff = interp.get_suffix()
        exp = """echo "Press the Any-Key to Continue "\nread any-key' &"""
        self.assertEqual(suff, exp)

    def test_interpreter_prefix(self):
        interp = Interpreter("urxvt")
        suff = interp.get_prefix()
        exp = (
            """urxvt -sl 10000 -cr BLUE -bg lightblue -fg black -e /bin/bash -c ' \n"""
        )
        self.assertEqual(suff, exp)

    def test_interpreter_decorate(self):
        interp = Interpreter("urxvt")
        cmd = interp.decorate_command("Mate, go hom yur drunk")
        exp = interp.get_prefix() + "Mate, go hom yur drunk" + interp.get_suffix()
        self.assertEqual(cmd, exp)
