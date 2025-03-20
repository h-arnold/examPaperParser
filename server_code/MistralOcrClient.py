import io
import anvil.secrets
from mistralai import Mistral

class MistralOcrClient:
    """
    A client for interacting with the Mistral OCR API using the MistralAI Python library.
    """
    def __init__(self, model: str = "mistral-ocr-latest"):
        """
        Initialise the OCR client.

        Args:
            model (str): The OCR model to use. Default is 'mistral-ocr-latest'.
        """
        self.apikey = self.getMistralApiKey()
        self.client = Mistral(api_key=self.apikey)
        self.model = model

    def upload_pdf(self, file_media, filename: str = None) -> str:
        """
        Upload a PDF file (as an Anvil Media object) to the Mistral API for OCR processing.

        Args:
            file_media: An Anvil Media object representing the PDF file.
            filename (str): The name of the file. If None, a default name is used.

        Returns:
            str: The signed URL for the uploaded PDF.
        """
        if filename is None:
            filename = "document.pdf"
        
        # Retrieve the bytes from the media object.
        if hasattr(file_media, "get_bytes"):
            file_bytes = file_media.get_bytes()
        else:
            file_bytes = file_media

        # Create a file-like object from the bytes.
        file_obj = io.BytesIO(file_bytes)

        response = self.client.files.upload(
            file={
                "file_name": filename,
                "content": file_obj,
            },
            purpose="ocr"
        )
        
        signed_url = response.get("url") if isinstance(response, dict) else getattr(response, "url", None)
        if not signed_url:
            raise ValueError("Upload did not return a signed URL.")
        return signed_url

    def ocr_pdf(self, signed_url: str, include_image_base64: bool = True) -> dict:
        """
        Perform OCR on a PDF document using its signed URL.

        Args:
            signed_url (str): The signed URL of the uploaded PDF.
            include_image_base64 (bool): Whether to include base64 image data in the response.

        Returns:
            dict: The OCR result as a JSON/dictionary.
        """
        return self.client.ocr.process(
            model=self.model,
            document={
                "type": "document_url",
                "document_url": signed_url,
            },
            include_image_base64=include_image_base64
        )

    def getMistralApiKey(self) -> str:
        """
        Retrieves the Mistral API Key from Anvil Secrets.
        """
        mistralApiKey = anvil.secrets.get_secret('mistralApiKey')
        if not mistralApiKey:
            raise Exception("No Mistral API Key provided. Please add one to your Anvil secrets and set the key as 'mistralApiKey'")
        return mistralApiKey
