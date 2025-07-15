import base64
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class EncryptionService:
    def __init__(self, secret_key: bytes):
        self.key = secret_key
        self.aesgcm = AESGCM(self.key)

    def encrypt(self, data: str) -> str:
        nonce = os.urandom(12)
        encrypted = self.aesgcm.encrypt(nonce, data.encode(), None)
        combined = nonce + encrypted
        return base64.urlsafe_b64encode(combined).decode()

    def decrypt(self, encrypted_data: str) -> str:
        try:
            combined = base64.urlsafe_b64decode(encrypted_data.encode())
            nonce = combined[:12]
            encrypted = combined[12:]
            decrypted = self.aesgcm.decrypt(nonce, encrypted, None)
            return decrypted.decode()
        except Exception:
            raise ValueError("Invalid or corrupted encrypted data")
