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


import os.path
import sys

DEBUG = False

# Debuglevel 0: No debugging outputs, 1: debugging outputs
if DEBUG:
    DEBUGLEVEL = 1
else:
    DEBUGLEVEL = 0

if sys.version_info.major < 3:
    print("Error: Please use python3  to execute."
          "Python 2 is not supported well anymore.")
    sys.exit()
else:
    import tkinter as tk

SHELL = 'xterm' # := xterm | urxvt | gnome-terminal | none

class Interpreter:
    """Class used to hide interpreter properties"""

    def __init__(self, shell):
        self.wait = False # wait with read for the any-key
        if shell == 'xterm':
            self.shell_prefix = \
            """xterm -sl 10000 -cr BLUE -bg lightblue -fg black -e /bin/bash -c ' \n"""
            if self.wait:
                self.shell_suffix = \
                """echo "Press the Any-Key to Continue "\nread any-key' &"""
            else:
                self.shell_suffix = \
                """ echo "Sleeping 5 seconds"\n sleep 5' &"""

        elif shell == 'urxvt':
            self.shell_prefix = \
            """urxvt -sl 10000 -cr BLUE -bg lightblue -fg black -e /bin/bash -c ' \n"""
            self.shell_suffix = \
            """echo "Press the Any-Key to Continue "\nread any-key' &"""

        elif shell == 'gnome-terminal':
            self.shell_prefix = \
            """gnome-terminal --hide-menubar -x /bin/bash -c '\n"""
            self.shell_suffix = \
            """echo "Press the Any-Key to Continue "\nread any-key' &"""

        elif shell == 'none':
            self.shell_prefix = \
            """/bin/bash -c ' \n"""
            self.shell_suffix = \
            """ ' &"""
        else:
            msg = 'Shell %s not found.'%shell
            print(msg)
            raise SystemError(msg)

    def decorate_command(self, command):
        """Add shell pre- and suffix"""
        return  self.shell_prefix + command + self.shell_suffix

    def get_suffix(self):
        """Return current shell suffix"""
        return self.shell_suffix

    def get_prefix(self):
        """Return current shell prefix"""
        return self.shell_prefix

class Config(object):
    """This class represents configuration objects
    """

    def __init__(self, text, name, nick, color):
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

        # check for ' signs
        if self.text.count("'") > 0:
            print("Warning the Command String \""+ \
                self.name+"\" contains a ' sign, this might confuse bash")

    def execute(self):
        """Execute configuration Option inside an rxvt/SHELL window
        """
        if DEBUGLEVEL > 0:
            print('Executing:"'+ self.name + '"')
        command = self.interpreter.decorate_command(self.text)

        if DEBUGLEVEL > 0:
            print('****************')
            print(command)
            print('****************')
        os.system(command)

    def __str__(self):
        return ('Name: \"%s\"; Command: \"%s\"; Code: \"%s\";')%\
            (self.name, self.nick, self.text)

    def get_command(self):
        """Get a command
        """
        return self.text

class AnyMate(object):
    """Class for Command execution"""

    # predefined colors (Anymate)
    RED = '#EFBFBF'
    GREEN = '#BFEFBF'
    CYAN = '#BFEFEF'
    GREY = '#BFBFBF'
    BLUE = '#BFBFEF'

    def __init__(self, filename):
        # Central list for configration options
        self.conf = []

        if os.path.isfile(filename) and filename[-8:] == ".anymate":
            print('Loading AnyMate configuration file ' + filename)
            self.read_config(filename)
        else:
            print('Unkown configuration file' + filename)
            raise SystemError('Unkown configuration file', filename)

    def get_color(self, color_string):
        """Returns predefined color string
        TODO: currently returns None when none was found -> Exeption ?
        """

        if color_string is None:
            color = None
        elif color_string == 'red':
            color = self.RED
        elif color_string == 'green':
            color = self.GREEN
        elif color_string == 'blue':
            color = self.BLUE
        elif color_string == 'gray':
            color = self.GREY
        elif color_string == 'cyan':
            color = self.CYAN
        elif color_string[0] == '#':
            if len(color_string) == 7:
                return color_string
            else:
                raise SystemError("Unknown color")
        else:
            print('Color type %s not found'%color_string)
            color = None
        return color

    def read_config(self, filename):
        """Read confif file from disk and parse
        """
        name = os.getcwd()+os.sep+filename

        # TODO Use fake global not the real one !
        exec(compile(open(name).read(), name, 'exec'), globals())

        #print locals()
        #print globals()
        command_list = globals()['commandList']

        for command in command_list:
            if len(command) != 4:
                print("Error in file " + filename)
                print("near field containing "+ command[0])
                sys.exit()

            color = self.get_color(command[2])
            self.conf.append(
                Config(
                    text=command[3],
                    name=command[0],
                    nick=command[1],
                    color=color
                    )
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
                #print item
                item.execute()
                return True

        # when no item was found
        print("Command not found")
        raise SystemError("Command not found")

# TODO: How can we write tests for this class?
class AnyMateGUI(object):
    """Responsible for creating the GUI"""

    def __init__(self, anymate, filename):
        self.options = anymate.conf

        self.save_space = False

        self.buttons = []
        self.textfields = []
        self.options_hidden = False

        # Set up the GUI
        self.rootwin = tk.Tk(className="AnyMate: "+ filename)

        # The alternatve wm_iconbitmap is buggy - will never work
        iconfile = os.path.join(sys.path[0], "icon.png")
        self.rootwin.iconphoto(True, tk.PhotoImage(file=iconfile))
        self.rootwin.resizable(width=False, height=True)
        self.rootwin.grid_rowconfigure(0, minsize=28)

        self.options_button = tk.Button(self.rootwin, text="Hide Options", \
              command=self.hide_handler)
        self.options_button.grid(column=1, row=0)

        if DEBUGLEVEL > 0:
            self.hidden_button = tk.Button(self.rootwin, text="", command=self.hidden_handler)
            self.hidden_button.grid(column=0, row=0)

        self.canvas = tk.Canvas(
            self.rootwin,
            #height=800,
            width=200,
            scrollregion=(0, 0, 100, 100),
            #background="RED",
            #borderwidth=5
            )
        self.canvas.grid(
            column=1,
            row=1,
            sticky=tk.N+tk.S+tk.E+tk.W
            )

        self.scrollbar = tk.Scrollbar(self.rootwin, orient=tk.VERTICAL)

        self.scrollbar.grid(row=1, column=0, sticky=tk.N+tk.S)
        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.rootwin.rowconfigure(0, weight=0)
        self.rootwin.rowconfigure(1, weight=1)
        self.rootwin.columnconfigure(0, weight=0)
        self.rootwin.columnconfigure(1, weight=0)
        self.mainframe = tk.Frame(self.canvas) #, background="BLUE")

        def scroll_wheel(event):
            """The mouse scroll event handler"""
            if DEBUGLEVEL > 0:
                print('scroll_wheel %i'%event.num)
            if event.num == 4:
                self.canvas.yview('scroll', -1, 'units')
            elif event.num == 5:
                self.canvas.yview('scroll', 1, 'units')

        self.scrollbar.bind('<Button-4>', scroll_wheel)
        self.scrollbar.bind('<Button-5>', scroll_wheel)

        self.rootwin.bind_all('<Button-4>', scroll_wheel)
        self.rootwin.bind_all('<Button-5>', scroll_wheel)

        #paint the frame on to the canvas -> posibillity for global scrollbar
        #http://tkinter.unpythonic.net/wiki/ScrolledFrame
        self.canvas.create_window(0, 0, anchor='nw', window=self.mainframe)
        #use wait visibility later and resize the Canvas

        self.use_row = 1
        self.use_row += 1

        for k in range(len(self.options)):
        # generate an option field
            option = self.options[k]
            self.generate_option(
                parent=self.mainframe, row=self.use_row,
                option=option, number=k)
            self.use_row += 1

        self.rootwin.wait_visibility(self.mainframe)
        self.resize_canvas()

    def resize_canvas(self):
        """Set the canvas size equal to the size of the mainframe"""
        height = self.mainframe.winfo_height()
        width = self.mainframe.winfo_width()
        self.canvas.config(height=height, width=width)
        self.canvas.config(scrollregion=(0, 0, width, height))
        if DEBUGLEVEL > 0:
            print(("The canvas should have now %ix%i pixels"%(width, height)))
            print(("The rootwin has a size of %ix%i pixels"%
                   (self.rootwin.winfo_width(), self.rootwin.winfo_height())))

    def hidden_handler(self):
        """Handler for hidden button (there in debug mode)
        """
        self.resize_canvas()

    def hide_handler(self):
        """Handler for hide button
        """
        if self.options_hidden:
            if DEBUGLEVEL > 0:
                print("Un-Hiding")
            for field in self.textfields:
                field.grid()
            self.resize_canvas()
            self.options_button.config(text="Hide Options")
            self.options_hidden = False
        else:
            if DEBUGLEVEL > 0:
                print("Hiding")
            for field in self.textfields:
                # After that, the widget still exists & it doesn't forget its attributes
                field.grid_remove()
            self.resize_canvas()
            self.options_button.config(text="Show Options")
            self.options_hidden = True

        # we need to call resize after continuing in the mainloop to
        # wait for the resize to prpopagate
        self.rootwin.after(50, self.resize_canvas)

    def quit(self):
        """Quit handler
        """
        print('exiting...')
        #killall clients
        sys.exit()

    def generate_option(self, parent, row, option, number):
        """Generates an option to click on
        """

        self.button = tk.Button(
            parent,
            text=option.name + '\n' + option.nick,
            #command= option.execute,

            # unfortunately Tkinter does not allow arguments for the Button
            # so we generate a pseudo function for that
            command=lambda: self.execute_option(number),
            bg=option.color
            )

        self.button.grid(column=0, row=row, rowspan=1, sticky=tk.W+tk.E+tk.N+tk.S)

        self.buttons.append(self.button)

        height = option.text.count('\n')

        if not self.save_space:
            height += 1

        self.textfield = tk.Text(parent, width=80, height=height)
        self.textfield.insert(tk.END, option.text)
        self.textfield.grid(
            column=1,
            columnspan=1,
            row=row,
            rowspan=1,
            sticky=tk.W+tk.E
            )
        self.textfields.append(self.textfield)

    def execute_option(self, number):
        """Handler for an option - button"""
        if DEBUGLEVEL > 0:
            print('Executing %i'%number)
        self.options[number].execute()

def print_help():
    """Helper message"""
    print('Please use "AnyMate [--nogui <cmd>] <file.anymate>"'+\
            ' to call anymate GUI.')

def main(argv):
    """Bam - Main
    """
    print('Starting AnyMate from', sys.path[0])

    if not isinstance(argv, list):
        print_help()
        sys.exit()
    if len(argv) < 2:
        print_help()
        sys.exit()

    abspath = os.path.abspath(os.path.dirname(argv[0]))
    # Everything we do now happens in this directory
    print('Switching to directory ' + abspath)
    os.chdir(abspath)

    # GUI version
    if len(argv) == 2:

        filename = argv[1]
        if not os.path.isfile(filename):
            print("File not found.")
            sys.exit()

        anymate = AnyMate(filename)
        #anymate.list()
        #anymate.command_list()
        anymategui = AnyMateGUI(anymate, filename)
        #Start the GTK Mainloop
        anymategui.rootwin.mainloop()
        print('Exiting...')

    # Commandline version
    elif len(argv) == 4:
        if argv[1] == '--nogui':
            filename = argv[3]

            if os.path.isfile(filename):
                pass
            else:
                print("File not found.")
                sys.exit()

            command = argv[2]

            anymate = AnyMate(filename)
            anymate.execute(command)
        else:
            print_help()
            sys.exit()
    else:
        # wrong amount of parameters: allowed 4 or 5
        print_help()
        sys.exit()


if __name__ == '__main__':
    print(sys.argv)
    main(sys.argv)
