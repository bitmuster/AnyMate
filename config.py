import logging
import subprocess

from interpreter import Interpreter

# import pysnooper

SHELL = "xterm"  # := xterm | urxvt | gnome-terminal | none | win | none_win


class Config:
    """This class represents configuration objects"""

    def __init__(self, text, name, nick, color, bookmark, debug=False):
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
        self.bookmark = bookmark

        # check for ' signs
        if self.text.count("'") > 0:
            print(
                'Warning the Command String "'
                + self.name
                + "\" contains a ' sign, this might confuse bash"
            )

    # @pysnooper.snoop()
    def execute(self, callback):
        """Execute configuration Option inside an rxvt/SHELL window"""
        if self.debug:
            print('Executing:"' + self.name + '"')

        command = self.interpreter.decorate_command_popen(self.text)

        if self.debug:
            print("****************")
            print(command)
            print("****************")
        logging.info("****************")
        logging.info(command)
        logging.info("****************")

        proc = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )

        out = ""

        # TODO This will block when we run everything in a subshell
        subshell = True
        if not subshell:
            if not proc.stdout.closed:
                # out += str(proc.stdout.read())
                # print("gout", out)
                for line in proc.stdout:
                    print(line)
                    if callback:
                        callback(str(line) + "\n")
            else:
                logging.info("The stream is already closed")

        return out

    def __str__(self):
        return (f'Name: "{self.name}"; Command: "{self.nick}"; Code: "{self.text}";')

    def get_command(self):
        """Get a command"""
        return self.text

    def get_name(self):
        """Get a name"""
        return self.name

    def get_nick(self):
        """Get a nick"""
        return self.nick
