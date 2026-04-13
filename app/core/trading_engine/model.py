import joblib
import os


def load_model(path=None):
    """
    Loads model from absolute path (works locally + Render)
    """

    # ✅ BASE DIR → points to /app
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    # ✅ Correct path (DO NOT repeat 'core')
    if path is None:
        path = os.path.join(BASE_DIR, "trading_engine", "models", "gold_model_v2.pkl")

    # ✅ Debug logs (VERY IMPORTANT in production)
    print(f"📦 Loading model from: {path}")
    print(f"📁 Exists: {os.path.exists(path)}")

    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Model not found: {path}")

    data = joblib.load(path)

    # ✅ Support both raw model and dict format
    if isinstance(data, dict):
        return data.get("model", data)

    return data