from typing import Optional
from hexbytes import HexBytes
from abc import ABC, abstractmethod
from eth_typing import Address, BlockNumber, ChecksumAddress
from eth_account.datastructures import SignedTransaction
from web3.types import (
    BlockIdentifier,
    _Hash32,
    TxData,
    ENS,
    Wei,
    BlockData,
    Nonce,
    TxParams,
    TxReceipt,
)

_Address = Address | ChecksumAddress | ENS


class BaseProcessor(ABC):
    @abstractmethod
    def get_balance(
        self,
        account: _Address,
        identifier: Optional[BlockIdentifier] = None,
    ) -> Wei: ...

    @abstractmethod
    def get_block(
        self, identifier: BlockIdentifier, full_transaction: bool = False
    ) -> BlockData: ...

    @abstractmethod
    def get_block_number(self, tx_hash: _Hash32) -> BlockNumber: ...

    @abstractmethod
    def get_transaction(self, hash: _Hash32) -> TxData: ...

    @abstractmethod
    def get_transaction_count(
        self,
        account: _Address,
        identifier: Optional[BlockIdentifier] = None,
    ) -> Nonce: ...

    @abstractmethod
    def get_transaction_receipt(self, transaction_hash: _Hash32) -> TxReceipt: ...

    @abstractmethod
    def estimate_gas(
        self, transaction: TxParams, block_identifier: Optional[BlockIdentifier] = None
    ) -> int: ...

    @abstractmethod
    def sign_transaction(
        self, params: TxParams, priv_key: _Hash32
    ) -> SignedTransaction: ...

    @abstractmethod
    def send_row_transaction(self, signed_tx: SignedTransaction) -> HexBytes: ...


class BaseContractProcessor(ABC):
    @abstractmethod
    def balanceOf(self, address: _Address) -> Wei: ...

    @abstractmethod
    def transfer(self, to_address: _Address, value: int | float) -> HexBytes: ...
