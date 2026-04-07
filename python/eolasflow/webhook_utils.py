"""Webhook signature verification utilities."""

import hmac
import hashlib


def verify_signature(payload: bytes | str, signature: str, secret: str) -> bool:
    """
    Verify that a webhook payload was signed by EolasFlow.

    Use this in your webhook handler to reject forged requests.

    Args:
        payload: Raw request body (bytes or string)
        signature: Value of the X-Webhook-Signature header
        secret: Your webhook secret from the EolasFlow Dashboard

    Returns:
        True if the signature is valid

    Example:
        @app.post("/webhooks/eolasflow")
        async def handle_webhook(request: Request):
            body = await request.body()
            signature = request.headers.get("X-Webhook-Signature", "")

            if not eolasflow.verify_signature(body, signature, "your-webhook-secret"):
                raise HTTPException(status_code=403, detail="Invalid signature")

            payload = await request.json()
            # process webhook...
    """
    if isinstance(payload, str):
        payload = payload.encode("utf-8")

    expected = hmac.new(
        secret.encode("utf-8"),
        payload,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(signature, expected)
