import unittest
from unittest.mock import MagicMock, patch

from AnyMate import main, print_help


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

    @patch("AnyMate.gui")
    @patch("AnyMate.AnyMate")
    def test_main_two_real_param(self, mock, guimock):
        # setup
        myfile = "template.json"
        mock.return_value = "Something"
        # exercise
        main(["./AnyMate.py", myfile])
        # validate
        mock.assert_called_once_with(myfile)
        # We expect the gui to be called with the return value of AnyMate()
        guimock.assert_called_once_with("Something", myfile)

    @patch("os.path.isfile")
    def test_main_nofile(self, mock):
        # setup
        myfile = "nofile"
        mock.return_value = False
        # exercise
        with self.assertRaises(SystemExit):
            main(["./AnyMate.py", myfile])

    @patch("os.path.isfile")
    @patch("AnyMate.gui")
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
    @patch("AnyMate.gui")
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
