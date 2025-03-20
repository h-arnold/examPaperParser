import anvil.secrets
import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import os
from pathlib import Path
import json
import logging
from MistralOcrClient import MistralOcrClient

class PdfOcrProcessor:
    """
    Processes PDF files from a source directory using the MistralOCRClient.
    """
    def __init__(self, source_folder: str, destination_folder: str, ocr_client: MistralOcrClient):
        """
        Initialise the PDF processor.

        Args:
            source_folder (str): Directory containing PDF files.
            destination_folder (str): Directory where OCR results will be saved.
            ocr_client (MistralOCRClient): An instance of the OCR client.
        """
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.ocr_client = ocr_client

        # Create the destination folder if it doesn't exist
        self.createDestinationFolder()

    def process_pdfs(self):
        """
        Iterate through PDF files in the source folder, upload them, process them via OCR,
        and save the results as JSON files in the destination folder.
        """
        pdf_files = os.listdir(self.source_folder) 
        
        if not pdf_files:
          print("No PDF files found in the source folder.")
          return
        
        for pdf_file in pdf_files:
            try:
                print(f"Uploading file: {pdf_file.name}")
                signed_url = self.ocr_client.upload_pdf(str(pdf_file))
                print(f"File uploaded successfully. Signed URL: {signed_url}")
                
                print(f"Processing OCR for file: {pdf_file.name}")
                ocr_result = self.ocr_client.ocr_pdf(signed_url)
                
                # Save the OCR result to the destination folder.
                output_file = self.destination_folder / (pdf_file.stem + ".json")
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(ocr_result, f, indent=4)
                print(f"OCR result saved to {output_file}")
            except Exception as e:
                logging.error(f"Error processing {pdf_file.name}: {e}")#

    def createDestinationFolder(self):
      directories = os.listdir("./")

      if self.destination_folder in directories:
        print("processedDocs folder already exists, skipping folder creation.")
      else:
        os.mkdir(f"./${self.destination_folder}")
        print("Created destination folder.")

    def checkForPdfsInFolder(self):
      pdfFiles = []
      files = os.listdir(f"{self.source_folder}")
      for file in files:
        if file.contains(".pdf"):
          pdfFiles.push(file)


    def list_files_in_directory():
      # Get the path of my Data Files directory
      my_directory_path = data_files['my_directory']

    with os.scandir(my_directory_path) as directory:
        for file in directory:
            if not file.name.startswith('.') and file.is_file():
                print(file.name)
