import os
import anvil.secrets
import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media

class FileManager:

    def __init__(self):
        pass

    # ----------------------------
    # Data Files (read-only) Methods
    # ----------------------------
    def listDataFiles(self, directoryPath):
        """
        Lists files from Anvil's data_files service in the given directory.
        These files are read-only and bundled with your app.
        """
        directory = data_files[directoryPath]
        files = []
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_file() and not entry.name.startswith('.'):
                    files.append(entry)
        return files

    # ----------------------------
    # Database File Methods
    # ----------------------------
    def listDbFiles(self, directory):
        """
        Lists file rows stored in the app_tables.files table that belong to the given directory.
        The table is expected to have at least 'path' and 'file' columns.
        """
        files = []
        for row in app_tables.files.search():
            if row['path'].startswith(f"{directory}/"):
                files.append(row)
        return files

    def writeFile(self, file, filename, directory):
        """
        Writes a file to the app_tables.files table.
        - file: an Anvil Media object.
        - filename: the name for the file.
        - directory: a logical directory name (used as part of the file path).
        
        If a file with the same path exists, it will be updated.
        """
        path = f"{directory}/{filename}"
        row = app_tables.files.get(path=path)
        if row:
            row['file'] = file
        else:
            row = app_tables.files.add_row(path=path, file=file)
        return row

    def readFile(self, filename, directory):
        """
        Reads a file from the app_tables.files table.
        Returns the Anvil Media object if found, else raises a FileNotFoundError.
        """
        path = f"{directory}/{filename}"
        row = app_tables.files.get(path=path)
        if row:
            return row['file']
        else:
            raise FileNotFoundError(f"No file found at {path}")

    def deleteFile(self, filename, directory):
        """
        Deletes a file from the app_tables.files table.
        Returns True if the file was deleted, or False if the file did not exist.
        """
        path = f"{directory}/{filename}"
        row = app_tables.files.get(path=path)
        if row:
            row.delete()
            return True
        return False
