from db import DB
from note_view import NoteView
from datetime import datetime, timezone

class Note:

    id = None
    text = None
    created_at = None
    MAX_LENGTH = 2000

    def __init__(self, id, text, created_at):
        self.id = id
        self.text = text
        self.created_at = created_at

    # This method returns all the notes registered in the database as a
    # set of Note objects.
    @staticmethod
    def get_all(db_instance):
        # get cursor from db instance and execute query.
        records = []
        cursor = db_instance.cursor()
        try:
            # exectue the query and get the results
            cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
            result_set = cursor.fetchall()
            # return as note collection.
            for idx, row in enumerate(result_set):
                note = Note(row[0], row[1], row[2])
                records.insert(idx, note)
        except sqlite3.Error as error:
            print("An error has occured: ", error)
        finally:
            # close the cursor and return the records.
            cursor.close()
            return records

    # This method creates a new note in the database.
    @staticmethod
    def insert(db_instance, text):
        # get cursor and insert in DB.
        cursor = db_instance.cursor()
        try:
            cursor.execute("INSERT INTO notes (text) VALUES (?)", (text,))
            db_instance.commit()
            cursor.close()
            return True
        except sqlite3.Error as error:
            cursor.close()
            print("An error has occured: ", error)
            return False

    # This method deletes a note from the database.
    @staticmethod
    def delete(db_instance, note_id):
        # get cursor and delete.
        cursor = db_instance.cursor()
        try:
            cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            db_instance.commit()
            cursor.close()
            return True
        except sqlite3.Error as error:
            cursor.close()
            print("An error has occured: ", error)
            return False

    # This method allows to show the note completely in a dialog.
    @staticmethod
    def view(db_instance, note_id, parent):
        # get cursor.
        cursor = db_instance.cursor()
        try:
            # get note
            cursor.execute("SELECT text, created_at FROM notes WHERE id = ?", (note_id,))

            # get info and close cursor.
            note = cursor.fetchone()
            cursor.close()

            note_text = note[0]
            # get the current time, on the database, it's saved as a UTC timestamp.
            created_timestamp = datetime.strptime(note[1], "%Y-%m-%d %H:%M:%S")

            # so we have to convert it to a localtime timestamp, and return it as a normal string.
            note_created_at = created_timestamp.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%Y-%m-%d %H:%M:%S")

            note_view = NoteView(parent, note_text, note_created_at)
            note_view.show_all()
            # note_view.connect("destroy", note_view.destroy)
        except sqlite3.Error as error:
            print("An error has occured: ", error)
            parent.create_error_dialog("An error has occured!", None, "An error has occured while trying to view the selected note.")
        finally:
            cursor.close()

    # This method returns the text of the current note.
    def get_text(self):
        return self.text
    
    # This method returns the note's ID.
    def get_id(self):
        return self.id

    # This method returns the timestamp when the note was created.
    def get_time(self):
        return self.created_at

    def get_time_localtime(self):
        # get the current time, on the database, it's saved as a UTC timestamp.
        created_timestamp = datetime.strptime(self.created_at, "%Y-%m-%d %H:%M:%S")

        # so we have to convert it to a localtime timestamp, and return it as a normal string.
        return created_timestamp.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime("%Y-%m-%d %H:%M:%S")