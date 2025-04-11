import os
from azure.storage.blob import BlobServiceClient
import fitz  # PyMuPDF
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure configs
AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")

# Initialize blob service client
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

def upload_file_to_blob(file_obj, blob_name: str) -> str:
    """
    Uploads a file-like object to Azure Blob Storage.
    """
    try:
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(file_obj, overwrite=True)
        return blob_name
    except Exception as e:
        raise Exception(f"Azure upload failed: {str(e)}")

def extract_text_from_blob(blob_name: str) -> str:
    """
    Downloads PDF from Azure Blob and extracts text using PyMuPDF.
    """
    try:
        blob_client = container_client.get_blob_client(blob_name)
        download_stream = blob_client.download_blob()
        pdf_bytes = download_stream.readall()

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "\n".join(page.get_text() for page in doc)
        return text
    except Exception as e:
        raise Exception(f"Azure PDF extraction failed: {str(e)}")
