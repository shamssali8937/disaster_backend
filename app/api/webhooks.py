import os
import stripe
from fastapi import APIRouter, Request, HTTPException
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/webhooks", tags=["Payments"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@router.post("/stripe")
async def stripe_webhook(request: Request):

    payload = await request.body()
    sig = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig,
            os.getenv("STRIPE_WEBHOOK_SECRET")
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"status": "success"}