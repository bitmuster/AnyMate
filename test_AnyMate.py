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

from AnyMate import main, AnyMate, AnyMateGUI, Config, Interpreter, abspath

class TestAnyMateConfig(unittest.TestCase):

    def test_pass(self):
        self.assertEqual(1, 1)

    def test_init(self):
        conf = Config("text", "name", "nick", "color")
        self.assertEqual(conf.text, "text")
        self.assertEqual(conf.name, "name")
        self.assertEqual(conf.nick, "nick")
        self.assertEqual(conf.color, "color")

    @patch("os.system")
    def test_execute(self, osmock):
        # Setup
        conf = Config("ls -l", "name", "command", "color")

        # According to the current setting
        call = 'xterm -sl 10000 -cr BLUE -bg lightblue -fg black -e /bin/bash ' \
            + '-c \' \nls -l echo "Sleeping 5 seconds"\n sleep 5\' &'

        # Execise
        conf.execute()

        # Verify
        osmock.assert_called_once_with(call)

    def test_str(self):
        # Setup
        conf = Config("text", "name", "command", "color")
        expected = "Name: \"name\"; Command: \"command\"; Code: \"text\";"

        # Exercise
        ret = str(conf)

        # Verify
        self.assertEqual(ret, expected)

    def test_getters(self):
        conf = Config("text", "name", "command", "color")
        ret = conf.get_command()
        self.assertEqual(ret, 'text')

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

        self.assertEqual(AnyMate.RED, '#EFBFBF')

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
        self.assertEqual(anymate.conf[0].color, '#ddffdd')

# intention unclear
#    @patch("__main__.exec")
#    @patch("__main__.open")
#    @patch("__main__.compile")
#    def test_readAnyMate_faked(self, compilemock, openmock, execmock):
#
#        a=AnyMate("empty.anymate")
#
#        a.readAnyMate("somefile")

    @patch("AnyMate.Config.execute")
    def test_execute(self, exmock):
        anymate = AnyMate("empty.anymate")
        anymate.execute("hello")

    @patch("AnyMate.Config.execute")
    def test_execute_fail(self, exmock):
        anymate = AnyMate("empty.anymate")
        with self.assertRaises(SystemError):
            anymate.execute("no")

    @patch("os.system")
    def test_execute_os_mocked(self, osmock):
        anymate = AnyMate("empty.anymate")
        anymate.execute("hello")
        call = 'xterm -sl 10000 -cr BLUE -bg lightblue -fg black -e /bin/bash ' \
            + '-c \' \necho "Hello World!"\n ' \
            + 'echo "Sleeping 5 seconds"\n sleep 5\' &'
        osmock.assert_called_with(call)

class TestClassAnyMateTemplate(unittest.TestCase):
    """A test class with yet unknown purpose"""

    def disabled_test_init(self):
        """Just load it to see if it loads,
        TODO: Remove abspath from this place
        """
        abspath = os.path.abspath(os.path.dirname(sys.argv[0]))
        print('Switching to directory ' + abspath)
        os.chdir(abspath)
        print(abspath)
        abspath = abspath
        print(abspath)
        AnyMate("template.anymate")

class TestMain(unittest.TestCase):
    """The main test class for AnyMate"""

    def test_main_noparam(self):
        with self.assertRaises(TypeError):
            main()

    def test_main_intparam(self):
        with self.assertRaises(SystemExit):
            main(88)

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
            main(["bad"]*5)

    @patch("AnyMate.AnyMateGUI")
    @patch("AnyMate.AnyMate")
    def test_main_two_real_param(self, mock, guimock):
        #setup
        myfile = 'template.anymate'
        mock.return_value = "Something"
        #exercise
        main(['./AnyMate.py', myfile])
        #validate
        mock.assert_called_once_with(myfile)
        # We expect the gui to be called with the return value of AnyMate()
        guimock.assert_called_once_with("Something", myfile)

    @patch("os.path.isfile")
    def test_main_nofile(self, mock):
        #setup
        myfile = 'nofile'
        mock.return_value = False
        #exercise
        with self.assertRaises(SystemExit):
            main(['./AnyMate.py', myfile])

    @patch("os.path.isfile")
    @patch("AnyMate.AnyMateGUI")
    @patch("AnyMate.AnyMate")
    def test_main_mockedfile(self, anymock, guimock, filemock):
        #setup
        myfile = 'nofile'
        filemock.return_value = True
        #exercise
        main(['./AnyMate.py', myfile])
        #validate
        anymock.assert_called_once_with(myfile)

    @patch("os.path.isfile")
    @patch("AnyMate.AnyMateGUI")
    @patch("AnyMate.AnyMate")
    def test_main_mainloop(self, anymock, guimock, filemock):
        #setup
        myfile = 'nofile'
        filemock.return_value = True
        #Anymate() returns an AnymateObject
        anymock.return_value = MagicMock(name='AnyMate')
        gui = MagicMock(name='AnyMateGui')
        guimock.return_value = gui
        #exercise
        main(['./AnyMate.py', myfile])
        #validate
        anymock.assert_called_once_with(myfile)
        gui.rootwin.mainloop.assert_called_once_with()

    @patch("AnyMate.AnyMate")
    def test_main_four_real_param(self, mock):
        #setup
        myfile = 'template.anymate'
        conf = 'hello'
        anym = MagicMock()
        mock.return_value = anym
        #exercise
        main(['./AnyMate.py', '--nogui', conf, myfile])
        #validate
        mock.assert_called_once_with(myfile)
        anym.execute.assert_called_once_with(conf)

    @patch("AnyMate.AnyMate")
    def test_main_four_wrong_param(self, mock):
        #setup
        myfile = 'template.anymate'
        conf = 'hello'
        anym = MagicMock()
        mock.return_value = anym
        #exercise
        with self.assertRaises(SystemExit):
            main(['./AnyMate.py', 'BAM', conf, myfile])

    @patch("AnyMate.AnyMate")
    def test_main_four_wrong_file(self, mock):
        #setup
        myfile = 'nofile'
        conf = 'hello'
        anym = MagicMock()
        mock.return_value = anym
        #exercise
        with self.assertRaises(SystemExit):
            main(['./AnyMate.py', '--nogui', conf, myfile])

    @patch("os.path.isfile")
    @patch("AnyMate.AnyMate")
    def test_main_four_wrong_file_mocked(self, mock, filemock):
        #setup
        myfile = 'template.anymate'
        conf = 'hello'
        anym = MagicMock()
        mock.return_value = anym
        filemock.return_value = False
        #exercise
        with self.assertRaises(SystemExit):
            main(['./AnyMate.py', 'BAM', conf, myfile])

class TestInterpreter(unittest.TestCase):
    """The test class for the Interpreter"""

    def test_interpreter_init(self):
        Interpreter('urxvt')

    def test_interpreter_fail(self):
        with self.assertRaises(Exception):
            Interpreter('fail')

    def test_interpreter_suffix(self):
        interp=Interpreter('urxvt')
        suff = interp.get_suffix()
        exp = """echo "Press the Any-Key to Continue "\nread any-key' &"""
        self.assertEqual(suff, exp)

    def test_interpreter_prefix(self):
        interp=Interpreter('urxvt')
        suff = interp.get_prefix()
        exp = """urxvt -sl 10000 -cr BLUE -bg lightblue -fg black -e /bin/bash -c ' \n"""
        self.assertEqual(suff, exp)

    def test_interpreter_decorate(self):
        interp=Interpreter('urxvt')
        cmd = interp.decorate_command('Mate, go hom yur drunk')
        exp = interp.get_prefix()+"Mate, go hom yur drunk"+interp.get_suffix()
        self.assertEqual(cmd, exp)

if __name__ == '__main__':
    # explicitly name the module so that pythons trace function cannot
    # mess around with unittest test discovery
    unittest.main(module="test_AnyMate")
