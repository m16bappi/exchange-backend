import rsa
from typing import Tuple
from rsa import DecryptionError

from .base import BaseEncryptor


class RsaEncryptor(BaseEncryptor):
    @staticmethod
    def encrypt(key: str) -> Tuple[bytes, bytes]:
        pub_key, priv_key = rsa.newkeys(600)
        salt = rsa.encrypt(key.encode(), pub_key)

        return (salt, priv_key.save_pkcs1("PEM"))

    @staticmethod
    def decrypt(salt: bytes, payload: bytes) -> str:
        try:
            parse_payload = rsa.PrivateKey.load_pkcs1(payload)

            return rsa.decrypt(salt, parse_payload).decode()
        except Exception as error:
            raise DecryptionError(error)
