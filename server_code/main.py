import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from MistralOcrClient import MistralOcrClient
from PdfOcrProcessor import PDFOcrProcessor

def main():
    """
    Main function to run the PDF OCR processing.
    """
    # Define the source and destination folders (update these paths as necessary).
    source_folder = "/"
    destination_folder = "/processedFolders"
    
    # Retrieve the Mistal API key from the environment.
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        raise EnvironmentError("MISTRAL_API_KEY environment variable not set.")
    
    # Initialise the Mistal OCR client using the MistalAI Python library.
    ocr_client = MistralOcrClient(api_key=api_key)
    
    # Initialise and run the PDF OCR processor.
    processor = PDFOCRProcessor(source_folder, destination_folder, ocr_client)
    processor.process_pdfs()

if __name__ == "__main__":
    main()

