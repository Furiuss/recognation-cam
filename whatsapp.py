import os
import time
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

numero_twilio = os.getenv("NUMERO_TWILIO")

meu_numero = os.getenv("MEU_NUMERO")

def enviar_mensagem(link):
    message = client.messages.create(body='⚠️ALERTA CRIMINOSO!',
                                     from_=numero_twilio,
                                     media_url=link,
                                     to=meu_numero)
    # time.sleep(60)
    print(message.sid)