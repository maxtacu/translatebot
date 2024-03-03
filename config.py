import os
from dotenv import load_dotenv

load_dotenv() 

telegram = {
    "token":  os.getenv(
        "TOKEN", "xxxxxxxxxxx"
    ),
    "deepl_api_key": os.getenv(
        "DEEPL_API_KEY", "xxxxxxxxxxx"
    )
}

google = {
    "service_urls": [
        'translate.google.com',
        'translate.google.es',
        'translate.google.pt',
        'translate.google.de',
        'translate.google.fr',
        'translate.google.ua',
        'translate.google.md',
        'translate.google.ru',
        'translate.google.ro'
    ]
}
