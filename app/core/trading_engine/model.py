import joblib
import os


def load_model(path=None):
    """
    Loads model from correct absolute path (works locally + Render)
    """

    # ✅ Build absolute path safely
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    if path is None:
        path = os.path.join(BASE_DIR, "core", "trading_engine", "models", "gold_model_v2.pkl")

    # Debug (optional)
    print(f"📦 Loading model from: {path}")

    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Model not found: {path}")

    data = joblib.load(path)

    if isinstance(data, dict):
        return data.get("model", data)

    return data