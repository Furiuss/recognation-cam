import os
import time
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

numero_twilio = os.getenv("NUMERO_TWILIO")

meu_numero = os.getenv("MEU_NUMERO")

def enviar_mensagem(foragido, link):
    body =  f"*Informações do Foragido*\n"  \
           f"📌 nome: {foragido['nome']}\n" \
           f"📌 cpf: {foragido['cpf']}\n" \
           f"📅 data_nascimento: {foragido['data_nascimento']}"

    message = client.messages.create(body=body,
                                     from_=numero_twilio,
                                     media_url=link,
                                     to=meu_numero)
    print(message.sid)