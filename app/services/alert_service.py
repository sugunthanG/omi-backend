import asyncio
from app.services.trading_service import run_trading_cycle
from app.core.websocket.manager import manager
from app.core.config import settings

from twilio.rest import Client


# =========================
# TWILIO SETUP
# =========================
client = Client(
    settings.TWILIO_ACCOUNT_SID,
    settings.TWILIO_AUTH_TOKEN
)


# =========================
# SEND WHATSAPP
# =========================
async def send_whatsapp(message: str, to: str):
    try:
        client.messages.create(
            body=message,
            from_=settings.TWILIO_WHATSAPP_FROM,
            to=f"whatsapp:{to}"
        )
        print("✅ WhatsApp sent")
    except Exception as e:
        print("❌ WhatsApp error:", e)


# =========================
# ALERT LOOP (REAL-TIME ENGINE)
# =========================
async def alert_loop():
    print("🚀 ALERT LOOP STARTED")  # ✅ confirm loop started

    while True:
        try:
            print("⏳ Running trading cycle...")

            # =========================
            # RUN STRATEGY
            # =========================
            result = run_trading_cycle()

            if not result:
                print("⚠️ No result returned")
                await asyncio.sleep(5)
                continue

            signal = result.get("signal", "NO DATA")

            print("📊 RESULT:", result)

            # =========================
            # 🔥 ALWAYS SEND TO FRONTEND
            # =========================
            if len(manager.active_connections) > 0:
                await manager.broadcast(result)
                print(f"📡 Sent to {len(manager.active_connections)} client(s)")
            else:
                print("⚠️ No WebSocket clients connected")

            # =========================
            # 🔥 WHATSAPP ONLY FOR TRADES
            # =========================
            if signal in ["BUY", "SELL"]:
                message = (
                    f"{signal} SIGNAL\n"
                    f"Price: {result['price']}\n"
                    f"Entry: {result['entry']}\n"
                    f"SL: {result['sl']}\n"
                    f"TP: {result['tp']}"
                )

                await send_whatsapp(message, "+91XXXXXXXXXX")

            # =========================
            # LOOP INTERVAL
            # =========================
            await asyncio.sleep(10)

        except Exception as e:
            print("❌ Alert loop error:", e)
            await asyncio.sleep(5)