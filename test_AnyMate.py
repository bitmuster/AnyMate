
# 4 Phase test pattern (from Osherove?)
# Setup-Exercise-Verify-Cleanup

# See also:
# https://docs.python.org/3.5/library/unittest.html
# https://docs.python.org/3.5/library/unittest.mock.html

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
        expected="Name: \"name\"; Command: \"command\"; Code: \"text\";"

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

#    def setUp(self):
#        #The abspath is used to set values in the configfile
#        global abspath
#        abspath="SomePath"
#
#    def tearDown(self):
#        global abspath
#        abspath=None

    def test_init(self):
        a=AnyMate("empty.anymate")
        a.list()
        a.commandList()

    def test_init_deprecated(self):
        with self.assertRaises( SystemError ):
            a=AnyMate("empty.taomate")

    def test_fail(self):
        with self.assertRaises( SystemError ):
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
        self.assertEqual( a.getcolor(None), None)
        self.assertEqual( a.getcolor("#FFFFFF"), "#FFFFFF")


    def test_getcolor_badfail(self):
        a=AnyMate("empty.anymate")
        with self.assertRaises( SystemError ):
            a.getcolor("#FF")

    def test_readAnyMate(self):
        """We read the example file, we know the content"""
        a=AnyMate("empty.anymate")
        self.assertEqual( a.conf[0].name, "Hello World" )
        self.assertEqual( a.conf[0].command, "hello" )
        self.assertEqual( a.conf[0].text, 'echo "Hello World!"\n' )
        self.assertEqual( a.conf[0].color, '#ddffdd' )

        self.assertEqual( a.conf[0].envobj.name, 'Environment Settings' )

    @patch("AnyMate.Config.execute")
    def test_execute(self, exmock):
        a=AnyMate("empty.anymate")
        a.execute("hello")

    @patch("AnyMate.Config.execute")
    def test_execute_fail(self, exmock):
        a=AnyMate("empty.anymate")
        with self.assertRaises(SystemError):
            a.execute("no")

    @patch("os.system")
    def test_execute_os_mocked(self, osmock):
        a=AnyMate("empty.anymate")
        a.execute("hello")
        call='xterm -sl 10000 -cr blue -bg lightblue -fg black -e /bin/bash -c \' \ncd ~/\necho "Directory: $(pwd)"\necho "Hello World!"\n echo "Sleeping 5 seconds"\n sleep 5\' &'
        osmock.assert_called_with(call)

class TestClassAnyMateTemplate(unittest.TestCase):

    def disabled_test_init(self):
        """Just load it to see if it loads,
        TODO: Remove abspath from this place
        """
        abspath=os.path.abspath( os.path.dirname(sys.argv[0]) )
        print('Switching to directory ' + abspath)
        os.chdir( abspath )
        print(AnyMate.abspath)
        AnyMate.abspath=abspath
        print(AnyMmate.abspath)
        a=AnyMate("template.anymate")

class TestMain(unittest.TestCase):

    def test_main_noparam(self):
        with self.assertRaises(TypeError):
            main()

    def test_main_listparam(self):
        with self.assertRaises(SystemExit):
            main([])

    def test_main_one_param(self):
        with self.assertRaises(SystemExit):
            main(["one"])

    def test_main_three_param(self):
        with self.assertRaises(SystemExit):
            main(["one", "two", "three"])

    @patch("AnyMate.AnyMateGUI")
    @patch("AnyMate.AnyMate")
    def test_main_two_real_param(self, mock, guimock):
        #setup
        f='template.anymate'
        mock.return_value="Something"
        #exercise
        main(['./AnyMate.py', f])
        #validate
        mock.assert_called_once_with(f)
        # We expect the gui to be called with the return value of AnyMate()
        guimock.assert_called_once_with("Something",f)

    @patch("os.path.isfile")
    def test_main_nofile(self, mock):
        #setup
        f='nofile'
        mock.return_value=False
        #exercise
        with self.assertRaises(SystemExit):
            main(['./AnyMate.py', f])

    @patch("os.path.isfile")
    @patch("AnyMate.AnyMateGUI")
    @patch("AnyMate.AnyMate")
    def test_main_mockedfile(self, anymock, guimock, filemock):
        #setup
        f='nofile'
        filemock.return_value=True
        #exercise
        main(['./AnyMate.py', f])
        #validate
        anymock.assert_called_once_with(f)

    @patch("os.path.isfile")
    @patch("AnyMate.AnyMateGUI")
    @patch("AnyMate.AnyMate")
    def test_main_mainloop(self, anymock, guimock, filemock):
        #setup
        f='nofile'
        filemock.return_value=True
        #Anymate() returns an AnymateObject
        anymock.return_value=MagicMock(name='AnyMate')
        gui=MagicMock(name='AnyMateGui')
        guimock.return_value=gui
        #exercise
        main(['./AnyMate.py', f])
        #validate
        anymock.assert_called_once_with(f)
        gui.rootwin.mainloop.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()
