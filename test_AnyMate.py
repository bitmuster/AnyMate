#!/usr/bin/env python3

# This test file is kind of experimental!
# Here we try to get everything under test-contorl before doing
# anything important to the code.
# This sometimes might lead to too complicated tests.

# 4 Phase test pattern (from Osherove?)
# Setup-Exercise-Verify-Cleanup

# See also:
# https://docs.python.org/3.5/library/unittest.html
# https://docs.python.org/3.5/library/unittest.mock.html

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

from AnyMate import AnyMate
from interpreter import Interpreter
from anymate_gui import AnyMateGui as gui
from AnyMate import main, print_help
import config as aconf

class TestClassAnyMate(unittest.TestCase):
    """Here we re-use a real existing file with defined content"""

    #    def setUp(self):
    #        #The abspath is used to set values in the configfile
    #        global abspath
    #        abspath="SomePath"
    #
    #    def tearDown(self):
    #        global abspath
    #        abspath=None

    def test_init(self):
        anymate = AnyMate("empty.anymate")
        anymate.list()
        anymate.command_list()

    def test_init_deprecated(self):
        with self.assertRaises(SystemError):
            AnyMate("empty.taomate")

    def test_fail(self):
        with self.assertRaises(SystemError):
            AnyMate("empty.anymate_nix")

    def test_getcolor(self):
        anymate = AnyMate("empty.anymate")
        self.assertEqual(anymate.get_color("red"), AnyMate.RED)
        self.assertEqual(anymate.get_color("green"), AnyMate.GREEN)
        self.assertEqual(anymate.get_color("blue"), AnyMate.BLUE)
        self.assertEqual(anymate.get_color("gray"), AnyMate.GREY)
        self.assertEqual(anymate.get_color("cyan"), AnyMate.CYAN)

        self.assertEqual(AnyMate.RED, "#EFBFBF")

    def test_getcolor_fail(self):
        anymate = AnyMate("empty.anymate")
        self.assertEqual(anymate.get_color("colorofmagic"), None)
        self.assertEqual(anymate.get_color(None), None)
        self.assertEqual(anymate.get_color("#FFFFFF"), "#FFFFFF")

    def test_getcolor_badfail(self):
        anymate = AnyMate("empty.anymate")
        with self.assertRaises(SystemError):
            anymate.get_color("#FF")

    def test_AnyMate_real_file(self):
        """We read the example file, we know the content"""
        anymate = AnyMate("empty.anymate")
        self.assertEqual(anymate.conf[0].name, "Hello World")
        self.assertEqual(anymate.conf[0].nick, "hello")
        self.assertEqual(anymate.conf[0].text, 'echo "Hello World!"\n')
        self.assertEqual(anymate.conf[0].color, "#ddffdd")

    # intention unclear
    #    @patch("__main__.exec")
    #    @patch("__main__.open")
    #    @patch("__main__.compile")
    #    def test_readAnyMate_faked(self, compilemock, openmock, execmock):
    #
    #        a=AnyMate("empty.anymate")
    #
    #        a.readAnyMate("somefile")

    @patch.object(aconf.Config, "execute")
    def test_execute(self, exmock):
        anymate = AnyMate("empty.anymate")
        anymate.execute("hello")

    @patch.object(aconf.Config, "execute")
    def test_execute_fail(self, exmock):
        anymate = AnyMate("empty.anymate")
        with self.assertRaises(SystemError):
            anymate.execute("no")

    @patch("os.system")
    def test_execute_os_mocked(self, osmock):
        anymate = AnyMate("empty.anymate")
        anymate.execute("hello")
        call = (
            "xterm -sl 10000 -cr BLUE -bg lightblue -fg black -e /bin/bash "
            + '-c \' \necho "Hello World!"\n '
            + 'echo "Sleeping 5 seconds"\n sleep 5\' &'
        )
        osmock.assert_called_with(call)


class AnyMateConfigReader(unittest.TestCase):

    # pain
    @patch("builtins.globals")
    @patch("builtins.open")
    @patch("builtins.compile")
    @patch("builtins.exec")
    @patch("AnyMate.AnyMate.__init__")
    def test_read_config_notabs(self, imock, emock, cmock, omock, gmock):
        filename = "afile"
        imock.return_value = None  # The constructor shall return None
        gmock.return_value = {"commandList": []}  # return empty commandList
        anymate = AnyMate()
        anymate.read_config(filename)
        omock.assert_called_once_with(os.path.abspath(filename))

    # pain
    @patch("builtins.globals")
    @patch("builtins.open")
    @patch("builtins.compile")
    @patch("builtins.exec")
    @patch("AnyMate.AnyMate.__init__")
    def test_read_config_abs(self, imock, emock, cmock, omock, gmock):
        filename = "/home/user/whereever/afile.anymate"
        imock.return_value = None  # The constructor shall return None
        gmock.return_value = {"commandList": []}  # return empty commandList
        anymate = AnyMate()
        anymate.read_config(filename)
        omock.assert_called_once_with(os.path.abspath(filename))


if __name__ == "__main__":
    # explicitly name the module so that pythons trace function cannot
    # mess around with unittest test discovery
    unittest.main(module="test_AnyMate")
