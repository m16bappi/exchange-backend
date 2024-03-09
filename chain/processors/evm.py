from hexbytes import HexBytes
from typing import Optional, cast
from web3 import Web3, HTTPProvider
from eth_typing import BlockNumber
from eth_account.datastructures import SignedTransaction
from web3.exceptions import ProviderConnectionError, BlockNotFound
from web3.types import (
    _Hash32,
    BlockData,
    BlockIdentifier,
    Nonce,
    TxData,
    TxParams,
    TxReceipt,
    Wei,
)

from .base import BaseProcessor, _Address


class EvmProcessor(BaseProcessor):
    def __init__(self, provider_url: str) -> None:
        if not provider_url:
            raise ProviderConnectionError(
                f'{self.__class__.__name__} provider url missing or invalid'
            )
        self.web3 = Web3(HTTPProvider(provider_url))

    def get_balance(
        self,
        account: _Address,
        identifier: Optional[BlockIdentifier] = None,
    ) -> Wei:
        return self.web3.eth.get_balance(account, identifier)

    def get_block(
        self, identifier: BlockIdentifier, full_transaction: bool = False
    ) -> BlockData:
        return self.web3.eth.get_block(identifier, full_transaction)

    def get_block_number(self, transaction_hash: _Hash32) -> BlockNumber:
        tx_data = self.get_transaction(transaction_hash)
        if not tx_data.get("blockNumber"):
            raise BlockNotFound("Block not found")
        return cast(BlockNumber, tx_data.get('blockNumber'))

    def get_transaction(self, hash: _Hash32) -> TxData:
        return self.web3.eth.get_transaction(hash)

    def get_transaction_count(
        self,
        account: _Address,
        identifier: Optional[BlockIdentifier] = None,
    ) -> Nonce:
        return self.web3.eth.get_transaction_count(account, identifier)

    def get_transaction_receipt(self, transaction_hash: _Hash32) -> TxReceipt:
        return self.web3.eth.get_transaction_receipt(transaction_hash)

    def estimate_gas(
        self, transaction: TxParams, block_identifier: Optional[BlockIdentifier] = None
    ) -> int:
        return self.web3.eth.estimate_gas(transaction, block_identifier)

    def sign_transaction(self, params: TxParams, priv_key: _Hash32) -> SignedTransaction:
        return self.web3.eth.account.sign_transaction(params, priv_key)  # type: ignore

    def send_row_transaction(self, signed_tx: SignedTransaction) -> HexBytes:
        return self.web3.eth.send_raw_transaction(transaction=signed_tx.rawTransaction)
