from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# -------- import internal modules ----------
from chain.processors import BaseProcessor, EvmProcessor


class ActiveNetwork(models.TextChoices):
    ETH = 'ETH', _('Ethereum')
    BSC = 'BSC', _('Binance Smart Chain')


class Network(models.Model):
    name = models.CharField(
        max_length=255, unique=True,
        choices=ActiveNetwork.choices,
    )
    rpc = models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'network'
        verbose_name = 'network'
        verbose_name_plural = 'networks'

    def __str__(self):
        return self.name

    def get_processor(self) -> BaseProcessor:
        return EvmProcessor(self.rpc)


@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ['name', 'rpc', 'created_at', 'updated_at']
