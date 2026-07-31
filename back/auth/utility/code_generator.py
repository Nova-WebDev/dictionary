import secrets
import string
from auth.core.interfaces.code_generator import ICodeGenerator


class CodeGenerator(ICodeGenerator):
    def __init__(self, length: int = 5):
        self.length = length
        self.alphabet = string.ascii_lowercase + string.digits

    async def generate(self) -> str:
        return ''.join(secrets.choice(self.alphabet) for _ in range(self.length))
