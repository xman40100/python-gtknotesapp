# Import the libraries
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from db import DB
from note import Note

class MainWindow(Gtk.Window):

    connection = DB()
    text_input = None
    note_list = None
    container = None

    # Main window constructor event, which initializaes everything inside
    # the window.
    def __init__(self):
        Gtk.Window.__init__(self, title="My Notes")
        self.set_border_width(5)
        self.connect("destroy", self.exit_window)
        self.add_elements()
        self.set_default_size(400, 400)

    # show the about dialog and add the default
    # action for quitting the dialog.
    def show_about(self, widget):
        # create about dialog and add the widgets.
        dialog = Gtk.Dialog(title="About - My Notes", transient_for=self, flags=0)
        dialog.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        dialog.set_default_size(200, 200)

        label = Gtk.Label(label="My Notes is a little application created in Python using the GTK GUI toolkit as practice with the Python scripting language.\nCreated by xman40100, see license on GitHub for additional details.", halign=Gtk.Align.START)
        label.set_justify(Gtk.Justification.LEFT)

        # get the content area of the dialog (Gtk.Box)
        content_area = dialog.get_content_area()
        content_area.pack_start(label, True, True, 0)

        # show dialog and destroy on response.
        dialog.show_all()
        dialog.run()
        dialog.destroy()

    # Method that gets the current notes stored.
    def get_notes(self):
        notes = self.get_db_notes()
        self.note_list = Gtk.Grid(column_spacing=10, row_spacing=10)
        self.note_list.set_column_homogeneous(True)
        self.note_list.set_hexpand(True)
        self.note_list.set_vexpand(True)
        note_quantity = len(notes)

        # table columns.
        columns = [
            "Note",
            "Added on",
            "Actions"
        ]

        # get the amount of columns and add them in the grid.
        col_amount = len(columns)
        for i in range(0, col_amount):
            label = Gtk.Label(label=columns[i])
            label.set_justify(Gtk.Justification.CENTER)
            self.note_list.attach(label, i, 0, 1, 1)

        # check if there are no notes available, if so, show the no notes registered
        # label.
        if (note_quantity == 0):
            label_no_items = Gtk.Label(label="No notes registered.")
            label.set_justify(Gtk.Justification.CENTER)
            self.note_list.attach(label_no_items, 0, 1, col_amount, 1)
            return self.note_list
        
        for i in range(0, note_quantity):
            item = notes[i]

            # get the first 15 chars of the string, and replacing the new line special char.
            note_text = item.get_text()
            note_text = note_text.replace("\n", " ")
            note_text = note_text[0:15] + "..."

            # add the labels and buttons
            label_text = Gtk.Label(label=note_text)
            label_text.set_justify(Gtk.Justification.CENTER)

            label_time = Gtk.Label(label=item.get_time_localtime())
            label_time.set_justify(Gtk.Justification.CENTER)

            # create the action buttons    
            action_grid = Gtk.Grid(column_spacing=10)
            action_grid.set_column_homogeneous(True)
            action_grid.set_hexpand(True)

            delete_button = Gtk.Button(label="Delete")
            delete_button.connect("clicked", self.delete_note, item.get_id())

            view_button = Gtk.Button(label="View")
            view_button.connect("clicked", self.view_note, item.get_id())

            action_grid.attach(view_button, 1, 0, 1, 1)
            action_grid.attach(delete_button, 2, 0, 1, 1)

            # attach to the note_list table.
            self.note_list.attach(label_text, 0, i + 1, 1, 1)
            self.note_list.attach(label_time, 1, i + 1, 1, 1)
            self.note_list.attach(action_grid, 2, i + 1, 1, 1)


        return self.note_list

    # This adds the elements into the GUI.
    def add_elements(self):
        # add scroll view
        scrollview = Gtk.ScrolledWindow()
        scrollview.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        # add the grid container.
        self.container = Gtk.Grid(column_spacing=10, row_spacing=10)

        # add button to add new note.
        button = Gtk.Button(label="Add note")
        button.connect("clicked", self.insert_note)
        self.container.attach(button, 1, 0, 1, 1)

        button2 = Gtk.Button(label="About")
        button2.connect("clicked", self.show_about)
        self.container.attach(button2, 12, 0, 1, 1)

        label = Gtk.Label(label="Type your new note:")
        label.set_justify(Gtk.Justification.LEFT)
        self.container.attach(label, 1, 1, 1, 1)

        # add an text_input for typing
        self.text_input = Gtk.TextView()
        self.text_input.set_hexpand(True)
        self.container.attach(self.text_input, 1, 2, 12, 3)

        # get the stored notes and add them into the GUI
        notes = self.get_notes()
        self.container.attach(notes, 1, 5, 12, 1)

        # add them to main GUI
        scrollview.add(self.container)
        self.add(scrollview)

    # Method that gets the current notes in the database
    def get_db_notes(self):
        connection = self.connection.get_instance()
        notes = Note.get_all(connection)
        return notes
    
    # exit window
    def exit_window(self, widget):
        self.connection.destroy_instance()
        Gtk.main_quit()

    # This method allows to insert a new note into the database.
    def insert_note(self, widget):
        # get the text and check if it's not empty.
        text_buffer = self.text_input.get_buffer()
        start, end = text_buffer.get_bounds()
        text = text_buffer.get_text(start, end, True)

        if len(text) == 0:
            return

        # insert on the database using the connection instance.
        inserted = Note.insert(self.connection.get_instance(), text)
        if not (inserted):
            self.create_error_dialog("An error has occured!", None, "An error has occured while trying to insert a new note.")
            return

        # reload the notes widget.
        self.container.remove_row(5)

        # get the notes and set text to null.
        notes = self.get_notes()
        self.container.attach(notes, 1, 5, 12, 1)
        text_buffer.set_text("")
        self.container.show_all()
    
    # This method allows to view a note.
    def view_note(self, widget, note_id):
        Note.view(self.connection.get_instance(), note_id, self)
    
    # This method allows to delete a note.
    def delete_note(self, widget, note_id):
        # confirmation message to check if the note is going to be deleted
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Confirm delete",
            title="Confirmation required",
            secondary_text="Are you sure you want to delete this note? This operation cannot be undone."
        )

        # run the dialog, taking control, then destroy it after it receives a response.
        response = dialog.run()
        dialog.destroy()
        if (response == Gtk.ResponseType.NO):
            return
        
        # check if the note was deleted.
        deleted = Note.delete(self.connection.get_instance(), note_id)
        if not (deleted):
            self.create_error_dialog("An error has occured!", None, "An error has occured while trying to delete the selected note.")
            return
        
        # reload the notes widget.
        self.container.remove_row(5)

        # get the notes and set text to null.
        notes = self.get_notes()
        self.container.attach(notes, 1, 5, 12, 1)
        self.container.show_all()
    
    # This method allows to create a quick error dialog.
    def create_error_dialog(self, dialog_title, dialog_subtitle, dialog_text):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=dialog_subtitle,
            title=dialog_title,
            secondary_text=dialog_text
        )
        dialog.run()
        dialog.destroy()
        
    
# instantiate new window, show it, and use the main GTk loop.
window = MainWindow()
window.show_all()
Gtk.main()
