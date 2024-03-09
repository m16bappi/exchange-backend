import secrets
from eth_account import Account

from .encryptors import RsaEncryptor
from .base import BaseAccount, LocalAccount


class EvmAccount(BaseAccount):
    @classmethod
    def generate(cls) -> LocalAccount:
        priv_key = secrets.token_hex(32)
        address = Account.from_key(priv_key).address
        salt, payload = RsaEncryptor.encrypt(priv_key)

        return LocalAccount(address, salt, payload)
