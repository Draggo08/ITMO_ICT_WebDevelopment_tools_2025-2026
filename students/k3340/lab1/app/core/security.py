import base64
import hashlib
import hmac
import json
import os
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from app.core.config import settings


def hash_password(password: str, salt: str | None = None) -> str:
    password_salt = salt or os.urandom(16).hex()
    password_hash = hashlib.sha256(f"{password}{password_salt}".encode("utf-8")).hexdigest()
    return f"{password_salt}${password_hash}"


def verify_password(password: str, stored_value: str) -> bool:
    salt, password_hash = stored_value.split("$")
    calculated_hash = hashlib.sha256(f"{password}{salt}".encode("utf-8")).hexdigest()
    return hmac.compare_digest(calculated_hash, password_hash)


def _encode_payload(payload: dict) -> str:
    return base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).decode().rstrip("=")


def _decode_payload(payload: str) -> dict:
    padding = "=" * (-len(payload) % 4)
    return json.loads(base64.urlsafe_b64decode(f"{payload}{padding}").decode("utf-8"))


def create_access_token(user_id: int) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    exp_time = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": str(user_id), "exp": int(exp_time.timestamp())}

    encoded_header = _encode_payload(header)
    encoded_payload = _encode_payload(payload)
    signature_data = f"{encoded_header}.{encoded_payload}".encode("utf-8")
    signature = hmac.new(settings.jwt_secret_key.encode("utf-8"), signature_data, hashlib.sha256).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).decode().rstrip("=")

    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"


def decode_access_token(token: str) -> int:
    try:
        encoded_header, encoded_payload, encoded_signature = token.split(".")
        signature_data = f"{encoded_header}.{encoded_payload}".encode("utf-8")
        expected_signature = hmac.new(settings.jwt_secret_key.encode("utf-8"), signature_data, hashlib.sha256).digest()
        expected_signature_encoded = base64.urlsafe_b64encode(expected_signature).decode().rstrip("=")

        if not hmac.compare_digest(encoded_signature, expected_signature_encoded):
            raise ValueError("Invalid signature")

        payload = _decode_payload(encoded_payload)
        if int(payload["exp"]) < int(datetime.now(timezone.utc).timestamp()):
            raise ValueError("Token expired")

        return int(payload["sub"])
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from error
