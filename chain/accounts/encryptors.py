import rsa
from typing import Tuple
from rsa import DecryptionError
from abc import ABC, abstractmethod
from cryptography.fernet import Fernet


class BaseEncryptor(ABC):
    @staticmethod
    @abstractmethod
    def encrypt(key: str) -> Tuple[bytes, bytes]:
        """Encrypts the provided key."""
        raise NotImplementedError("subclass must implement encrypt method")

    @staticmethod
    @abstractmethod
    def decrypt(salt: bytes, payload: bytes) -> str:
        """
        Decrypts the provided salt and payload.

        Args:
            salt (bytes): The salt used for encryption.
            payload (bytes): The payload to be decrypted.

        Returns:
            str: The decrypted payload.
        """
        raise NotImplementedError("subclass must implement decrypt method")


class RsaEncryptor(BaseEncryptor):
    @staticmethod
    def encrypt(key: str) -> Tuple[bytes, bytes]:
        pub_key, priv_key = rsa.newkeys(2048)
        salt = rsa.encrypt(key.encode(), pub_key)

        return (salt, priv_key.save_pkcs1("PEM"))

    @staticmethod
    def decrypt(salt: bytes, payload: bytes) -> str:
        try:
            parse_payload = rsa.PrivateKey.load_pkcs1(payload)

            return rsa.decrypt(salt, parse_payload).decode()
        except Exception as error:
            raise DecryptionError(error)


class FernetEncryptor(BaseEncryptor):

    @staticmethod
    def encrypt(key: str) -> Tuple[bytes, bytes]:
        payload = Fernet.generate_key()
        salt = Fernet(payload).encrypt(key.encode())
        return salt, payload

    @staticmethod
    def decrypt(salt: bytes, payload: bytes) -> str:
        cipher_suite = Fernet(payload)
        return cipher_suite.decrypt(salt).decode()
