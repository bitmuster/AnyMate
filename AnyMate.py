    #!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AnyMate: Automate Anything - Version 1.1 beta
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


# Links:
# http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/index.html
# http://effbot.org/tkinterbook/
# http://www.tkdocs.com/tutorial/grid.html

# TODO: Problems with the ' Character
# TODO: Add tests with full code coverage
# TODO: Refractor all
# TODO: Find solution for weird "environment" stuff in class config
# TODO: Combine environment and checkboxes for interpreter environment
# TODO: Add Checkboxes to choose interpreter and or command window, rxvt,
#    gnome-SHELL, cmd, mintty, preambles -> Why?
# TODO: Add Windows / Cygwin profile to avoid ongoing pain with Windows OS
# TODO: Read / Store from/to XML or another suitable format
# TODO: Buttons: Save, Revert, SaveAs, Open
# TODO: Select terminal type per configuration
# TODO: Other fonts
# TODO: Switch to python logger
# TODO: Rename Config command to nick


# Infos:
#  * Use this as as example for creating a button at the gnome panel
#     xterm -e /bin/bash -c 'cd /home/micha/Koffer/Projects/AnyMate;
#         ./AnyMate.py Koffer.anymate; read any_key'
#
#  * To avoid Problems in commands please avoid the ' Character,
#     this would confuse bash.
#
# rxvt micro snippet with integrated waiting:

"""
rxvt -e /bin/bash -c '
echo "Hello World"
read' &
"""

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
    #from Tkinter import *
else:
    from tkinter import *

SHELL = 'xterm' # := xterm | urxvt | gnome-terminal | none

# This prefix is put in front every command
if SHELL == 'xterm':
    shellPrefix = \
    """xterm -sl 10000 -cr BLUE -bg lightblue -fg black -e /bin/bash -c ' \n"""
#    shellSuffix = \
#    """echo "Press the Any-Key to Continue "\nread any-key' &"""
    shellSuffix = \
    """ echo "Sleeping 5 seconds"\n sleep 5' &"""

elif SHELL == 'urxvt':
    shellPrefix = \
    """urxvt -sl 10000 -cr BLUE -bg lightblue -fg black -e /bin/bash -c ' \n"""
    shellSuffix = \
    """echo "Press the Any-Key to Continue "\nread any-key' &"""

elif SHELL == 'gnome-terminal':
    shellPrefix = \
    """gnome-terminal --hide-menubar -x /bin/bash -c '\n"""
    shellSuffix = \
    """echo "Press the Any-Key to Continue "\nread any-key' &"""

# Outputs in commands via echo get printed to the original SHELL
elif SHELL == 'none':
    shellPrefix = \
    """/bin/bash -c ' \n"""
    shellSuffix = \
    """ ' &"""
else:
    print('Shell not found.')
    sys.exit()

# Path of this script
# Can be used by other commands (is set automatically)
ABSPATH = None

# predefined colors (Anymate)
RED = '#EFBFBF'
GREEN = '#BFEFBF'
CYAN = '#BFEFEF'
GREY = '#BFBFBF'
BLUE = '#BFBFEF'

class Config(object):
    """This class represents configuration objects
    """

    def __init__(self, text, name, command, color, envobj=None):
        """A configuration option
       text:   The command text that is stored as configuration
       name:   The name of the command
       nick:   The nickname of the command
       color:  The color of the execution button
       envobj: An environment object of class config
       """
        self.text = text
        self.name = name
        self.command = command # aka nick
        self.color = color
        self.envobj = envobj

        # check for ' signs
        if self.text.count("'") > 0:
            print("Warning the Command String \""+ \
                self.name+"\" contains a ' sign, this might confuse bash")

    def execute(self):
        """Execute configuration Option inside an rxvt/SHELL window
        """
        if DEBUGLEVEL > 0:
            print('Executing:"'+ self.name + '"')
        if self.envobj:
            command = shellPrefix + self.envobj.text \
                + self.text + shellSuffix
        else:
            command = shellPrefix + self.text + shellSuffix

        if DEBUGLEVEL > 0:
            print('****************')
            print(command)
            print('****************')
        os.system(command)

    def __str__(self):
        return ('Name: \"%s\"; Command: \"%s\"; Code: \"%s\";')%\
            (self.name, self.command, self.text)

    def setCommand(self, cmd):
        # Currently only allowed for environment objects (why ?)
        if self.envobj:
            self.text = cmd
        else:
            print('Command is not a environment Object')

    def getCommand(self):
        return self.text

    def setEnvironment(self, env):
        # This can only happen when the Config object is of type envobject
        if self.envobj is None:
            self.text = env
        else:
            print('Object is a environment Object')

class AnyMate(object):
    """Class for Command execution"""

    def __init__(self, filename):
        self.environment = None
        # Central list for configration options
        self.conf = []

        if os.path.isfile(filename) and filename[-8:] == ".anymate":
            print('Loading AnyMate configuration file ' + filename)
            self.readAnyMate(filename)
        else:
            print('Unkown configuration file' + filename)
            raise SystemError("'Unkown configuration file' + filename")

    def getcolor(self, colorString):
        """Returns predefined color string
        TODO: currently returns None when none was found -> Exepton ?
        """
        if colorString is None:
            color = None
        elif colorString == 'RED':
            color = RED
        elif colorString == 'GREEN':
            color = GREEN
        elif colorString == 'BLUE':
            color = BLUE
        elif colorString == 'GREY':
            color = GREY
        elif colorString == 'CYAN':
            color = CYAN
        elif colorString[0] == '#':
            if len(colorString) == 7:
                return colorString
            else:
                raise SystemError("Unknown color")
        else:
            print('Color type %s not found'%colorString)
            color = None
        return color

    def readAnyMate(self, filename):
        name = os.getcwd()+os.sep+filename

        #print(globals())
        #assert( ABSPATH != None) #Would be nice,but we cannot test this well

        # TODO Use fake global not the real one !
        exec(compile(open(name).read(), name, 'exec'), globals())

        #print locals()
        #print globals()
        commandList = globals()['commandList']
        environment = globals()['environment']

        field = environment
        if len(field) != 4:
            print("Error in file " + filename)
            print("near field containing "+ field[0])
            sys.exit()

        color = self.getcolor(field[2])
        self.environment = \
            Config(
                text=field[3],
                name=field[0],
                command=field[1],
                color=color
                )
        for command in commandList:
            if len(command) != 4:
                print("Error in file " + filename)
                print("near field containing "+ command[0])
                sys.exit()

            color = self.getcolor(command[2])
            self.conf.append(
                Config(
                    text=command[3],
                    name=command[0],
                    command=command[1],
                    color=color,
                    envobj=self.environment
                    )
                )

    def list(self):
        """just print what is inside here"""
        for i in self.conf:
            print(i)

    def commandList(self):
        """just print what is inside here"""
        for i in self.conf:
            print(i.command)

    def execute(self, command):
        """execute given command, only used in command line mode"""

        for item in self.conf:
            if item.command == command:
                #print item
                item.execute()
                return True

        if self.environment.command == command:
            self.environment.execute()
            return True

        # when no item was found
        print("Command not found")
        raise SystemError("Command not found")

class AnyMateGUI(object):
    """Responsible for creating the GUI
    TODO: How can we writetests for this class?
    """

    def __init__(self, anymate, filename):
        self.environment = anymate.environment
        self.options = anymate.conf

        self.save_space = False

        self.buttons = []
        self.textfields = []
        self.optionsHidden = False

        # Set up the GUI
        self.rootwin = Tk(className="AnyMate: "+ filename)

        # The alternatve wm_iconbitmap is buggywill never work
        iconfile = os.path.join(sys.path[0], "icon.png")
        self.rootwin.iconphoto(True, PhotoImage(file=iconfile))
        self.rootwin.resizable(width=False, height=True)
        self.rootwin.grid_rowconfigure(0, minsize=28)

        self.optionsButton = Button(self.rootwin, text="Hide Options", \
              command=self.hide_handler)
        self.optionsButton.grid(column=1, row=0)

        if DEBUGLEVEL  > 0:
            self.hiddenButton = Button(self.rootwin, text="", command=self.hidden_handler)
            self.hiddenButton.grid(column=0, row=0)

        self.canvas = Canvas(
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
            sticky=N+S+E+W
            )

        self.scrollbar = Scrollbar(self.rootwin, orient=VERTICAL)

        self.scrollbar.grid(row=1, column=0, sticky=N+S)
        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.rootwin.rowconfigure(0, weight=0)
        self.rootwin.rowconfigure(1, weight=1)
        self.rootwin.columnconfigure(0, weight=0)
        self.rootwin.columnconfigure(1, weight=0)
        self.mainframe = Frame(self.canvas) #, background="BLUE")

        def scrollWheel(event):
            if DEBUGLEVEL > 0:
                print('scrollWheel %i'%event.num)
            if event.num == 4:
                self.canvas.yview('scroll', -1, 'units')
            elif event.num == 5:
                self.canvas.yview('scroll', 1, 'units')

        self.scrollbar.bind('<Button-4>', scrollWheel)
        self.scrollbar.bind('<Button-5>', scrollWheel)

        self.rootwin.bind_all('<Button-4>', scrollWheel)
        self.rootwin.bind_all('<Button-5>', scrollWheel)

        #paint the frame on to the canvas -> posibillity for global scrollbar
        #http://tkinter.unpythonic.net/wiki/ScrolledFrame
        self.canvas.create_window(0, 0, anchor='nw', window=self.mainframe)
        #use wait visibility later and resize the Canvas

        self.useRow = 1
        self.useRow += 1
        # generate the environment field
        self.generateOption(
            parent=self.mainframe, row=self.useRow,
            option=self.environment, number=0)
        self.useRow += 1

        for k in range(len(self.options)):
        # generate an option field
            option = self.options[k]
            self.generateOption(
                parent=self.mainframe, row=self.useRow,
                option=option, number=k+1)
            self.useRow += 1

        self.rootwin.wait_visibility(self.mainframe)
        self.resizeCanvas()

    def resizeCanvas(self):
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
        self.resizeCanvas()

    def hide_handler(self):
        if self.optionsHidden:
            if DEBUGLEVEL > 0:
                print("Un-Hiding")
            for field in self.textfields:
                field.grid()
            self.resizeCanvas()
            self.optionsButton.config(text="Hide Options")
            self.optionsHidden = False
        else:
            if DEBUGLEVEL > 0:
                print("Hiding")
            for field in self.textfields:
                # After that, the widget still exists & it doesn't forget its attributes
                field.grid_remove()
            self.resizeCanvas()
            self.optionsButton.config(text="Show Options")
            self.optionsHidden = True

        # we need to call resize after continuing in the mainloop to
        # wait for the resize to prpopagate
        self.rootwin.after(50, self.resizeCanvas)

    def quit(self):
        print('exiting...')
        #killall clients
        sys.exit()

    def generateOption(self, parent, row, option, number):

        self.button = Button(
            parent,
            text=option.name + '\n' + option.command,
            #command= option.execute,

            # unfortunately Tkinter does not allow arguments for the Button
            # so we generate a pseudo function for that
            command=lambda: self.executeOption(number),
            bg=option.color
            )

        self.button.grid(column=0, row=row, rowspan=1, sticky=W+E+N+S)

        self.buttons.append(self.button)

        height = option.text.count('\n')

        if not self.save_space:
            height += 1

        self.textfield = Text(parent, width=80, height=height)
        self.textfield.insert(END, option.text)
        self.textfield.grid(
            column=1,
            columnspan=1,
            row=row,
            rowspan=1,
            sticky=W+E
            )
        self.textfields.append(self.textfield)

    def executeOption(self, number):
        self.updateTextfield(number)
        if number == 0:
            if DEBUGLEVEL > 0:
                print('Executing Environment')

            self.environment.execute()
        else:
            if DEBUGLEVEL > 0:
                print('Executing %i'%number)
            # currently the option list is one element smaller since there is no
            # environment in the options list from Anymate
            self.options[number -1].execute()

    def updateTextfield(self, number):
        text = self.textfields[number].get("0.0", END)
        if DEBUGLEVEL > 0:
            print(text)
        if number == 0:
            self.environment.setEnvironment(text)
        else:
            self.updateTextfield(0)
            # currently the option list is one element smaller since
            # there is no environment Object at the beginning
            # in the options list from Anymate
            self.options[number-1].setCommand(text)

def main(argv):
    print('Starting AnyMate from', sys.path[0])

    if type(argv) != list:
        sys.exit()
    if len(argv) < 2:
        sys.exit()

    global ABSPATH
    ABSPATH = os.path.abspath(os.path.dirname(argv[0]))
    print('Switching to directory ' + ABSPATH)
    os.chdir(ABSPATH)

    # GUI version
    if len(argv) == 2:

        filename = argv[1]
        if not os.path.isfile(filename):
            print("File not found.")
            sys.exit()

        anymate = AnyMate(filename)
        #anymate.list()
        #anymate.commandList()
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
            #elif os.path.ABSPATH( os.path.dirname(sys.argv[0]) ) + filename:
            #   pass
            else:
                print("File not found.")
                sys.exit()

            command = argv[2]

            anymate = AnyMate(filename)
            anymate.execute(command)
        else:
            sys.exit()
    else:
        # wrong amount of parameters: allowed 4 or 5
        print('Please use "AnyMate [--nogui <cmd>] <file.anymate>"'+\
            ' to call anymate GUI.')
        sys.exit()

if __name__ == '__main__':
    print(sys.argv)
    main(sys.argv)
