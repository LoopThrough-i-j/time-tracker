#!/usr/bin/env python3

import base64
import secrets


def generate_aes_gcm_key() -> str:
    key = secrets.token_bytes(32)
    return base64.b64encode(key).decode()


if __name__ == "__main__":
    key = generate_aes_gcm_key()
    print(f"Generated AES-GCM key (base64): {key}")
    print("Add this to your environment variables as SECRET_KEY")
