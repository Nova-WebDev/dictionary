from dataclasses import dataclass

@dataclass
class TokenHeader:
    alg: str
    typ: str
