

class Interpreter:
    """Class used to hide interpreter properties"""

    def __init__(self, shell):
        self.wait = False  # wait with read for the any-key
        if shell == "xterm":
            self.shell_prefix = """xterm -sl 10000 -cr BLUE -bg lightblue -fg black -e /bin/bash -c ' \n"""
            if self.wait:
                self.shell_suffix = (
                    """echo "Press the Any-Key to Continue "\nread any-key' &"""
                )
            else:
                self.shell_suffix = """ echo "Sleeping 5 seconds"\n sleep 5' &"""

        elif shell == "urxvt":
            self.shell_prefix = """urxvt -sl 10000 -cr BLUE -bg lightblue -fg black -e /bin/bash -c ' \n"""
            self.shell_suffix = (
                """echo "Press the Any-Key to Continue "\nread any-key' &"""
            )

        elif shell == "gnome-terminal":
            self.shell_prefix = """gnome-terminal --hide-menubar -x /bin/bash -c '\n"""
            self.shell_suffix = (
                """echo "Press the Any-Key to Continue "\nread any-key' &"""
            )

        elif shell == "none":
            self.shell_prefix = """/bin/bash -c ' \n"""
            self.shell_suffix = """ ' &"""

        elif shell == "none_win":  # Windows cmd.exe without own window
            self.shell_prefix = """cmd.exe /C  """
            # self.shell_suffix = \
            # """ & echo Press the any-key & pause"""
            self.shell_suffix = """ """

        elif shell == "win":  # Windows cmd.exe in own window
            self.shell_prefix = """start cmd.exe /C " """
            self.shell_suffix = """ & echo Press the any-key & pause " """

        else:
            msg = "Shell %s not found." % shell
            print(msg)
            raise SystemError(msg)

    def decorate_command(self, command):
        """Add shell pre- and suffix"""
        return self.shell_prefix + command + self.shell_suffix

    def get_suffix(self):
        """Return current shell suffix"""
        return self.shell_suffix

    def get_prefix(self):
        """Return current shell prefix"""
        return self.shell_prefix
