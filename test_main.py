import unittest
from unittest.mock import MagicMock, patch

from AnyMate import main, print_help, AnyMate

# In Spyder:
#    unittest:
#       !python3 -m unittest test_main.py
#    pytest
#       !pytest test_main.py::TestMain::test_main_hello -s


class TestMain(unittest.TestCase):
    """The main test class for AnyMate"""

    def test_main_noparam(self):
        with self.assertRaises(TypeError):
            main()

    def test_help(self):
        print_help()

    @patch("AnyMate.print_help")
    def test_main_help(self, mock):
        with self.assertRaises(SystemExit):
            main("")
        mock.assert_called_once_with()

    @patch("AnyMate.print_help")
    def test_main_intparam(self, mock):
        with self.assertRaises(SystemExit):
            main(88)
        mock.assert_called_once_with()

    def test_main_listparam(self):
        with self.assertRaises(SystemExit):
            main([])

    def test_main_one_param(self):
        with self.assertRaises(SystemExit):
            main(["one"])

    def test_main_three_param(self):
        with self.assertRaises(SystemExit):
            main(["one", "two", "three"])

    def test_main_fife_param(self):
        with self.assertRaises(SystemExit):
            main(["bad"] * 5)

    @patch("AnyMate.anymate_gui")
    @patch("AnyMate.AnyMate")
    def test_main_two_real_param(self, mock, guimock):
        # setup
        myfile = "template.json"
        mock.return_value = MagicMock()
        mock.load_configuration = MagicMock()
        # exercise
        main(["./AnyMate.py", myfile])
        # validate
        mock.assert_called_once_with(myfile)
        # We expect the gui to be called with the return value of AnyMate()
        guimock.assert_called_once_with(mock(), myfile)

    @patch("os.path.isfile")
    def test_main_nofile(self, mock):
        # setup
        myfile = "nofile"
        mock.return_value = False
        # exercise
        with self.assertRaises(SystemExit):
            main(["./AnyMate.py", myfile])

    @patch("os.path.isfile")
    @patch("AnyMate.anymate_gui")
    @patch("AnyMate.AnyMate")
    def test_main_mockedfile(self, anymock, guimock, filemock):
        # setup
        myfile = "nofile"
        filemock.return_value = True
        # exercise
        main(["./AnyMate.py", myfile])
        # validate
        anymock.assert_called_once_with(myfile)

    @patch("os.path.isfile")
    @patch("AnyMate.anymate_gui")
    @patch("AnyMate.AnyMate")
    def test_main_mainloop(self, anymock, guimock, filemock):
        # setup
        myfile = "nofile"
        filemock.return_value = True
        # Anymate() returns an AnymateObject
        anymock.return_value = MagicMock(name="AnyMate")
        gui = MagicMock(name="AnyMateGui")
        guimock.return_value = gui
        # exercise
        main(["./AnyMate.py", myfile])
        # validate
        anymock.assert_called_once_with(myfile)
        gui.mainloop.assert_called_once_with()

    @patch("AnyMate.AnyMate")
    def test_main_four_real_param(self, mock):
        # setup
        myfile = "template.json"
        conf = "hello"
        anym = MagicMock()
        mock.return_value = anym
        # exercise
        main(["./AnyMate.py", "--nogui", conf, myfile])
        # validate
        mock.assert_called_once_with(myfile, False)
        anym.execute.assert_called_once_with(conf)

    @patch("AnyMate.AnyMate")
    def test_main_four_wrong_param(self, mock):
        # setup
        myfile = "template.json"
        conf = "hello"
        anym = MagicMock()
        mock.return_value = anym
        # exercise
        with self.assertRaises(SystemExit):
            main(["./AnyMate.py", "BAM", conf, myfile])

    @patch("AnyMate.AnyMate")
    def test_main_four_wrong_file(self, mock):
        # setup
        myfile = "nofile"
        conf = "hello"
        anym = MagicMock()
        mock.return_value = anym
        # exercise
        with self.assertRaises(SystemExit):
            main(["./AnyMate.py", "--nogui", conf, myfile])

    @patch("os.path.isfile")
    @patch("AnyMate.AnyMate")
    def test_main_four_wrong_file_mocked(self, mock, filemock):
        # setup
        myfile = "template.json"
        conf = "hello"
        anym = MagicMock()
        mock.return_value = anym
        filemock.return_value = False
        # exercise
        with self.assertRaises(SystemExit):
            main(["./AnyMate.py", "BAM", conf, myfile])

    # Play with the main class

    @patch("AnyMate.AnyMate.execute")
    def test_main_greet(self, mock):
        myfile = "template.json"
        conf = "greet"

        main(["./AnyMate.py", "--nogui", conf, myfile])

        mock.assert_called_once_with(conf)

    def test_main_config_list_name(self):
        myfile = "template.json"
        anymate = AnyMate(myfile)
        anymate.load_configuration()

        cfg = anymate.get_config_list()
        value = cfg[0].get_name()

        self.assertEqual(value, "Greetings")

    def test_main_config_list_nick(self):
        myfile = "template.json"
        anymate = AnyMate(myfile)
        anymate.load_configuration()

        cfg = anymate.get_config_list()
        value = cfg[0].get_nick()

        self.assertEqual(value, "greet")

    def test_main_config_list_length(self):
        myfile = "template.json"

        anymate = AnyMate(myfile)
        anymate.load_configuration()

        cfg = anymate.get_config_list()
        expect = 18
        value = len(cfg)
        self.assertEqual(expect, value)

    def test_main_config_read_json(self):
        myfile = "template.json"

        anymate = AnyMate(myfile)
        anymate.load_configuration()

        cfg = anymate.get_config_list()
        expect = 18
        value = len(cfg)
        self.assertEqual(expect, value)

    def test_parse_entry_to_config_empty(self):
        myfile = "template.json"
        anymate = AnyMate(myfile)
        entry = ""

        self.assertRaises(SystemError)

    def test_parse_entry_to_config_single_get_name(self):
        myfile = "template.json"
        anymate = AnyMate(myfile)
        anymate.load_configuration()

        entry = {
            "name": "Greetings",
            "nick": "greet",
            "color": "green",
            "cmd": 'echo "Hello World"',
        }

        cfg = anymate.parse_entry_to_config(entry, myfile)
        self.assertEqual(entry.get("name"), cfg.get_name())

    def test_parse_entry_to_config_single_get_nick(self):
        myfile = "template.json"
        anymate = AnyMate(myfile)
        anymate.load_configuration()

        entry = {
            "name": "Greetings",
            "nick": "greet",
            "color": "green",
            "cmd": 'echo "Hello World"',
        }

        cfg = anymate.parse_entry_to_config(entry, myfile)
        self.assertEqual(entry.get("nick"), cfg.get_nick())
