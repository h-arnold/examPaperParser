import json
import logging
from FileManager import FileManager

class PdfOcrProcessor:
    """
    Processes PDF files stored in the database using the MistralOcrClient.
    """
    def __init__(self, source_folder: str, destination_folder: str, ocr_client):
        """
        Initialise the PDF processor.

        Args:
            source_folder (str): Logical directory name for PDF files in the database.
            destination_folder (str): Logical directory name where OCR results will be saved.
            ocr_client (MistralOcrClient): An instance of the OCR client.
        """
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.ocr_client = ocr_client

    def process_pdfs(self):
        """
        Iterate through PDF files stored in the database (source folder), process them via OCR,
        and save the results as JSON files in the destination folder.
        """
        file_manager = FileManager()
        pdf_file_rows = file_manager.listDbFiles(self.source_folder)
        
        if not pdf_file_rows:
            print("No PDF files found in the source folder.")
            return
        
        for row in pdf_file_rows:
            try:
                # Extract the media file and filename from the row.
                pdf_media = row['file']
                filename = row['path'].split("/")[-1]
                
                print(f"Uploading file: {filename}")
                signed_url = self.ocr_client.upload_pdf(pdf_media, filename)
                print(f"File uploaded successfully. Signed URL: {signed_url}")
                
                print(f"Processing OCR for file: {filename}")
                ocr_result = self.ocr_client.ocr_pdf(signed_url)
                
                # Convert OCR result to a JSON string.
                json_content = json.dumps(ocr_result, indent=4)
                json_filename = filename.rsplit('.', 1)[0] + ".json"
                
                # Create a BlobMedia object for the JSON file.
                import anvil.BlobMedia
                json_media = anvil.BlobMedia("application/json", json_content.encode("utf-8"), name=json_filename)
                
                # Write the JSON file to the destination folder in the database.
                file_manager.writeFile(json_media, json_filename, self.destination_folder)
                print(f"OCR result saved to {self.destination_folder}/{json_filename}")
            except Exception as e:
                logging.error(f"Error processing {filename}: {e}")
