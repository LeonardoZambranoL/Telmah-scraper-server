from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

authdb_path = os.getenv("AUTHDB_PATH")
authdb_engine = create_engine(f'sqlite:///{authdb_path}')
db_encryption_key = os.getenv("DB_ENCRYPTION_KEY").encode()