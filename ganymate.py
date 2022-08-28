import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

"""

https://pygobject.readthedocs.io/en/latest/index.html

https://docs.gtk.org/gtk3/#BUILDER-UI

https://docs.gtk.org/gtk3/class.Builder.html

https://www.gtk.org/docs/getting-started/index

https://pygobject.readthedocs.io/en/latest/guide/testing.html

https://python-gtk-3-tutorial.readthedocs.io/en/latest/builder.html

https://python-gtk-3-tutorial.readthedocs.io/en/latest/layout.html#grid

https://python-gtk-3-tutorial.readthedocs.io/en/latest/textview.html

"""


# window = Gtk.Window(title="Hello World")
# window.show()
# window.connect("destroy", Gtk.main_quit)
# Gtk.main()


class AnyMateGtkGui:
    """Responsible for creating the GUI"""

    def __init__(self, anymate, filename):

        self.build(anymate, filename)

    def build(self, anymate, filename):
        builder = Gtk.Builder()
        builder.add_from_file("anymate_gui.xml")

        window = builder.get_object("anymategui")

        controlgrid = builder.get_object("controlgrid")
        commandgrid = builder.get_object("commandgrid")
        treeview = builder.get_object("treeview")
        textview = builder.get_object("textview")

        #        scrolledwindow = Gtk.ScrolledWindow()
        #        scrolledwindow.set_hexpand(True)
        #        scrolledwindow.set_vexpand(True)
        #        self.grid.attach(scrolledwindow, 0, 1, 3, 1)

        #        self.textview = Gtk.TextView()

        textbuffer = textview.get_buffer()
        textbuffer.set_text(
            "This is some text inside of a Gtk.TextView. "
            + "Select text and click one of the buttons 'bold', 'italic', "
            + "or 'underline' to modify the text accordingly."
        )
        # scrolledwindow.add(self.textview)

        #         self.tag_bold = self.textbuffer.create_tag("bold", weight=Pango.Weight.BOLD)
        #         self.tag_italic = self.textbuffer.create_tag("italic", style=Pango.Style.ITALIC)
        #         self.tag_underline = self.textbuffer.create_tag(
        #             "underline", underline=Pango.Underline.SINGLE
        #         )
        #        self.tag_found = self.textbuffer.create_tag("found", background="yellow")

        store = Gtk.TreeStore(str, str, float)

        treeiter = store.append(
            None, ["The Art of Computer Programming", "Donald E. Knuth", 25.46]
        )

        treeiter = store.append(
            None, ["The Art of Computer Programming", "Donald E. Knuth", 25.46]
        )

        treeiter = store.append(treeiter, ["Stuff", "That", 25.46])

        treeview.set_model(store)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Title", renderer, text=0, weight=1)
        treeview.append_column(column)

        button1 = Gtk.Button(label="Button 1")
        controlgrid.attach(button1, 0, 0, 1, 1)  # left top with height

        for i in range(10):

            label = Gtk.Label(label="Its")
            statuslabel = Gtk.Label(label="dead")
            button = Gtk.Button(label=f"Button {i}")
            commandgrid.attach(label, 0, i, 1, 1)  # left top with height
            commandgrid.attach(button, 1, i, 1, 1)  # left top with height
            commandgrid.attach(statuslabel, 2, i, 1, 1)  # left top with height

        controlgrid.attach(commandgrid, 0, 1, 1, 1)  # left top with height

        button3 = Gtk.Button(label="Button 3")
        controlgrid.attach(button3, 0, 2, 1, 1)  # left top with height

        window.show_all()

    def mainloop(self):
        Gtk.main()


if __name__ == "__main__":
    gui = AnyMateGtkGui(None, None)
    gui.mainloop()
