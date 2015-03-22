#!/usr/bin/env python
# -*- coding: utf-8 -*-

# AnyMate: Automate Anything - Version 1.0
#
# Automated execution of bash code snippets via Tkinter-GUI or Commandline.
# Copyright (C) 2009 - 2015 Michael Abel
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


# Links
# http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/index.html
# http://effbot.org/tkinterbook/

# TODO: Find solution for weird "environment" stuff
# TODO: Combine environment and checkboxes for interpreter environment
# TODO: Color Picker ?
# TODO: Add Checkboxes to choose interpreter and or command window, rxvt, gnome-shell, cmd, mintty, preambles
# TODO: Add Windows / Cygwin profile to avoid ongoing pain
# TODO: Read / Store from/to XML
# TODO: Buttons: Save, Revert, SaveAs, Open
# TODO: Select terminal type per configuration
# TODO: Other fonts
# TODO: Remove Taomate dependencies

# TODO:Problems with the ' Character,
# TODO: -> so try to enhance this first:

#rxvt -e /bin/bash -c '
#echo "Hello World"
#read any-key' &

# DONE: Permission denied
# micha@ganymed:~/Koffer/Projects/AnyMate$ ./AnyMate.py template.anymate 
# bash: ./AnyMate.py: /usr/bin/env: bad interpreter: Permission denied
# mount -o remount,exec /dev/DEVICE solved it

# Use this as as example for creating a button at the gnome panel
# xterm -e /bin/bash -c 'cd /home/micha/Koffer/Projects/AnyMate; ./AnyMate.py Koffer.anymate; read any_key'

# To avoid Problems in commands please avoid the ' Character,
# this would confuse bash.

import os
import os.path
import sys
import time

debug=False

# Debuglevel 0: No debugging outputs, 1: debugging outputs
if debug:
    debuglevel=1
else:
    debuglevel=0

shell='xterm' # := xterm | urxvt | gnome-terminal | none

# This prefix is put in front every command
if shell=='xterm':
    shellPrefix=\
    """xterm -sl 10000 -cr blue -bg lightblue -fg black -e /bin/bash -c ' \n"""
#    shellSuffix=\
#    """echo "Press the Any-Key to Continue "\nread any-key' &"""
    shellSuffix=\
    """ echo "Sleeping 5 seconds"\n sleep 5' &"""

elif shell=='urxvt':
    shellPrefix=\
    """urxvt -sl 10000 -cr blue -bg lightblue -fg black -e /bin/bash -c ' \n"""
    shellSuffix=\
    """echo "Press the Any-Key to Continue "\nread any-key' &"""

elif shell=='gnome-terminal':
    shellPrefix=\
    """gnome-terminal --hide-menubar -x /bin/bash -c '\n"""
    shellSuffix=\
    """echo "Press the Any-Key to Continue "\nread any-key' &"""

# Outputs in commands via echo get printed to the original shell
elif shell=='none':
    shellPrefix=\
    """/bin/bash -c ' \n"""
    shellSuffix=\
    """ ' &"""
else:
    print ('Shell not found.')
    sys.exit()

# Path of this script
# Can be used by other commands (is set automatically)
abspath=None

# predefined colors (Anymate)
red=    '#EFBFBF'
green=  '#BFEFBF'
cyan=   '#BFEFEF'
gray=   '#BFBFBF'
blue=   '#BFBFEF'

# Old color style (Taomate)
redbg=      '#EFBFBF'
cmdbg=      '#BFEFBF'
cmdbg2=     '#BFEFEF'
configbg=   '#BFBFBF'
kofferbg=   '#BFBFEF'


class Config (object):
    """This class represents configuration objects
    """
    
    def __init__(self,text,name,command,color,envobj=None):
        """A configuration option
       text:   The command text that is stored as configuration
       name:   The name of the command
       nick:   The nickname of the command
       color:  The color of the execution button
       envobj: An environment object of class config
       """
        self.text=text
        self.name=name
        self.command=command # aka nick
        self.color=color
        self.envobj=envobj

        # check for ' signs
        if self.text.count("'") > 0:
            print "Warning the Command String \""+ \
                self.name+"\" contains a ' sign, this might confuse bash"

    def execute(self):
        """Execute configuration Option inside an rxvt/shell window
        """
        #os.system('rxvt -e echo hallo' )
        if debuglevel >0:
            print 'Executing:"'+ self.name + '"'
        if self.envobj:
            c= shellPrefix + self.envobj.text+ self.text + shellSuffix
        else:
            #self.update()
            c= shellPrefix + self.text + shellSuffix

        if debuglevel >0:
            print '****************'
            print c
            print '****************'
        os.system(c)

    def __str__(self):
        return ('Name: %s\nCommand: %s\nCode:\n%s')%\
            (self.name, self.command, self.text)

    def setCommand(self, cmd):
        if self.envobj:
            self.text=cmd
        else:
            print 'Command is not a environment Object'

    def setEnvironment(self, env):
        if self.envobj==None:
            self.text=env
        else:
            print 'Object is a environment Object'

class AnyMate(object):
    """Class for Command execution"""
    def __init__(self, filename):
        self.environment=None
        # Central list for configration options
        self.conf=[]

        if os.path.isfile(filename) and ".taomate"==filename[-8:]:
            print 'Loading TAOMate configuration file ' + filename
            self.readLegacyTAOMate(filename)
        elif os.path.isfile(filename) and ".anymate"==filename[-8:]:
            print 'Loading AnyMate configuration file ' + filename
            self.readAnyMate(filename)
        else:
            print 'Unkown configuration file' + sys.argv[1]
            sys.exit()

    def getcolor(self,s):
            if s == None:
                color=None
            elif s == 'red':
                color=red
            elif s == 'green':
                color=green
            elif s == 'blue':
                color=blue
            elif s == 'gray':
                color=gray
            elif s == 'cyan':
                color=cyan

            # Old color stlye ( *.taomate)
            elif s == 'redbg':
                color=redbg
            elif s == 'cmdbg':
                color=cmdbg
            elif s == 'cmdbg2':
                color=cmdbg2
            elif s == 'configbg':
                color=configbg
            elif s == 'kofferbg':
                color=kofferbg
            elif s[0]=='#':
                return s
            else:
                print 'Color type %s not found'%s
                color=None
            return color

    def readLegacyTAOMate(self, filename):
        name=os.getcwd()+os.sep+filename
        execfile(name,globals())
        #print locals()
        #print globals()
        fieldList=globals()['fieldList']
        environment=globals()['environment']

        field=environment
        color=self.getcolor( field[3] )
        self.environment=\
            Config( field[0], field[1], field[2], color  )

        for field in fieldList:
            color=self.getcolor( field[3] )
            self.conf.append(
                Config( field[0], field[1], field[2], color, 
                    envobj=self.environment )
                )

    def readAnyMate(self, filename):
        name=os.getcwd()+os.sep+filename
        execfile(name,globals())
        #print locals()
        #print globals()
        commandList=globals()['commandList']
        environment=globals()['environment']

        field=environment
        if len(field) != 4:
            print "Error in file " + filename
            print "near field containing "+ field[0]
            sys.exit()

        color=self.getcolor( field[2] )
        self.environment=\
            Config(
                text=field[3],
                name=field[0],
                command=field[1],
                color=color
                )
        for command in commandList:
            if len(command) != 4:
                print "Error in file " + filename
                print "near field containing "+ command[0]
                sys.exit()

            color=self.getcolor( command[2] )
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
            print i

    def commandList(self):
        """just print what is inside here"""
        for i in self.conf:
            print i.command

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
        print "Command not found"
        return False

class AnyMateGUI(object):
    """Responsible for creating the GUI"""
    
    def __init__(self, anymate):
        self.environment= anymate.environment;
        self.options= anymate.conf;

        self.save_space= False

        self.buttons=[]
        self.textfields=[]
        self.optionsHidden=False

        # Set up the GUI
        self.rootwin=Tk(className="AnyMate: "+ filename)
        #self.rootwin.resizable(width=True, height=True)
        #self.rootwin.iconbitmap(default="/mnt/Koffer/Projects/AnyMate/icon.ico")
        #self.rootwin.iconbitmap(bitmap="@/mnt/Koffer/Projects/AnyMate/icon.xbm")
        #self.rootwin.iconbitmap(bitmap="@icon.xbm")

        self.rootwin.resizable(width=True, height=True)
        self.basegrid = self.rootwin

        self.optionsButton=Button( self.basegrid, text="Hide Options", command=self.hide_handler)
        self.optionsButton.grid(column=1,row=0)

        if debug:
            self.hiddenButton=Button( self.basegrid, text="", command=self.hidden_handler)
            self.hiddenButton.grid(column=0,row=0)


        self.canvas= Canvas(
            self.basegrid,
            #height=800,
            width=200,
            scrollregion=(0,0,100,100),
            #background="red",
            #borderwidth=5
            )
        self.canvas.grid(
            column=1,
            row=1,
            sticky=N+S+E+W
            )

        self.scrollbar=Scrollbar(self.basegrid,orient=VERTICAL)

        self.scrollbar.grid(row=1,column=0,sticky=N+S)
        self.scrollbar.config( command=self.canvas.yview )
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.basegrid.rowconfigure(0, weight=1)
        self.basegrid.columnconfigure(0, weight=1)
        self.basegrid.columnconfigure(1, weight=0)
        self.mainframe= Frame(self.canvas)#, background="blue")

        def scrollWheel(event):
            if event.num == 4:
                self.canvas.yview('scroll', -1, 'units')
            elif event.num == 5:
                self.canvas.yview('scroll', 1, 'units')

        self.scrollbar.bind('<Button-4>', scrollWheel)
        self.scrollbar.bind('<Button-5>', scrollWheel)

        self.basegrid.bind_all('<Button-4>', scrollWheel)
        self.basegrid.bind_all('<Button-5>', scrollWheel)

        #paint the frame on to the canvas -> posibillity for global scrollbar
        #http://tkinter.unpythonic.net/wiki/ScrolledFrame
        self.canvas.create_window(0,0, anchor='nw', window=self.mainframe)
        #use wait visibility later and resize the Canvas

        self.useRow=1;
        self.useRow+=1
        # generate the environment field
        self.generateOption(parent=self.mainframe, row=self.useRow,
            option=self.environment, number=0)
        self.useRow+=1

        for k in range(len(self.options)):
        # generate an option field
            option=self.options[k]
            self.generateOption(parent=self.mainframe, row=self.useRow,
                option=option, number=k+1)
            self.useRow+=1
        
        self.basegrid.wait_visibility(self.mainframe)
        self.resizeCanvas()

    def resizeCanvas(self):
        """Set the canvas size equal to the size of the mainframe"""
        height= self.mainframe.winfo_height()
        width=self.mainframe.winfo_width()
        self.canvas.config ( height=height, width=width)
        self.canvas.config (scrollregion=(0,0,width,height))
        if debuglevel >0 :
            print("The canvas should have now %ix%i pixels"%(width,height))
        
        
    def hidden_handler(self):
            self.resizeCanvas()
        
    def hide_handler (self):
        if self.optionsHidden:
            if debuglevel >0:
                print ("Un-Hiding")
            for field in self.textfields:
                field.grid()
            self.resizeCanvas()
            self.optionsButton.config(text="Hide Options")
            self.optionsHidden=False
        else:
            if debuglevel >0:
                print ("Hiding")
            for field in self.textfields:
                field.grid_remove() # After that, the widget still exists & it doesn't forget its attributes
            self.resizeCanvas()
            self.optionsButton.config(text="Show Options")
            self.optionsHidden=True
        
        # Fixme:
        # we need to call resize after continuing in the mainloop to wait for the resize to prpopagate
        self.rootwin.after(50, self.resizeCanvas)
        
    def quit(self):
        print 'exiting...'
        #killall clients
        sys.exit()

    def generateOption(self, parent, row, option, number):

        self.button=Button(
            parent,
            text=option.name + '\n' + option.command,
            #command= option.execute,

            # unfortunately Tkinter does not allow arguments for the Button
            # so we generate a pseudo function for that
            command= lambda:self.executeOption(number),

            bg=option.color
            )
        self.button.grid(column=0,row=row, rowspan=1, sticky=W+E+N+S)

        self.buttons.append(self.button)

        height=option.text.count('\n')

        if not self.save_space:
            height +=1;

        self.textfield=Text(parent, width=80, height=height)
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
        if number==0:
            if debuglevel >0:
                print 'Executing Environment'

            self.environment.execute()
        else:
            if debuglevel >0:
                print 'Executing %i'%number
            # currently the option list is one element smaller since there is no
            # environment in the options list from Anymate
            self.options[number -1].execute()

    def updateTextfield(self, number):
            text=self.textfields[number].get("0.0",END)
            if debuglevel >0:
                print text
            if number==0:
                self.environment.setEnvironment(text)
            else:
                self.updateTextfield(0)
                # currently the option list is one element smaller since 
                # there is no environment Object at the beginning
                # in the options list from Anymate
                self.options[number-1].setCommand(text)

if __name__=='__main__':
    print 'Starting AnyMate'
    #print  sys.argv
    #print os.path.dirname(sys.argv[0])
    abspath=os.path.abspath( os.path.dirname(sys.argv[0]) )
    print 'Switching to directory ' + abspath
    os.chdir( abspath )
    
    
    # GUI version
    if len(sys.argv) ==2:
        from Tkinter import *

        filename=sys.argv[1]
        if not os.path.isfile(filename):
            print "File not found."
            sys.exit()

        anymate=AnyMate(filename)
        #anymate.list()
        #anymate.commandList()
        anymategui=AnyMateGUI( anymate )
        #Start the GTK Mainloop
        anymategui.rootwin.mainloop()
        print 'Exiting...'

    # Commandline version
    elif len(sys.argv) ==4:
        if sys.argv[1] == '--nogui':
            filename=sys.argv[3]

            if os.path.isfile(filename):
                pass
            #elif os.path.abspath( os.path.dirname(sys.argv[0]) ) + filename:
            #   pass
            else:
                print "File not found."

            command=sys.argv[2]

            anymate=AnyMate(filename)
            anymate.execute(command)
    else:
        # wrong amount of parameters
        print 'Please use "anymate [--nogui <cmd>] <file.anymate>"'+\
            ' to call anymate GUI.'
        sys.exit()
