import anvil.secrets
import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from MistralOcrClient import MistralOcrClient
from PdfOcrProcessor import PdfOcrProcessor

@anvil.server.callable
def testWriteFile():
  import FileManager
  fileManager = FileManager()

  files = fileManager.getFilesInADirectory("pdfsToProcess")
  print(files)

  fileManager.writeFile(files[0], "test.pdf", "pdfsToProcess")

  updatedFileList = files.fileManager.getFilesInADirectory("pdfsToProcess")
  print(updatedFileList)

@anvil.server.callable
def list_files_in_directory():
  import os
  # Get the path of my Data Files directory
  my_directory_path = data_files['pdfsToProcess']

  with os.scandir(my_directory_path) as directory:
    for file in directory:
      if not file.name.startswith('.') and file.is_file():
        print(file.name)

@anvil.server.callable
def main():
  
    """
    Main function to run the PDF OCR processing.
    """
    # Define the source and destination folders (update these paths as necessary).
    source_folder = "pdfsToProcess"
    destination_folder = "processedDocs"
    
  
    # Initialise the Mistal OCR client using the MistalAI Python library.
    ocr_client = MistralOcrClient()
    
    # Initialise and run the PDF OCR processor.
    processor = PdfOcrProcessor(source_folder, destination_folder, ocr_client)
    processor.process_pdfs()





