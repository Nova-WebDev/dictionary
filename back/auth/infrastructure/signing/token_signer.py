from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from auth.core.interfaces.token_signer import ITokenSigner

_DEFAULT_KEY_PATH = Path(__file__).resolve().parent.parent / "key" / "private_key.pem"


class TokenSigner(ITokenSigner):
    def __init__(self, private_key_path: Path = _DEFAULT_KEY_PATH):
        self.private_key = self._load_private_key(private_key_path)

    @staticmethod
    def _load_private_key(path: Path) -> Ed25519PrivateKey:
        with open(path, "rb") as f:
            key = serialization.load_pem_private_key(
                f.read(),
                password=None,
            )
        return key

    async def sign(self, unsigned: str) -> bytes:
        unsigned_bytes = unsigned.encode("utf-8")
        signature = self.private_key.sign(unsigned_bytes)
        return signature