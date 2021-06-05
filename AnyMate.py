#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AnyMate: Automate Anything - Version 1.2 beta
#
# Automated execution of bash code snippets via Tkinter-GUI or command-line.
# Copyright (C) 2009 - 2017 Michael Abel
#
# See the README file for further explanation.
#
# Licence:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Infos:
#
#  * Call it like :
#       python3 AnyMate.py empty.anymate
#       python3 AnyMate.py --nogui xclock template.anymate
#
#  * Use this as as example for creating a button at the gnome panel
#     xterm -e /bin/bash -c 'cd /home/micha/Koffer/Projects/AnyMate;
#         ./AnyMate.py Koffer.anymate; read any_key'
#
#  * To avoid Problems in commands please avoid the ' Character,
#     this would confuse bash.
#
# rxvt micro snippet with integrated waiting:

# Links:
# http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/index.html
# http://effbot.org/tkinterbook/
# http://www.tkdocs.com/tutorial/grid.html

# TODO: Avoid Problems with the ' Character
# TODO: Add tests with full code coverage
# TODO: Refractor all
# TODO: Add Checkboxes to choose interpreter and or command window, rxvt,
#    gnome-shell, cmd, mintty, python -> Why?
# TODO: Add Windows / Cygwin profile to avoid ongoing pain with Windows OS
# TODO: Read / Store from/to XML or another suitable format
# TODO: Buttons: Save, Revert, SaveAs, Open
# TODO: Select terminal type per configuration
# TODO: Switch to python logger
# TODO: Rename Config command to nick
# TODO: Read configs from separate files in subfolder
# TODO: Windows: avoid \U : SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 45-46: truncated \UXXXXXXXX escape
# TODO: Improve Windwos support
# TODO: Support mulitple lines under Windows (^) ?

import os.path
import sys

from anymate_gui import AnyMateGui as gui
import config as aconf

DEBUG = True

# Debuglevel 0: No debugging outputs, 1: debugging outputs
if DEBUG:
    DEBUGLEVEL = 1
else:
    DEBUGLEVEL = 0

if sys.version_info.major < 3:
    print(
        "Error: Please use python3 to execute. "
        "Python 2 is not supported here anymore."
    )
    sys.exit()
else:
    import tkinter as tk
    import tkinter.scrolledtext as tks
    import tkinter.ttk as ttk


class AnyMate:
    """Class for Command execution"""

    # predefined colors (Anymate)
    RED = "#EFBFBF"
    GREEN = "#BFEFBF"
    CYAN = "#BFEFEF"
    GREY = "#BFBFBF"
    BLUE = "#BFBFEF"

    def __init__(self, filename, debug=False):
        # Central list for configration options
        self.conf = []
        self.debug = debug

        if os.path.isfile(filename) and filename[-8:] == ".anymate":
            print("Loading AnyMate configuration file " + filename)
            self.read_config(filename)
        else:
            print("Unkown configuration file" + filename)
            raise SystemError("Unkown configuration file", filename)

    def get_color(self, color_string):
        """Returns predefined color string
        TODO: currently returns None when none was found -> Exeption ?
        """

        if color_string is None:
            color = None
        elif color_string == "red":
            color = self.RED
        elif color_string == "green":
            color = self.GREEN
        elif color_string == "blue":
            color = self.BLUE
        elif color_string == "gray":
            color = self.GREY
        elif color_string == "cyan":
            color = self.CYAN
        elif color_string[0] == "#":
            if len(color_string) == 7:
                return color_string
            else:
                raise SystemError("Unknown color")
        else:
            print("Color type %s not found" % color_string)
            color = None
        return color

    def read_config(self, filename):
        """Read config file from disk and parse
        """

        # Derive absolute path by current working directory
        name = os.path.abspath(filename)

        # TODO Use fake global not the real one !
        exec(compile(open(name).read(), name, "exec"), globals())

        # Derive variable commandList from global dictionary
        command_list = globals()["commandList"]

        for command in command_list:
            if len(command) != 4:
                print("Error in file " + filename)
                print("near field containing " + command[0])
                sys.exit()

            color = self.get_color(command[2])
            self.conf.append(
                aconf.Config(text=command[3], name=command[0], nick=command[1], color=color, debug=self.debug)
            )

    def list(self):
        """just print what is inside here"""
        for i in self.conf:
            print(i)

    def command_list(self):
        """just print what is inside here"""
        for i in self.conf:
            print(i.nick)

    def execute(self, command):
        """execute given command, only used in command line mode"""

        for item in self.conf:
            if item.nick == command:
                # print item
                item.execute()
                return True

        # when no item was found
        print("Command not found")
        raise SystemError("Command not found")


def print_help():
    """Helper message"""
    print(
        'Please use "AnyMate [--nogui <cmd>] <file.anymate>"' + " to call anymate GUI."
    )


def main(argv, debug=False):
    """Bam - Main"""

    if debug > 0:
        print("Starting AnyMate from", sys.path[0], "with argv", sys.argv)

    if not isinstance(argv, list):
        print_help()
        sys.exit()
    if len(argv) < 2:
        print_help()
        sys.exit()

    abspath = os.path.abspath(os.path.dirname(argv[0]))
    # Everything we do now happens in this directory

    if debug > 0:
        print("Switching to directory " + abspath)
    os.chdir(abspath)

    # GUI version
    if len(argv) == 2:

        filename = argv[1]
        if not os.path.isfile(filename):
            print("File not found.")
            sys.exit()

        anymate = AnyMate(filename)
        # anymate.list()
        # anymate.command_list()
        anymategui = gui(anymate, filename)
        # Start the GTK Mainloop
        anymategui.rootwin.mainloop()
        if debug > 0:
            print("Exiting...")

    # Commandline version
    elif len(argv) == 4:
        if argv[1] == "--nogui":
            filename = argv[3]

            if os.path.isfile(filename):
                pass
            else:
                print("File not found.")
                sys.exit()

            command = argv[2]

            anymate = AnyMate(filename, debug)
            anymate.execute(command)
        else:
            print_help()
            sys.exit()
    else:
        # wrong amount of parameters: allowed 4 or 5
        print_help()
        sys.exit()


if __name__ == "__main__":
    main(sys.argv, DEBUGLEVEL)
