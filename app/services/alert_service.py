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

            # Only send alerts for trades
            if signal in ["BUY", "SELL"]:
                message = (
                    f"{signal} SIGNAL\n"
                    f"Price: {result['price']}\n"
                    f"Entry: {result['entry']}\n"
                    f"SL: {result['sl']}\n"
                    f"TP: {result['tp']}"
                )

                # 1. WebSocket broadcast
                await manager.broadcast(result)

                # 2. WhatsApp (optional hardcoded for now)
                # Replace with DB users later
                await send_whatsapp(message, "+91XXXXXXXXXX")

            await asyncio.sleep(10)  # run every 10 sec

        except Exception as e:
            print("Alert loop error:", e)
            await asyncio.sleep(5)