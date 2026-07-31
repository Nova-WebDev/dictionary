import time
from dataclasses import asdict

from auth.core.entities.refresh_token import RefreshToken
from auth.core.errors.errors import TokenGenerationError
from auth.core.interfaces.token_header_generator import ITokenHeaderGenerator
from auth.core.interfaces.token_payload_generator import ITokenPayloadGenerator
from auth.core.interfaces.token_signer import ITokenSigner
from auth.utility.base64url import encode_json, encode_bytes


class GenerateAccessToken:
    def __init__(
        self,
        header_generator: ITokenHeaderGenerator,
        payload_generator: ITokenPayloadGenerator,
        signer: ITokenSigner
    ):
        self.header_generator = header_generator
        self.payload_generator = payload_generator
        self.signer = signer

    async def execute(self, refresh_token: RefreshToken) -> str:
        now = int(time.time())

        header = await self.header_generator.generate_header()

        payload = await self.payload_generator.generate_payload({
            "email": refresh_token.email,
            "role": refresh_token.role,
            "public_id": refresh_token.public_id,
            "iat": now
        })

        header_b64 = encode_json(asdict(header))
        payload_b64 = encode_json(asdict(payload))
        unsigned = f"{header_b64}.{payload_b64}"

        try:
            signature = await self.signer.sign(unsigned)
        except Exception as exc:
            raise TokenGenerationError() from exc

        signature_b64 = encode_bytes(signature)

        return f"{unsigned}.{signature_b64}"