import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

"""
PyGObject
https://pygobject.readthedocs.io/en/latest/index.html

https://docs.gtk.org/gtk3/#BUILDER-UI

https://docs.gtk.org/gtk3/class.Builder.html

https://www.gtk.org/docs/getting-started/index

PyGObject API Reference
http://lazka.github.io/pgi-docs/
http://lazka.github.io/pgi-docs/#Gtk-3.0/hierarchy.html

https://pygobject.readthedocs.io/en/latest/guide/testing.html

The Python GTK+ 3 Tutorial
https://python-gtk-3-tutorial.readthedocs.io/en/latest/index.html
https://python-gtk-3-tutorial.readthedocs.io/en/latest/builder.html
https://python-gtk-3-tutorial.readthedocs.io/en/latest/layout.html#grid
https://python-gtk-3-tutorial.readthedocs.io/en/latest/self.textview.html

https://python-gtk-3-tutorial.readthedocs.io/en/latest/cellrenderers.html
->
store.append(treeiter, [option.name, f"That {k}", f"This {k}", Gtk.Button(label=f"But {k}")])



# pip install pygobject

"""


# window = Gtk.Window(title="Hello World")
# window.show()
# window.connect("destroy", Gtk.main_quit)
# Gtk.main()


class AnyMateGtkGui:
    """Responsible for creating the GUI"""

    def __init__(self, anymate, filename):

        self.textbuffer = None

        self.build(anymate, filename)
        self.hidden = False

    def on_click_hidebutton(self, button):
        if self.hidden:
            self.treeview.show()
            self.textview.show()
            self.alabel.show()
            self.hidden = False
            self.hidebutton.set_label("hide")
        else:
            self.treeview.hide()
            self.textview.hide()
            self.alabel.hide()
            self.hidden = True
            self.hidebutton.set_label("show")
            self.window.resize(1, 1)

    def on_click_run_button(self, button):
        print(f"Run Button {button}")
        print(f"Run Button {button.get_label()}")
        print(f"Run Button {button.get_name()}")
        k = int(button.get_name()[-2:])
        self.textbuffer.set_text(self.options[k].execute(None))

    def on_click_show_button(self, button):
        print(f"Show Button {button}")
        print(f"Show Button {button.get_label()}")
        print(f"Show Button {button.get_name()}")

        k = int(button.get_name()[-2:])
        self.textbuffer.set_text(self.options[k].get_command())

    def on_row_activated(self, view, path, column):
        print(f"row activated {view} {path} {column}")
        print(type(path))
        treeiter = self.store.get_iter(path)
        name = self.store.get_value(treeiter, 0)
        print("Name", name)
        value = self.store.get_value(treeiter, 1)
        print("Stuff", value)

        # hackery
        for option in self.options:
            if option.get_name() == name:
                self.textbuffer.set_text(option.get_command())

        #path = Gtk.TreePath([1, 4])
        #treeiter = self.store.get_iter(path)
        ## Get value at 2nd column
        #value = self.store.get_value(treeiter, 1)
        #print(value)



    def build(self, anymate, filename):

        self._anymate = anymate

        self.options = anymate.get_config_list()

        builder = Gtk.Builder()
        builder.add_from_file("anymate_gui.xml")

        self.window = builder.get_object("anymategui")

        controlgrid = builder.get_object("controlgrid")
        commandgrid = builder.get_object("commandgrid")
        self.treeview = builder.get_object("treeview")
        self.textview = builder.get_object("textview")
        self.scrolledwindow = builder.get_object("scrolledwindow")

        #        scrolledwindow = Gtk.ScrolledWindow()
        #        scrolledwindow.set_hexpand(True)
        #        scrolledwindow.set_vexpand(True)
        #        self.grid.attach(scrolledwindow, 0, 1, 3, 1)

        #        self.self.textview = Gtk.TextView()

        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text(
            "*"*80 + "\n"  + "*"*80 + "\n" 
        )
        # scrolledwindow.add(self.textview)

        #         self.tag_bold = self.textbuffer.create_tag("bold", weight=Pango.Weight.BOLD)
        #         self.tag_italic = self.textbuffer.create_tag("italic", style=Pango.Style.ITALIC)
        #         self.tag_underline = self.textbuffer.create_tag(
        #             "underline", underline=Pango.Underline.SINGLE
        #         )
        #        self.tag_found = self.textbuffer.create_tag("found", background="yellow")

        # Title, Path
        store = Gtk.TreeStore(str, str)
        self.store = store
        
        treeiter = store.append(
            None, ["Test title", "testpath"]
        )

        treeiter = store.append(None, ["Command", "This"])

        # treeiter = store.append(treeiter, ["Stuff", "That", 25.46])

        self.treeview.set_model(store)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Title", renderer, text=0, weight=1)
        self.treeview.append_column(column)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Path", renderer, text=1, weight=1)
        self.treeview.append_column(column)

        # renderer = Gtk.CellRendererText()
        # column = Gtk.TreeViewColumn("Where", renderer, text=2, weight=1)
        # self.treeview.append_column(column)

        # renderer = Gtk.CellRendererText()
        # column = Gtk.TreeViewColumn("Buttons", renderer, text=3, weight=1)
        # self.treeview.append_column(column)

        self.treeview.connect("row-activated", self.on_row_activated)

        attr = Pango.AttrList()
        # fg_color = Pango.AttrForeground(65535, 0, 0, 0, 6)
        # wtf = Pango.Alignment.RIGHT
        # attr.insert(wtf)
        # attr.insert(Pango.Underline.SINGLE)
        fg = Pango.attr_foreground_new(65535, 0, 0)
        attr.insert(fg)
        # left = Pango.pango_layout_set_alignment(Pango.Alignment.RIGHT)

        button1 = Gtk.Button(label="Button 1")

        self.alabel = Gtk.Label(label="Testlabel", attributes=attr)
        controlgrid.attach(self.alabel, 1, 0, 1, 1)  # left top with height

        layout = self.alabel.create_pango_layout()
        # print("Layout", layout)
        # layout.set_alignment(Pango.Alignment.RIGHT)
        # layout.set_text("Whee")
        # context = self.alabel.create_pango_context()
        # print("Context", context)
        self.alabel.set_xalign(0.1)

        controlgrid.attach(button1, 0, 0, 1, 1)  # left top with height

        # for i in range(10):
        #    label = Gtk.Label(label="Its")
        #    statuslabel = Gtk.Label(label="dead")
        #    button = Gtk.Button(label=f"Button {i}")
        #    commandgrid.attach(label, 0, i, 1, 1)  # left top with height
        #    commandgrid.attach(button, 1, i, 1, 1)  # left top with height
        #    commandgrid.attach(statuslabel, 2, i, 1, 1)  # left top with height

        self.hidebutton = builder.get_object("hidebutton")
        if self.hidebutton:
            self.hidebutton.connect("clicked", self.on_click_hidebutton)
        else:
            raise SystemError("Can't connect hidebutton")

        for k in range(len(self.options)):
            # generate an option field
            option = self.options[k]
            # self.generate_option(
            #    parent=self.mainframe, row=self.use_row, option=option, number=k
            # )
            # self.use_row += 1
            print(option)

            label = Gtk.Label(label=option.get_nick())
            label.set_xalign(0.1)
            # statuslabel = Gtk.Label(label=option.nick)
            runbutton = Gtk.Button(label="run", name=f"runbutton{k:3}")
            #showbutton = Gtk.Button(label="show", name=f"showbutton{k:3}")

            # not sure if the lambda really works here
            runbutton.connect("clicked", lambda x: self.on_click_run_button(x))
            #showbutton.connect("clicked", lambda x: self.on_click_show_button(x))

            commandgrid.attach(label, 0, k, 1, 1)  # left top with height
            commandgrid.attach(runbutton, 1, k, 1, 1)  # left top with height
            #commandgrid.attach(showbutton, 2, k, 1, 1)  # left top with height

            store.append(treeiter, [option.name, f"That {k}"])

        controlgrid.attach(commandgrid, 0, 1, 1, 1)  # left top with height

        button3 = Gtk.Button(label="Button 3")
        controlgrid.attach(button3, 0, 2, 1, 1)  # left top with height

        self.window.show_all()

    def mainloop(self):
        Gtk.main()
