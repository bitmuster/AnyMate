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
https://python-gtk-3-tutorial.readthedocs.io/en/latest/gallery.html
https://python-gtk-3-tutorial.readthedocs.io/en/latest/builder.html
https://python-gtk-3-tutorial.readthedocs.io/en/latest/layout.html#grid
https://python-gtk-3-tutorial.readthedocs.io/en/latest/self.textview.html

https://python-gtk-3-tutorial.readthedocs.io/en/latest/cellrenderers.html
->
store.append(treeiter, [option.name, f"That {k}", f"This {k}", Gtk.Button(label=f"But {k}")])

https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/TreeView.html#Gtk.TreeView


# pip install pygobject

"""


class AnyMateGtkGui:
    """Responsible for creating the GUI"""

    def __init__(self, anymate, filename):
        self.textbuffer = None

        self.build(anymate, filename)
        self.hidden = False

        self.active_option = None

    def on_click_hidebutton(self, button):
        if self.hidden:
            self.treeview.show()
            self.textview.show()
            self.alabel.show()
            self.hidden = False
            self.hidebutton.set_label("hide")
            self.controlbox_1.show()
            self.controlbox_2.show()
            self.treeview_container.show()
        else:
            self.treeview.hide()
            self.textview.hide()
            self.alabel.hide()
            self.hidden = True
            self.hidebutton.set_label("show")
            self.window.resize(1, 1)
            self.controlbox_1.hide()
            self.controlbox_2.hide()
            self.treeview_container.hide()

    def on_click_runbutton(self, button):
        # hackery
        for option in self.options:
            if option.get_name() == self.active_option:
                option.execute(None)

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
                self.active_option = name
                self.nameentry.set_text(name)
                break

    def build(self, anymate, filename):
        self._anymate = anymate

        self.options = anymate.get_config_list()

        builder = Gtk.Builder()
        builder.add_from_file("anymate_gui.xml")

        self.window = builder.get_object("anymategui")
        self.window.connect("destroy", Gtk.main_quit)

        controlgrid = builder.get_object("controlgrid")
        commandgrid = builder.get_object("commandgrid")
        self.treeview = builder.get_object("treeview")
        self.textview = builder.get_object("textview")
        self.scrolledwindow = builder.get_object("scrolledwindow")

        self.nameentry = builder.get_object("nameentry")
        self.filenameentry = builder.get_object("filenameentry")
        self.interpreterentry = builder.get_object("interpreterentry")

        self.runbutton = builder.get_object("runbutton")
        self.runbutton.connect("clicked", self.on_click_runbutton)

        self.statuslabel = builder.get_object("statuslabel")
        self.stopbutton = builder.get_object("stopbutton")
        self.pidlabel = builder.get_object("pidlabel")
        self.bookmark_checkbox = builder.get_object("bookmark_checkbox")

        self.scrolledwindow = builder.get_object("scrolledwindow")

        self.controlbox_1 = builder.get_object("controlbox_1")
        self.controlbox_2 = builder.get_object("controlbox_2")
        self.treeview_container = builder.get_object("treeview_container")

        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("*" * 80 + "\n" + "*" * 80 + "\n")

        # Title, Path
        store = Gtk.TreeStore(str, str)
        self.store = store

        treeiter = store.append(None, ["Test title", "testpath"])

        treeiter = store.append(None, ["Command", "This"])

        self.treeview.set_model(store)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Title", renderer, text=0, weight=1)
        self.treeview.append_column(column)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Nick", renderer, text=1, weight=1)
        self.treeview.append_column(column)

        self.treeview.connect("row-activated", self.on_row_activated)

        # Does not work right
        # self.treeview.expand_all()

        attr = Pango.AttrList()

        fg = Pango.attr_foreground_new(65535, 0, 0)
        attr.insert(fg)
        # left = Pango.pango_layout_set_alignment(Pango.Alignment.RIGHT)

        button1 = Gtk.Button(label="Button 1")

        self.alabel = Gtk.Label(label="Testlabel", attributes=attr)
        controlgrid.attach(self.alabel, 1, 0, 1, 1)  # left top with height

        layout = self.alabel.create_pango_layout()

        self.alabel.set_xalign(0.1)

        controlgrid.attach(button1, 0, 0, 1, 1)  # left top with height

        self.hidebutton = builder.get_object("hidebutton")
        if self.hidebutton:
            self.hidebutton.connect("clicked", self.on_click_hidebutton)
        else:
            raise SystemError("Can't connect hidebutton")

        for k in range(len(self.options)):
            # generate an option field
            option = self.options[k]

            print(option)

            label = Gtk.Label(label=option.get_nick())
            label.set_xalign(0.1)
            runbutton = Gtk.Button(label="run", name=f"runbutton{k:3}")

            # not sure if the lambda really works here
            runbutton.connect("clicked", lambda x: self.on_click_run_button(x))

            commandgrid.attach(label, 0, k, 1, 1)  # left top with height
            commandgrid.attach(runbutton, 1, k, 1, 1)  # left top with height

            store.append(treeiter, [option.name, option.nick])

        controlgrid.attach(commandgrid, 0, 1, 1, 1)  # left top with height

        button3 = Gtk.Button(label="Button 3")
        controlgrid.attach(button3, 0, 2, 1, 1)  # left top with height

        self.treeview.expand_all()

        self.window.show_all()

    def mainloop(self):
        Gtk.main()
