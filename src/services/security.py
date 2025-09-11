from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings


class TokenCipher:

    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.fernet = Fernet(self.secret_key)

    def encrypt(self, plaintext: str | bytes) -> str | None:
        if plaintext in (None, ""):
            return None
        if not isinstance(plaintext, (str, bytes)):
            raise TypeError("plaintext must be str or bytes")
        data = plaintext if isinstance(plaintext, bytes) else plaintext.encode("utf-8")
        return self.fernet.encrypt(data).decode("utf-8")

    def decrypt(self, ciphertext: str | bytes) -> str | None:
        if ciphertext in (None, ""):
            return None
        if not isinstance(ciphertext, (str, bytes)):
            raise TypeError("ciphertext must be str or bytes")
        token = ciphertext if isinstance(ciphertext, bytes) else ciphertext.encode("utf-8")
        try:
            plain = self.fernet.decrypt(token)
        except InvalidToken as e:
            raise ValueError("Invalid encrypted token or wrong key") from e
        return plain.decode("utf-8")

token_cipher = TokenCipher(secret_key=settings.FERNET_KEY)