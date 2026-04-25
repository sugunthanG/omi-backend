from fastapi import APIRouter, Query
from app.services.trading_service import run_trading_cycle

router = APIRouter()


# =========================
# TEST ENDPOINT
# =========================
@router.get("/test")
def test():
    return {"message": "Trading API working"}


# =========================
# GET SIGNAL
# =========================
@router.get("/signal")
def get_signal():
    try:
        result = run_trading_cycle()
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# =========================
# RUN WITH OPTIONS
# =========================
@router.post("/run")
def run_trading(
    whatsapp: bool = Query(False),
    phone: str = Query(None)
):
    try:
        result = run_trading_cycle(
            whatsapp=whatsapp,
            phone=phone
        )

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }