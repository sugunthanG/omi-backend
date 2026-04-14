import joblib
import os


def get_project_root():
    """
    Returns project root directory (omi-backend)
    Works locally and in production (Render)
    """
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../")
    )


def load_model(path=None):
    """
    Load ML model safely
    """

    BASE_DIR = get_project_root()

    # ✅ Default model path
    if path is None:
        path = os.path.join(BASE_DIR, "models", "gold_model_v2.pkl")

    # ✅ Debug logs (keep for now)
    print("\n========== MODEL DEBUG ==========")
    print(f"PROJECT ROOT: {BASE_DIR}")
    print(f"MODEL PATH: {path}")
    print(f"FILE EXISTS: {os.path.exists(path)}")
    print("================================\n")

    # ❌ If not found → fail clearly
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Model not found at: {path}")

    # ✅ Load model
    data = joblib.load(path)

    # ✅ Support dict or direct model
    if isinstance(data, dict):
        return data.get("model", data)

    return data