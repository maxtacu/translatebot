import os
from dotenv import load_dotenv

load_dotenv()

telegram = {"token": os.getenv("TOKEN", "xxxxxxxxxxx"), "admin": os.getenv("ADMIN_ID", "")}

deepl = {"token": os.getenv("DEEPL_TOKEN", "xxxxxxxx")}
