# =========================================
# SIGNAL GENERATION (FINAL CLEAN VERSION)
# =========================================

FEATURES = [
    'ema20','ema50','rsi','atr',
    'momentum','trend_up','trend_down',
    'break_up','break_down'
]

CONF_THRESHOLD = 0.55   # 🔥 lower threshold


def generate_signal(model, df):
    try:
        latest = df[FEATURES].iloc[-1:].copy()

        probs = model.predict_proba(latest)[0]

        sell_prob = float(probs[0])
        hold_prob = float(probs[1])
        buy_prob = float(probs[2])

        # ✅ Directional confidence (0–1 scale)
        directional_conf = max(sell_prob, buy_prob)

        entry = float(df["Close"].iloc[-1])
        atr = float(df["atr"].iloc[-1])

        break_up = int(df["break_up"].iloc[-1])
        break_down = int(df["break_down"].iloc[-1])

        signal = "NO TRADE"

        # ================= BUY =================
        if buy_prob > sell_prob and directional_conf > CONF_THRESHOLD:
            signal = "BUY"

            # 🚀 breakout boost
            if break_up == 1:
                directional_conf += 0.05

        # ================= SELL =================
        elif sell_prob > buy_prob and directional_conf > CONF_THRESHOLD:
            signal = "SELL"

            if break_down == 1:
                directional_conf += 0.05

        # ✅ clamp (avoid >1 after boost)
        directional_conf = min(directional_conf, 1.0)

        # ✅ ROUND HERE (IMPORTANT)
        directional_conf = round(directional_conf, 4)

        return signal, directional_conf, entry, atr

    except Exception as e:
        print(f"Signal Error: {e}")
        return "NO TRADE", 0.0, None, None