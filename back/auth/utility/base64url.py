import json
import base64


def encode_json(data: dict) -> str:

    raw = json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return encode_bytes(raw)


def encode_bytes(raw: bytes) -> str:
    encoded = base64.urlsafe_b64encode(raw).decode("utf-8")
    return encoded.rstrip("=")
