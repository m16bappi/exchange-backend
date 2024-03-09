from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple


@dataclass
class LocalAccount:
    address: str
    salt: bytes
    payload: bytes


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


class BaseAccount(ABC):
    @classmethod
    @abstractmethod
    def generate(cls) -> LocalAccount:
        """Generates a new LocalAccount."""
        pass
