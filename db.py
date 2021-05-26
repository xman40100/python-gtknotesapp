import sqlite3

class DB:
    
    db_instance = None
    def __init__(self):
        try:
            # make the connection and create a cursor for checking if tables exists.
            self.db_instance = sqlite3.connect("mynotes.db")
            cursor = self.db_instance.cursor()
            print("Database connection established!")
            print("Checking existing tables...")

            # check if table exists, fetch results and run migrations if table doesn't exist.
            cursor.execute("SELECT name FROM sqlite_master WHERE name IN ('notes')")
            records = cursor.fetchall()
            if (len(records) == 1):
                print("Table exists.")
            else:
                print("Table doesn't exists. Running migrations.")
                self.run_migrations()
            # close the cursor
            print("Done.")
            cursor.close()
        except sqlite3.Error as error:
            print("Error connecting to database: ", error)
    
    # This method returns the current instance of the connection to the database.
    def get_instance(self):
        return self.db_instance
        
    # This method destroy the instance of the current connection to the database.
    def destroy_instance(self):
        print("Destroying connection instance.")
        if not (self.db_instance is None):
            print("Destroyed.")
            self.db_instance.close()
            return True
        return False

    # This method runs the migrations for the database.
    def run_migrations(self):
        try:
            print("Creating notes table.")
            cursor = self.db_instance.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS notes (ID INTEGER PRIMARY KEY AUTOINCREMENT, text VARCHAR(2000), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            self.db_instance.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Error running migration: ", error)
            return False
        return True