import os
from dotenv import load_dotenv

load_dotenv() 

telegram = {
    "token":  os.getenv(
        "TOKEN", "xxxxxxxxxxx"
    )
}

deepl = {
    "token": os.getenv("DEEPL_TOKEN", "xxxxxxxx")
}
