import unittest
from unittest.mock import MagicMock, patch

import config as aconf


class TestAnyMateConfig(unittest.TestCase):
    def test_pass(self):
        self.assertEqual(1, 1)

    def test_init(self):
        conf = aconf.Config("text", "name", "nick", "color")
        self.assertEqual(conf.text, "text")
        self.assertEqual(conf.name, "name")
        self.assertEqual(conf.nick, "nick")
        self.assertEqual(conf.color, "color")

    @patch("os.system")
    def test_execute(self, osmock):
        # Setup
        conf = aconf.Config("ls -l", "name", "command", "color")

        # According to the current setting
        call = (
            "xterm -sl 10000 -cr BLUE -bg lightblue -fg black -e /bin/bash "
            + "-c ' \nls -l echo \"Sleeping 5 seconds\"\n sleep 5' &"
        )

        # Execise
        conf.execute()

        # Verify
        osmock.assert_called_once_with(call)

    def test_str(self):
        # Setup
        conf = aconf.Config("text", "name", "command", "color")
        expected = 'Name: "name"; Command: "command"; Code: "text";'

        # Exercise
        ret = str(conf)

        # Verify
        self.assertEqual(ret, expected)

    def test_getters(self):
        conf = aconf.Config("text", "name", "command", "color")
        ret = conf.get_command()
        self.assertEqual(ret, "text")