from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# ---------- use internal module ------------------
from .network import Network


class SupportedAsset(models.TextChoices):
    ETH = 'ETH', _('ETH')
    BNB = 'BNB', _('BNB')


class Asset(models.Model):
    symbol = models.CharField(max_length=255, choices=SupportedAsset)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'asset'
        verbose_name = 'asset'
        verbose_name_plural = 'assets'
        constraints = [
            models.UniqueConstraint(
                fields=['symbol', 'network'], name='unique_asset_by_network'
            )
        ]

    @property
    def is_contract(self):
        return bool(self.address)

    def __str__(self):
        return self.symbol

    def get_processor(self):
        return self.network.get_processor()


@admin.register(Asset)
class AdminAsset(admin.ModelAdmin):
    list_display = [
        'symbol',
        'network',
        'address',
        'is_contract',
        'enabled',
    ]
