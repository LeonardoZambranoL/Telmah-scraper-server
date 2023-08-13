from dotenv import load_dotenv
import os

load_dotenv()
comm_encryption_key = os.getenv("COMM_ENCRYPTION_KEY").encode()
secret_key = os.getenv("SECRET_KEY")