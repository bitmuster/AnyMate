#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AnyMate: Automate Anything - Version 1.3 beta

Automated execution of bash code snippets via GTK-GUI or command-line.
Copyright (C) 2009 - 2023 Michael Abel

See the README file for further explanation.

Licence:

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

Infos:

  * Call it like :
      python3 AnyMate.py empty.anymate
      python3 AnyMate.py --nogui xclock template.anymate

  * Use this as as example for creating a button at the gnome panel
    xterm -e /bin/bash -c 'cd /home/micha/Koffer/Projects/AnyMate;
        ./AnyMate.py Koffer.anymate; read any_key'

  * To avoid Problems in commands please avoid the ' Character,
    this would confuse bash.

Links:
* https://github.com/bitmuster/AnyMate
* https://gitlab.com/bitmuster/anymate
"""

import logging
import os.path
import sys
import json

# from anymate_gui import AnyMateGui as gui
from ganymate import AnyMateGtkGui as gui

import config as aconf

DEBUG = True

if sys.version_info.major < 3:
    print(
        "Error: Please use python3 to execute. "
        "Python 2 is not supported here anymore."
    )
    sys.exit()


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
        self._config_list = []
        self.debug = debug
        self._gui = None
        self._terminal = None
        self._filename = filename

    def load_configuration(self):
        if os.path.isfile(self._filename) and self._filename.endswith(".json"):
            print("Loading AnyMate configuration file " + self._filename)
            self.read_json_config(self._filename)
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
            raise SystemError("Unknown color")
        else:
            print("Color type %s not found" % color_string)
            color = None
        return color

    def parse_entry_to_config(self, command, filename):
        print(command)
        if not command:
            raise SystemError(f"Cannot parse {command}")
        if len(command) != 4:
            print("Error in file " + filename)
            print("near field containing " + command[0])
            sys.exit()
        cfg = aconf.Config(
            text=command.get("cmd"),
            name=command.get("name"),
            nick=command.get("nick"),
            color=command.get("color"),
            bookmark=False,
            debug=self.debug,
        )
        return cfg

    def read_json_config(self, filename):
        thefile = open(filename)
        command_list = json.load(thefile)
        print("CommandList", command_list)

        for command in command_list:
            if self.debug:
                print("    Command", command)

            cfg = self.parse_entry_to_config(command, filename)

            # color = self.get_color(command[2])
            self._config_list.append(cfg)

    def list(self):
        """just print what is inside here"""
        for i in self._config_list:
            print(i)

    def command_list(self):
        """just print what is inside here"""
        for i in self._config_list:
            print(i.nick)

    def execute(self, command: str):
        """execute given command, only used in command line mode"""

        for item in self._config_list:
            if item.nick == command:
                print(item)
                # logging.error(item)
                if self._terminal:
                    out = item.execute(self._gui.terminal_append)
                else:
                    out = item.execute(None)

                if self._gui:
                    self._gui.build_new_run_entry(item.nick)
                if self._terminal:
                    self._gui.terminal_append(out + "\n")
                return True

        # when no item was found
        print("Command not found %s" % command)
        raise SystemError("Command not found")

    def get_config_list(self):
        """Retrieve config list"""
        return self._config_list

    def print_option(self, nick):
        for item in self._config_list:
            if item.nick == nick:
                print(item)

    def register_gui(self, gui):
        self._gui = gui

    def register_terminal(self, terminal):
        self._terminal = terminal


def print_help():
    """Helper message"""
    print(
        'Please use "AnyMate [--nogui <cmd>] <file.anymate>"' + " to call anymate GUI."
    )


def main(argv, debug=False):
    """Bam - Main"""

    if debug:
        print("Starting AnyMate from", sys.path[0], "with argv", sys.argv)

    if not isinstance(argv, list):
        print_help()
        sys.exit()
    if len(argv) < 2:
        print_help()
        sys.exit()

    abspath = os.path.abspath(os.path.dirname(argv[0]))
    # Everything we do now happens in this directory

    if debug:
        print("Switching to directory " + abspath)

    os.chdir(abspath)

    # GUI version
    if len(argv) == 2:
        filename = argv[1]
        if not os.path.isfile(filename):
            print("File not found.")
            sys.exit()

        anymate = AnyMate(filename)
        print("Ficken", anymate)
        anymate.load_configuration()
        # anymate.list()
        # anymate.command_list()
        anymategui = gui(anymate, filename)
        # Start the TK Mainloop
        anymategui.mainloop()
        if debug:
            print("Exiting mainloop...")

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
            print(anymate)
            anymate.load_configuration()
            anymate.execute(command)
        else:
            print_help()
            sys.exit()
    else:
        # wrong amount of parameters: allowed 4 or 5
        print_help()
        sys.exit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main(sys.argv, DEBUG)
