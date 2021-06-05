
import os

from interpreter import Interpreter

SHELL = "xterm"  # := xterm | urxvt | gnome-terminal | none | win | none_win

class Config:
    """This class represents configuration objects
    """

    def __init__(self, text, name, nick, color, debug=False):
        """A configuration option
       text:   The command text that is stored as configuration
       name:   The name of the command
       nick:   The nickname of the command
       color:  The color of the execution button
       """
        self.text = text
        self.name = name
        self.nick = nick
        self.color = color
        self.interpreter = Interpreter(SHELL)
        self.debug = debug

        # check for ' signs
        if self.text.count("'") > 0:
            print(
                'Warning the Command String "'
                + self.name
                + "\" contains a ' sign, this might confuse bash"
            )

    def execute(self):
        """Execute configuration Option inside an rxvt/SHELL window
        """
        if self.debug > 0:
            print('Executing:"' + self.name + '"')
        command = self.interpreter.decorate_command(self.text)

        if self.debug > 0:
            print("****************")
            print(command)
            print("****************")
        os.system(command)

    def __str__(self):
        return ('Name: "%s"; Command: "%s"; Code: "%s";') % (
            self.name,
            self.nick,
            self.text,
        )

    def get_command(self):
        """Get a command
        """
        return self.text
