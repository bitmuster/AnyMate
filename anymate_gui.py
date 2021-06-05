import os.path
import sys

import tkinter as tk
import tkinter.scrolledtext as tks
import tkinter.ttk as ttk


class AnyMateGui:
    """Responsible for creating the GUI"""

    def __init__(self, anymate, filename, debug=False):
        """Build the UI"""

        self.options = anymate.get_config_list()

        self.save_space = False

        self.buttons = []
        self.textfields = []
        self.options_hidden = False
        self.debug = debug

        self.build_rootwin(filename)
        self.build_option_menue()
        self.build_run_menue()
        self.build_terminal()

        self.rootwin.wait_visibility(self.mainframe)
        self.resize_canvas()

    def build_rootwin(self, filename):
        """Build the main window"""

        # Set up the GUI
        self.rootwin = tk.Tk(className="AnyMate: " + filename)

        # The alternatve wm_iconbitmap is buggy - will never work
        iconfile = os.path.join(sys.path[0], "icon.png")
        self.rootwin.iconphoto(True, tk.PhotoImage(file=iconfile))
        self.rootwin.resizable(width=False, height=True)
        self.rootwin.grid_rowconfigure(0, minsize=28)

        self.options_button = tk.Button(
            self.rootwin, text="Hide Options", command=self.hide_handler
        )
        self.options_button.grid(column=1, row=0, columnspan=2)

        if self.debug > 0:
            self.hidden_button = tk.Button(
                self.rootwin, text="", command=self.hidden_handler
            )
            self.hidden_button.grid(column=0, row=0)

        self.rootwin.rowconfigure(0, weight=0)
        self.rootwin.rowconfigure(1, weight=1)
        self.rootwin.columnconfigure(0, weight=1)
        self.rootwin.columnconfigure(1, weight=0)  # scrollbar
        self.rootwin.columnconfigure(2, weight=1)

    def build_option_menue(self):
        """Build the option menue on the left"""

        self.canvas = tk.Canvas(
            self.rootwin,
            # height=800,
            width=200,
            scrollregion=(0, 0, 100, 100),
            background="RED",
            borderwidth=5,
        )
        self.canvas.grid(column=0, row=1, sticky=tk.N + tk.S + tk.E + tk.W)

        def scroll_wheel(event):
            """The mouse scroll event handler"""
            if self.debug > 0:
                print("scroll_wheel %i" % event.num)
            if event.num == 4:
                self.canvas.yview("scroll", -1, "units")
            elif event.num == 5:
                self.canvas.yview("scroll", 1, "units")

        self.scrollbar = tk.Scrollbar(
            self.rootwin,
            orient=tk.VERTICAL,
            background="DARKGREEN",
            highlightcolor="GREEN",
        )

        self.scrollbar.grid(row=1, column=1, sticky="ns")
        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.scrollbar.bind("<Button-4>", scroll_wheel)
        self.scrollbar.bind("<Button-5>", scroll_wheel)
        # self.canvas.bind_all('<Button-4>', scroll_wheel)
        # self.canvas.bind_all('<Button-5>', scroll_wheel)
        # self.rootwin.bind_all('<Button-4>', scroll_wheel)
        # self.rootwin.bind_all('<Button-5>', scroll_wheel)

        self.mainframe = tk.Frame(self.canvas, background="BLUE")

        # paint the frame on to the canvas -> posibillity for global scrollbar
        # http://tkinter.unpythonic.net/wiki/ScrolledFrame
        self.canvas.create_window(0, 0, anchor="nw", window=self.mainframe)
        # use wait visibility later and resize the Canvas

        self.use_row = 1
        self.use_row += 1

        for k in range(len(self.options)):
            # generate an option field
            option = self.options[k]
            self.generate_option(
                parent=self.mainframe, row=self.use_row, option=option, number=k
            )
            self.use_row += 1

    def build_run_menue(self):
        """Build the run menue in the middle"""

        self.proccanvas = tk.Canvas(
            self.rootwin,
            # height=800,
            width=200,
            scrollregion=(0, 0, 100, 100),
            background="BLUE",
            # borderwidth=5
        )
        self.proccanvas.grid(column=2, row=1, sticky=tk.N + tk.S + tk.E + tk.W)
        self.runframe = tk.Frame(self.proccanvas, background="GREEN")

        def run_scroll_wheel(event):
            """The mouse scroll event handler"""
            if self.debug > 0:
                print("scroll_wheel %i" % event.num)
            if event.num == 4:
                self.proccanvas.yview("scroll", -1, "units")
            elif event.num == 5:
                self.proccanvas.yview("scroll", 1, "units")

        self.runscrollbar = tk.Scrollbar(
            self.rootwin,
            orient=tk.VERTICAL,
            background="DARKGREEN",
            highlightcolor="GREEN",
        )

        self.runscrollbar.bind("<Button-4>", run_scroll_wheel)
        self.runscrollbar.bind("<Button-5>", run_scroll_wheel)

        self.runscrollbar.grid(row=1, column=3, sticky="ns")
        self.proccanvas.config(yscrollcommand=self.runscrollbar.set)
        self.runscrollbar.config(command=self.proccanvas.yview)

        self.proccanvas.create_window(0, 0, anchor="nw", window=self.runframe)

        self.b1 = tk.Button(self.runframe, text="b1")
        self.b1.grid(column=0, row=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.b2 = tk.Button(self.runframe, text="b2")
        self.b2.grid(column=0, row=1, sticky=tk.N + tk.S + tk.E + tk.W)

    def build_terminal(self):
        """Build the terminal on the right"""

        # self.terminal = tks.ScrolledText(
        #    self.rootwin,
        #    #background="GREEN",
        #    borderwidth=5
        #    )

        # self.terminal.insert(tk.END, "thats it ...")
        # self.terminal.grid(
        #    column=2,
        #    row=1)

        self.book = tk.ttk.Notebook(self.rootwin)
        self.book.grid(column=4, row=1)

        self.terminal = tks.ScrolledText(
            self.book,
            # background="GREEN",
            borderwidth=5,
        )

        self.terminal.insert(tk.END, "thats it ...")
        # self.terminal.grid(
        #    column=0,
        #    row=0)
        self.book.add(self.terminal, text="test")

    def resize_canvas(self):
        """Set the canvas size equal to the size of the mainframe"""
        height = self.mainframe.winfo_height()
        width = self.mainframe.winfo_width()
        self.canvas.config(height=height, width=width)
        self.canvas.config(scrollregion=(0, 0, width, height))
        if self.debug > 0:
            print(("The canvas should have now %ix%i pixels" % (width, height)))
            print(
                (
                    "The rootwin has a size of %ix%i pixels"
                    % (self.rootwin.winfo_width(), self.rootwin.winfo_height())
                )
            )

    def hidden_handler(self):
        """Handler for hidden button (there in debug mode)
        """
        self.resize_canvas()

    def hide_handler(self):
        """Handler for hide button
        """
        if self.options_hidden:
            if self.debug > 0:
                print("Un-Hiding")
            for field in self.textfields:
                field.grid()
            self.resize_canvas()
            self.options_button.config(text="Hide Options")
            self.options_hidden = False
        else:
            if self.debug > 0:
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

    @staticmethod
    def quit():
        """Quit handler
        """
        print("exiting...")
        # killall clients
        sys.exit()

    def generate_option(self, parent, row, option, number):
        """Generates an option to click on
        """
        textfield_width = 80

        # self.button = tk.Button(
        #    parent,
        #    text=option.name + '\n' + option.nick,
        #    #command= option.execute,

        #    # unfortunately Tkinter does not allow arguments for the Button
        #    # so we generate a pseudo function for that
        #    command=lambda: self.execute_option(number),
        #    bg=option.color
        #    )
        # self.button.grid(column=2, row=row, rowspan=1, sticky=tk.W+tk.E+tk.N+tk.S)

        button = tk.Button(parent, text=option.name, bg=option.color, borderwidth=2)
        button.grid(column=0, row=row, rowspan=1, sticky=tk.W + tk.E + tk.N + tk.S)

        runbutton = tk.Button(
            parent, text="run", command=lambda: self.execute_option(number)
        )
        runbutton.grid(column=1, row=row, rowspan=1, sticky=tk.W + tk.E + tk.N + tk.S)

        printbutton = tk.Button(
            parent, text="print", command=lambda: self.print_option(number, option.text)
        )
        printbutton.grid(column=3, row=row, rowspan=1, sticky=tk.W + tk.E + tk.N + tk.S)

        label = tk.Label(parent, text="state")
        label.grid(column=2, row=row, rowspan=1, sticky=tk.W + tk.E + tk.N + tk.S)

        # self.buttons.append(self.button)

        height = option.text.count("\n")
        if height == 0:
            height = len(option.text) // textfield_width
        if not self.save_space:
            height += 1  # looks a bit nicer

        # self.textfield = tk.Text(parent,
        #        width=textfield_width, height=height)
        # self.textfield.insert(tk.END, option.text)
        # self.textfield.grid(
        #    column=4,
        #    columnspan=1,
        #    row=row,
        #    rowspan=1,
        #    sticky=tk.W+tk.E
        #    )
        # self.textfields.append(self.textfield)

    def print_option(self, number, text):
        """Handler for an option - button"""
        if self.debug > 0:
            print("Executing %i" % number)
        print(text)
        self.terminal.insert(tk.END, text)

        # self.options[number].execute()

    def execute_option(self, number):
        """Handler for an option - button"""
        if self.debug > 0:
            print("Executing %i" % number)
        self.options[number].execute()
        # self.terminal.insert(tk.END, text)
