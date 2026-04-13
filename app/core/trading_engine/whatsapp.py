from twilio.rest import Client
from app.core.config import settings

client = Client(
    settings.TWILIO_ACCOUNT_SID,
    settings.TWILIO_AUTH_TOKEN
)


def send_whatsapp(message: str, to: str):
    try:
        msg = client.messages.create(
            body=message,
            from_=settings.TWILIO_WHATSAPP_FROM,
            to=f"whatsapp:{to}"
        )

        print("✅ Message sent:", msg.sid)

    except Exception as e:
        print("❌ WhatsApp error:", e)