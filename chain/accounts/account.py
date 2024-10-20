import secrets
from eth_account import Account
from dataclasses import dataclass
from abc import ABC, abstractmethod

from .encryptors import FernetEncryptor


@dataclass
class LocalAccount:
    address: str
    salt: bytes
    payload: bytes


class BaseAccount(ABC):

    @classmethod
    @abstractmethod
    def generate(cls) -> LocalAccount:
        """Generates a new LocalAccount."""
        pass


class EvmAccount(BaseAccount):

    @classmethod
    def generate(cls) -> LocalAccount:
        priv_key = secrets.token_hex(32)
        address = Account.from_key(priv_key).address
        salt, payload = FernetEncryptor.encrypt(priv_key)

        return LocalAccount(address, salt, payload)
