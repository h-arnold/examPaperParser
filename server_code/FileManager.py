import anvil.secrets
import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import os
import anvil.media

class FileManager:

  def __init__(self):

    def getFilesInADirectory(directoryPath):
      directory = data_files[directoryPath]
      directoryFiles = []
      
      with os.scandir(directory) as directory:
        for file in directory:
            if not file.name.startswith('.') and file.is_file():
              directoryFiles.push(file)
      
      return directoryFiles

    def writeFile(file,filename, path):
      app_tables.Files.add_row(path=f"{path}/[filename]",
                                    file=file
                                    )
