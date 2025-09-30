import os
from fastapi import FastAPI
from twilio.rest import Client
from fastapi import Request


app = FastAPI()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
verify_sid = os.environ["TWILIO_VERIFY_SID"]

client = Client(account_sid, auth_token)

@app.post("/send-otp/")
async def send_otp(request: Request):
    body = await request.json()
    phone = body.get("phone")

    if not phone:
        raise HTTPException(status_code=400, detail="Phone number is required")

    verification = client.verify.v2.services(verify_sid).verifications.create(
        to=phone,
        channel="sms"
    )

    return {"status": verification.status}


@app.post("/verify-otp/")
async def verify_otp(request: Request):
    body = await request.json()
    phone = body.get("phone")
    code = body.get("code")

    if not phone or not code:
        return {"error": "Phone and code required"}

    try:
        verification_check = client.verify.v2.services(verify_sid) \
            .verification_checks \
            .create(to=phone, code=code)
        return {"status": verification_check.status}
    except Exception as e:
        return {"error": str(e)}
