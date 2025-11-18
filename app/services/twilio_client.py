from twilio.rest import Client
from decouple import config

TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = config('TWILIO_WHATSAPP_NUMBER')

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp_message(to_number: str, body_text: str):
    try:
        message = twilio_client.messages.create(
            to=f"whatsapp:{to_number}",
            from_=TWILIO_WHATSAPP_NUMBER,
            body=body_text
        )
        print(f"Mensagem enviada com sucesso. SID: {message.sid}")
        return True
    except Exception as e:
        print(f"Erro ao enviar mensagem via Twilio: {e}")
        return False