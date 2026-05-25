import os
from dotenv import load_dotenv
from gigachat import GigaChat

load_dotenv()

with GigaChat(credentials=os.getenv("GIGACHAT_CREDENTIALS"), verify_ssl_certs=False) as giga:
    response = giga.chat("Привет! Ты работаешь?")
    print(response.choices[0].message.content)