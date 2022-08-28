import logging
import os
import subprocess

from interpreter import Interpreter

# SHELL = "nonepopen"  # := xterm | urxvt | gnome-terminal | none | win | none_win
SHELL = "xterm"  # := xterm | urxvt | gnome-terminal | none | win | none_win


class Config:
    """This class represents configuration objects"""

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

    def execute(self, callback):
        """Execute configuration Option inside an rxvt/SHELL window"""
        if self.debug:
            print('Executing:"' + self.name + '"')

        # command = self.interpreter.decorate_command_none_popen(self.text)
        command = self.interpreter.decorate_command(self.text)

        if self.debug:
            print("****************")
            print(command)
            print("****************")
        logging.info("****************")
        logging.info(command)
        logging.info("****************")

        os.system(command)
        # proc = subprocess.Popen(
        #    command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        # )

        out = ""
        # while not self.poll():
        #    try:
        #        outs, errs = proc.communicate(timeout=1)
        #        logging.info("Return %s", proc.returncode)
        #        logging.info("Pid %s", proc.pid)
        #        logging.info("Stdout %s", str(outs))
        #        logging.info("Stderr %s", str(errs))
        #        out += str(outs)
        #    except subprocess.TimeoutExpired:
        #        #proc.kill()
        #        logging.info("Timeout!")
        #        #outs, errs = proc.communicate()
        #        #out += str(outs)

        if not proc.stdout.closed:
            # out += str(proc.stdout.read())
            # print("gout", out)
            for line in proc.stdout:
                print(line)
                if callback:
                    callback(str(line) + "\n")
        else:
            logging.info("The stream is already closed")

        # logging.info("Return %s", proc.returncode)
        # logging.info("Stdout %s", str(outs))
        # logging.info("Stderr %s", str(errs))
        # out += str(outs)

        return out

    def __str__(self):
        return ('Name: "%s"; Command: "%s"; Code: "%s";') % (
            self.name,
            self.nick,
            self.text,
        )

    def get_command(self):
        """Get a command"""
        return self.text
