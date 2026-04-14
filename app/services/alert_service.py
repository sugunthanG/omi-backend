import asyncio
import json
from app.services.trading_service import run_trading_cycle
from app.core.websocket.manager import manager
from app.core.config import settings
from app.api.v1.endpoints.websocket import clients


from twilio.rest import Client


# Twilio client
client = Client(
    settings.TWILIO_ACCOUNT_SID,
    settings.TWILIO_AUTH_TOKEN
)


async def send_whatsapp(message: str, to: str):
    client.messages.create(
        body=message,
        from_=settings.TWILIO_WHATSAPP_FROM,
        to=f"whatsapp:{to}"
    )


# Background loop
async def alert_loop():
    while True:
        try:
            result = run_trading_cycle()

            signal = result["signal"]

            # ✅ ALWAYS SEND DATA (important)
            await manager.broadcast(result)

            # ✅ ONLY send WhatsApp for trades
            if signal in ["BUY", "SELL"]:
                message = (
                    f"{signal} SIGNAL\n"
                    f"Price: {result['price']}\n"
                    f"Entry: {result['entry']}\n"
                    f"SL: {result['sl']}\n"
                    f"TP: {result['tp']}"
                )

                await send_whatsapp(message, "+91XXXXXXXXXX")

            await asyncio.sleep(10)

        except Exception as e:
            print("Alert loop error:", e)
            await asyncio.sleep(5)