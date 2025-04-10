import os
import boto3
import fitz  # PyMuPDF
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Get S3 configs
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# Initialize boto3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=AWS_REGION
)


def upload_file_to_s3(file_obj, key: str) -> str:
    """
    Uploads a file-like object to S3 under the given key.
    """
    s3.upload_fileobj(file_obj, BUCKET_NAME, key)
    return key


def extract_text_from_pdf_s3(key: str) -> str:
    """
    Downloads the PDF from S3 and extracts text using PyMuPDF.
    """
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
    pdf_bytes = obj["Body"].read()

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)
    return text
