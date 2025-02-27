import os
from dotenv import load_dotenv
import traceback
import cloudinary.uploader
import uuid
import random
import string
from dataclasses import dataclass
import requests

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


def generate_otp() -> str:
    """Generates an otp for email verification"""
    uid = uuid.uuid4()
    uuid_hex = uid.hex  # convert to hex value
    otp = "".join(filter(str.isdigit, uuid_hex))[:6]
    return otp


def generate_ref() -> str:
    """generate unique reference code"""
    code = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return code.upper()


@dataclass
class FlutterSDK:
    """Flutter SDK class for making payments"""

    amount: str
    customer_email: str
    customer_name: str
    customer_phone: str
    secret_key: str = get_env("FLUTTER_SECRET_KEY", "")
    public_key: str = get_env("FLUTTER_PUBLIC_KEY", "")
    base_url: str = get_env("FLUTTER_BASE_URL", "")
    redirect_url: str = get_env("REDIRECT_URL", "")
    currency: str = "NGN"
    tx_ref: str = generate_ref()

    def generate_checkout_url(self):
        """Generate checkout url for flutterwave"""
        endpoint: str = f"{self.base_url}/payments"
        body = {
            "tx_ref": self.tx_ref,
            "amount": self.amount,
            "currency": self.currency,
            "redirect_url": self.redirect_url,
            "customer": {
                "email": self.customer_email,
                "phonenumber": str(self.customer_phone),
                "name": self.customer_name,
            },
            "payment_options": "card, ussd, opay, banktransfer, account, googlepay",
            "customizations": {
                "description": "Payment for services",
                "logo": "https://assets.piedpiper.com/logo.png",
            },
        }
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }

        # send the request
        response = requests.post(endpoint, json=body, headers=headers)
        resp = response.json()
        if response.status_code == 200:
            return resp["data"]["link"]
        else:
            raise Exception(resp.get("message", "An error occurred"))
