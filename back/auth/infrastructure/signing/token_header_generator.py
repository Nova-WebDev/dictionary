from auth.core.entities.token_header import TokenHeader
from auth.core.interfaces.token_header_generator import ITokenHeaderGenerator


class TokenHeaderGenerator(ITokenHeaderGenerator):
    async def generate_header(self) -> TokenHeader:
        return TokenHeader(
            alg="EdDSA",
            typ="JWT"
        )
