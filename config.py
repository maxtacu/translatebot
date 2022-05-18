import os

telegram = {
    "token":  os.getenv(
        "TOKEN", "telegramtokenvalue"
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
