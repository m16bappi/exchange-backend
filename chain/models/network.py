from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# -------- import internal modules ----------
from chain.processors import BaseProcessor, EvmProcessor
from chain.accounts import EvmAccount, LocalAccount


class ActiveNetwork(models.TextChoices):
    ETH = 'ETH', _('Ethereum')
    BSC = 'BSC', _('Binance Smart Chain')


class NetworkFmaily(models.TextChoices):
    EVM = 'EVM', _('EVM')
    BTC = 'BTC', _('Bitcoin')
    SOL = 'SOL', _('Solana')


class NetworkStrategy:
    def get_processor(self, rpc: str) -> BaseProcessor:
        raise NotImplementedError("Subclasses must implement this method")

    def get_account(self) -> LocalAccount:
        raise NotImplementedError("Subclasses must implement this method")


class EthereumNetwork(NetworkStrategy):
    def get_processor(self, rpc: str) -> BaseProcessor:
        return EvmProcessor(rpc)

    def get_account(self) -> LocalAccount:
        return EvmAccount.generate()


class BinanceSmartChainNetwork(NetworkStrategy):
    def get_processor(self, rpc: str) -> BaseProcessor:
        return EvmProcessor(rpc)

    def get_account(self) -> LocalAccount:
        return EvmAccount.generate()


class NetworkFactory:
    _network_map = {
        ActiveNetwork.ETH: EthereumNetwork,
        ActiveNetwork.BSC: BinanceSmartChainNetwork,
    }

    @staticmethod
    def get_strategy(network_name: str) -> NetworkStrategy:
        try:
            network_enum = ActiveNetwork[network_name]
            strategy_class = NetworkFactory._network_map.get(network_enum)
            if strategy_class is None:
                raise ValueError(f"No strategy found for network: {network_name}")
            return strategy_class()
        except KeyError:
            raise ValueError(f"Invalid network name: {network_name}")


class Network(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        choices=ActiveNetwork,
    )
    family = models.CharField(
        max_length=255,
        choices=NetworkFmaily,
        default=NetworkFmaily.EVM,
    )
    rpc = models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'network'
        verbose_name_plural = 'networks'

        constraints = [
            models.UniqueConstraint(
                fields=['name', 'family'],
                name='unique_network_and_family',
            )
        ]

    def __str__(self):
        return self.name

    def get_processor(self):
        strategy = NetworkFactory.get_strategy(self.name)
        return strategy.get_processor(self.rpc)

    def get_account(self):
        strategy = NetworkFactory.get_strategy(self.name)
        return strategy.get_account()


@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'family',
        'rpc',
        'created_at',
        'updated_at',
    ]
