from os import environ
from typing import Literal

from .base import BaseProcessor
from .evm import EvmProcessor

__processors__ = {
    "ETH": EvmProcessor(environ['ETHEREUM_PROVIDER']),
}

ProcessorTypes = Literal["ETH"]


# @overload
# def get_processor(matcher: Literal["ETH"]) -> EvmProcessor: ...
# Todo: Enable overload if there is more processor comming
def get_processor(matcher: ProcessorTypes) -> BaseProcessor:
    return __processors__[matcher]


__all__ = ["BaseProcessor", "EvmProcessor"]
