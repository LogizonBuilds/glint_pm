import os
from dotenv import load_dotenv
import traceback

load_dotenv()


def get_env(key: str, fallback: str) -> str:
    """get environment variable value from .env

    Args:
        key (str): variable key
        fallback (str): fallback value if none

    Returns:
        str: value of environment variable
    """
    return os.getenv(key, fallback)


import cloudinary.uploader


def upload_to_cloudinary(file, folder=None):
    """
    Uploads a file to Cloudinary and returns the URL.

    Args:
        file (file): The file to be uploaded.
        folder (str, optional): The folder in Cloudinary to upload the file. Defaults to None.

    Returns:
        str: The URL of the uploaded file.

    Raises:
        Exception: If the upload fails.
    """
    try:
        response = cloudinary.uploader.upload(file, folder=folder, resource_type="auto")
        return response.get("secure_url")
    except Exception as e:
        traceback.print_exc()
        raise Exception(f"Cloudinary upload failed: {str(e)}")
