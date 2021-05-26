import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class NoteView(Gtk.Window):

    def __init__(self, parent, note_text, created_at):
        Gtk.Window.__init__(self, title="My note")
        self.set_border_width(5)

        label_text = Gtk.Label(label=note_text, halign=Gtk.Align.START, valign=Gtk.Align.START)
        label_text.set_line_wrap(True)
        
        label_created_at = Gtk.Label(label=created_at, halign=Gtk.Align.START, valign=Gtk.Align.START)

        scroll_view = Gtk.ScrolledWindow()

        container = Gtk.Grid(column_spacing=10, row_spacing=10)
        container.attach(label_created_at, 1, 0, 1, 1)
        container.attach(label_text, 1, 1, 2, 1)

        scroll_view.add(container)
        self.add(scroll_view)
        self.set_default_size(500, 500)
        
        self.set_transient_for(parent)
        self.set_modal(True)