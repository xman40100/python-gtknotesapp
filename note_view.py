import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class NoteView(Gtk.Dialog):

    def __init__(self, parent, note_text, created_at):
        Gtk.Dialog.__init__(self, title="My Note", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(400, 300)

        label_text = Gtk.Label(label=note_text, halign=Gtk.Align.START, valign=Gtk.Align.START)
        label_created_at = Gtk.Label(label=created_at, halign=Gtk.Align.START, valign=Gtk.Align.START)

        box = self.get_content_area()
        # box.set_homogeneous(True)
        box.pack_start(label_created_at, True, False, 0)
        box.pack_start(label_text, True, True, 0)

        self.show_all()
        self.run()
        self.destroy()

