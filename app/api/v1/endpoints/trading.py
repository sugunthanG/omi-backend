from fastapi import APIRouter, Query
from app.core.trading_engine.data import fetch_data_with_timeout
from app.core.trading_engine.features import create_features
from app.core.trading_engine.signals import generate_signal, FEATURES
from app.core.trading_engine.model import load_model
from app.core.trading_engine.trade_tracker import update_trades
from app.core.trading_engine.whatsapp import send_whatsapp

import os

router = APIRouter()

MODEL_PATH = "models/gold_model_v2.pkl"

# In-memory state (temporary; later move to Redis/DB)
active_trades = []
signal_history = []


# =========================
# CORE TRADING FUNCTION
# =========================
def run_trading_cycle(whatsapp=False, phone=None):
    global active_trades, signal_history

    if not os.path.exists(MODEL_PATH):
        raise Exception("Model not found")

    model = load_model(MODEL_PATH)

    df = fetch_data_with_timeout()

    if df is None or df.empty:
        raise Exception("No data available")

    df = create_features(df)

    for f in FEATURES:
        if f not in df.columns:
            df[f] = 0

    df = df.dropna()

    signal, prob, entry, atr = generate_signal(model, df)

    if prob < 0.65:
        signal = "NO TRADE"

    price = float(df["Close"].iloc[-1])

    if signal == "BUY":
        sl = entry - atr * 1.5
        tp = entry + atr * 3
    elif signal == "SELL":
        sl = entry + atr * 1.5
        tp = entry - atr * 3
    else:
        sl, tp = None, None

    # WhatsApp Alert
    if whatsapp and signal in ["BUY", "SELL"] and phone:
        msg = f"{signal} | Entry:{entry} | SL:{sl} | TP:{tp}"
        send_whatsapp(msg, phone)

    active_trades = update_trades(active_trades, df)

    signal_history.append({
        "signal": signal,
        "price": price
    })

    return {
        "price": price,
        "signal": signal,
        "confidence": prob,
        "entry": entry,
        "sl": sl,
        "tp": tp,
        "active_trades": active_trades[-5:],
        "signal_history": signal_history[-10:]
    }


# =========================
# API ENDPOINTS
# =========================

@router.get("/test")
def test():
    return {"message": "Trading API working"}


@router.get("/signal")
def get_signal():
    try:
        result = run_trading_cycle()
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/run")
def run_trading(
    whatsapp: bool = Query(False),
    phone: str = Query(None)
):
    try:
        result = run_trading_cycle(whatsapp=whatsapp, phone=phone)
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}