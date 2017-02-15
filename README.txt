
This is a readme file for AnyMate  (Automate Anything)
======================================================
Copyright (C) 2009 - 2015 Michael Abel

Automated execution of bash code snippets via Tkinter-GUI or command-line.

AnyMate is a small desktop automation utility for lazy people. It's purpose 
is the execution of bash script snippets. It's target are scripts and 
complicated commands that to complex to remember, but are not worth enough
to write a real bash script for them. Snippets can be loaded from a 
configuration file. Before execution, they can be edited in the GUI.

Snippets can be executed via a GUI or via command-line. Before execution of a
snippet a set of commands is inserted to serve as sort of environment. The
environment can also be configured. You can for example chdir to a specific
directory or insert environment variables.

Command and environment can be executed in terminal windows or directly in the
current shell. The variable "shell" in AnyMate.py controls this behavior. Good
presets are available for urxvt and xterm.

I use this tool now on a daily basis for lots of years. It helps me to organize
all my tasks while swtiching pc's, synchronsize files and keep track of
software that is not installed via debian's package management.

Prerequisites
-------------
Anymate needs python3

Commandline:
------------

Commands/snippets can be executed via commandline in the form:

$ ./AnyMate.py --nogui hello template.anymate

Where "template.anymate" is the configuration file and "hello" the nickname of a
bash snippet. 

Graphical User Interface:
-------------------------

AnyMate can be started with GUI:

$ ./AnyMate.py template.anymate 

A simple window will open, presenting buttons at the left side and text-fields
on the right side. Every configuration option is loaded into a text field. The
first field is for the environment. If you press on one of the buttons the
commands contained in the text field right to the button is extended with the
environment and then called in a new terminal window.

You can change the commands in the GUI if you like, commands are always loaded
from the text field, but changes are not saved back to the configuration file.

Desktop integration:
--------------------

For integration into desktop systems I prefer to use a command like this one:

rxvt -e bash -c 'cd <PATH_TO_ANYMATE>/AnyMate; \
      python3 AnyMate.py  template.anymate; read'

This command can be used for example for a custom launcher in the gnome panel.
It opens an extra shell window in which Anymate is executed.


Configuration File:
-------------------

An explanation and examples how configuration files are build is contained in
the file template.anymate. Use this one as template for enhancements.

To avoid Problems in commands please avoid the ' Character,
this would confuse bash.

Example:
--------

How does AnyMate execute commands?
AnyMate glues the following parts together and calls them in a shell:
   1) shellPrefix
   2) environment
   3) command
   4) shellSuffix

The code that is executed might for example look like this:

# Prefix:
rxvt -sl 10000 -cr blue -bg pink -fg black -e /bin/bash -c '
# Environment
cd ~/
echo "Directory: $(pwd)"
# Command:
echo "Hello World"
echo "Press the Any-Key to Continue "
# Postfix:
read any-key' &

Test
----

Anymate gets an update in the test driven manner. You will observe
lots of tests. To perform this Anymate uses python unittest.
To run all the tests please execute:

$ python3 test_AnyMate.py

Here are the commands to get a simple code coverage analysis:

python3-coverage run test_AnyMate.py
python3-coverage report
python3-coverage html
