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
def main():
    """
    Main function to run the PDF OCR processing.
    """
    # Define the source and destination folders (update these paths as necessary).
    source_folder = "."
    destination_folder = "processedDocs"
    
  
    # Initialise the Mistal OCR client using the MistalAI Python library.
    ocr_client = MistralOcrClient()
    
    # Initialise and run the PDF OCR processor.
    processor = PdfOcrProcessor(source_folder, destination_folder, ocr_client)
    processor.process_pdfs()



