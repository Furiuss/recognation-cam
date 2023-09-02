import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

numero_twilio = os.getenv("NUMERO_TWILIO")

meu_numero = os.getenv("MEU_NUMERO")

def enviar_mensagem():
    message = client.messages.create(body='⚠️ALERTA CRIMINOSO!',
                                     from_=numero_twilio,
                                     to=meu_numero,
                                     media_url="https://520e-189-63-26-130.ngrok.io/imagem")